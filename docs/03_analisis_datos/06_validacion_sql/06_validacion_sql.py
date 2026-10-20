"""Valida los conteos y la cobertura de MySQL contra los resumenes Parquet."""

from __future__ import annotations

import argparse
import getpass
import json
import os
from pathlib import Path

import pandas as pd

try:
    import mysql.connector
except ImportError:  # pragma: no cover - depende del entorno local
    mysql = None
else:
    mysql = mysql.connector


REQUIRED_ENV = ["TSI_MYSQL_HOST", "TSI_MYSQL_USER", "TSI_MYSQL_DATABASE"]
GROUP_QUERY = """
SELECT
    c.nombre AS ciudad,
    f.nombre AS fuente,
    o.metrica_principal,
    COUNT(*) AS observaciones,
    MIN(o.timestamp_observacion) AS primera_observacion,
    MAX(o.timestamp_observacion) AS ultima_observacion
FROM fact_observaciones AS o
JOIN dim_ciudad AS c ON c.id_ciudad = o.id_ciudad
JOIN dim_fuente AS f ON f.id_fuente = o.id_fuente
GROUP BY c.nombre, f.nombre, o.metrica_principal
ORDER BY c.nombre, f.nombre, o.metrica_principal
"""


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--expected",
        type=Path,
        default=root / "data/03_analysis_output/eda/resumen_por_fuente.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=root / "data/03_analysis_output/validacion_sql",
    )
    parser.add_argument("--password", action="store_true", help="Solicita la contrasena sin guardarla")
    return parser.parse_args()


def connection_from_environment(ask_password: bool):
    if mysql is None:
        raise RuntimeError("Falta mysql-connector-python en el entorno activo")
    missing = [name for name in REQUIRED_ENV if not os.environ.get(name)]
    if missing:
        raise RuntimeError("Faltan variables: " + ", ".join(missing))
    password = os.environ.get("TSI_MYSQL_PASSWORD")
    if ask_password and password is None:
        password = getpass.getpass("Contrasena MySQL: ")
    return mysql.connect(
        host=os.environ["TSI_MYSQL_HOST"],
        port=int(os.environ.get("TSI_MYSQL_PORT", "3306")),
        user=os.environ["TSI_MYSQL_USER"],
        password=password or "",
        database=os.environ["TSI_MYSQL_DATABASE"],
    )


def main() -> None:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    expected = pd.DataFrame(json.loads(args.expected.read_text(encoding="utf-8")))
    expected = expected.rename(columns={"observaciones": "observaciones_parquet"})
    try:
        connection = connection_from_environment(args.password)
    except RuntimeError as error:
        (args.output / "estado.json").write_text(
            json.dumps({"estado": "pendiente", "motivo": str(error)}, indent=2),
            encoding="utf-8",
        )
        print(f"validacion_pendiente={error}")
        return

    try:
        total = pd.read_sql("SELECT COUNT(*) AS observaciones_mysql FROM fact_observaciones", connection)
        observed = pd.read_sql(GROUP_QUERY, connection)
    finally:
        connection.close()

    comparison = expected.merge(
        observed,
        on=["ciudad", "fuente", "metrica_principal"],
        how="outer",
        indicator=True,
    )
    comparison["diferencia_observaciones"] = (
        comparison["observaciones_mysql"].fillna(0) - comparison["observaciones_parquet"].fillna(0)
    )
    comparison.to_csv(args.output / "comparacion_por_fuente.csv", index=False)
    total_expected = int(expected["observaciones_parquet"].sum())
    total_mysql = int(total.iloc[0]["observaciones_mysql"])
    status = "completa" if total_expected == total_mysql and comparison["_merge"].eq("both").all() and comparison["diferencia_observaciones"].eq(0).all() else "con_discrepancias"
    (args.output / "estado.json").write_text(
        json.dumps(
            {
                "estado": status,
                "observaciones_parquet": total_expected,
                "observaciones_mysql": total_mysql,
                "diferencia_total": total_mysql - total_expected,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"estado={status}")
    print(f"parquet={total_expected}")
    print(f"mysql={total_mysql}")


if __name__ == "__main__":
    main()
