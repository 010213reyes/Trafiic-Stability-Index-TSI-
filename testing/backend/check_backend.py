#!/usr/bin/env python
"""Diagnostico de integridad del backend TSI basado en artefactos reales."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INVENTORY_PATH = PROJECT_ROOT / "data" / "01_processed" / "data_inventory.csv"
LINEAGE_PATH = PROJECT_ROOT / "data" / "01_processed" / "data_lineage.csv"
ALGORITHM_CHECKS = {
    "Isolation Forest": (
        "data/02_clean/traffic_enriched.csv",
        "data/02_clean/filtered_isolation_forest.csv",
        None,
    ),
    "Local Outlier Factor": (
        "data/02_clean/traffic_enriched.csv",
        "data/02_clean/filtered_local_outlier_factor.csv",
        "data/03_algorithm_output/local_outlier_factor_summary.csv",
    ),
    "DBSCAN": (
        "data/02_clean/traffic_enriched.csv",
        "data/02_clean/filtered_dbscan.csv",
        "data/03_algorithm_output/dbscan_summary.csv",
    ),
}


def report(check_name: str, passed: bool, detail: str = "") -> bool:
    status = "OK" if passed else "FALLO"
    suffix = f": {detail}" if detail else ""
    print(f"[{status}] {check_name}{suffix}")
    return passed


def check_project_files() -> bool:
    required_paths = (
        PROJECT_ROOT / "scripts" / "collect_traffic_data.py",
        PROJECT_ROOT / "data" / "00_raw",
        PROJECT_ROOT / "data" / "01_processed",
        PROJECT_ROOT / "data" / "02_clean",
        INVENTORY_PATH,
        LINEAGE_PATH,
    )
    missing = [str(path.relative_to(PROJECT_ROOT)) for path in required_paths if not path.exists()]
    return report(
        "Estructura minima del proyecto",
        not missing,
        f"faltan: {', '.join(missing)}" if missing else "",
    )


def read_table(path: Path):
    import pandas as pd

    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)


def check_dependencies() -> bool:
    passed = True
    for module_name in ("numpy", "pandas"):
        try:
            importlib.import_module(module_name)
            report(f"Dependencia {module_name}", True)
        except ImportError as error:
            report(f"Dependencia {module_name}", False, str(error))
            passed = False

    parquet_paths = list((PROJECT_ROOT / "data").rglob("*.parquet"))
    if parquet_paths:
        parquet_available = importlib.util.find_spec("pyarrow") is not None
        passed = report(
            "Lector de archivos Parquet",
            parquet_available,
            "instala pyarrow para validar salidas Parquet" if not parquet_available else "",
        ) and passed
    return passed


def check_backend_imports() -> bool:
    scripts_path = PROJECT_ROOT / "scripts"
    if str(scripts_path) not in sys.path:
        sys.path.insert(0, str(scripts_path))

    try:
        module = importlib.import_module("collect_traffic_data")
        required_functions = (
            "recolectar_datos_diarios",
            "interpolar_datos_historicos",
            "generar_anomalias_estocasticas",
        )
        missing = [name for name in required_functions if not callable(getattr(module, name, None))]
    except Exception as error:
        return report("Importacion de modulos del backend", False, str(error))

    return report(
        "Importacion de modulos del backend",
        not missing,
        f"funciones ausentes: {', '.join(missing)}" if missing else "",
    )


def check_inventory_artifacts() -> bool:
    try:
        inventory = read_table(INVENTORY_PATH)
    except Exception as error:
        return report("Lectura del inventario de datos", False, str(error))

    required_inventory_columns = {"source_id", "path", "processed_output", "clean_output", "rows", "columns", "column_names"}
    missing_columns = required_inventory_columns - set(inventory.columns)
    if missing_columns:
        return report(
            "Esquema del inventario de datos",
            False,
            f"faltan: {', '.join(sorted(missing_columns))}",
        )

    failures = []
    checked = 0
    for row in inventory.to_dict("records"):
        for field in ("path", "processed_output", "clean_output"):
            relative_path = Path(str(row[field]))
            artifact_path = PROJECT_ROOT / relative_path
            if not artifact_path.exists():
                failures.append(f"{row['source_id']}: falta {relative_path}")
                continue
            try:
                dataframe = read_table(artifact_path)
                checked += 1
                if dataframe.empty:
                    failures.append(f"{row['source_id']}: vacio {relative_path}")
            except Exception as error:
                failures.append(f"{row['source_id']}: no se puede leer {relative_path} ({error})")

        source_path = PROJECT_ROOT / Path(str(row["path"]))
        if source_path.exists():
            try:
                source = read_table(source_path)
                declared_columns = set(str(row["column_names"]).split("|"))
                if not declared_columns.issubset(source.columns):
                    failures.append(f"{row['source_id']}: columnas declaradas no coinciden")
                if len(source) != int(row["rows"]):
                    failures.append(f"{row['source_id']}: filas declaradas {row['rows']} != reales {len(source)}")
            except Exception as error:
                failures.append(f"{row['source_id']}: no se puede validar el inventario ({error})")

    return report(
        "Artefactos raw, processed y clean",
        not failures,
        "; ".join(failures) if failures else f"{checked} archivos leidos",
    )


def check_algorithm_artifacts() -> bool:
    passed = True
    for algorithm, (source_relative, output_relative, summary_relative) in ALGORITHM_CHECKS.items():
        source_path = PROJECT_ROOT / source_relative
        output_path = PROJECT_ROOT / output_relative
        try:
            source = read_table(source_path)
            output = read_table(output_path)
        except Exception as error:
            report(f"Artefactos de {algorithm}", False, str(error))
            passed = False
            continue

        algorithm_ok = not source.empty and not output.empty and len(output) <= len(source)
        detail = f"base={len(source)}, salida={len(output)}"

        if summary_relative:
            summary_path = PROJECT_ROOT / summary_relative
            try:
                summary = read_table(summary_path)
                metrics = dict(zip(summary["metric"], summary["value"]))
                summary_total = int(float(metrics["total_registros"]))
                summary_retained = int(float(metrics["registros_retenidos"]))
                algorithm_ok = algorithm_ok and summary_total == len(source) and summary_retained == len(output)
                detail += f", resumen={summary_total}/{summary_retained}"
            except Exception as error:
                algorithm_ok = False
                detail += f", resumen invalido: {error}"

        report(f"Artefactos de {algorithm}", algorithm_ok, detail)
        passed = algorithm_ok and passed

    return passed


def main() -> int:
    print("\n=== Diagnostico real del backend TSI ===")
    checks = (
        check_dependencies(),
        check_project_files(),
        check_backend_imports(),
        check_inventory_artifacts(),
        check_algorithm_artifacts(),
    )
    passed = all(checks)
    print("=== Backend verificado ===" if passed else "=== Backend con fallas ===")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())