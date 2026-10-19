"""Consolida el estado y los hallazgos disponibles de la fase de analisis."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


PHASES = {
    "01_eda": "completada",
    "02_calidad_cobertura": "completada",
    "03_analisis_temporal": "completada",
    "04_comparacion_fuentes": "completada",
    "05_indicador_tsi": "provisional",
    "06_validacion_sql": "pendiente_carga_mysql",
}


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=root / "data/03_analysis_output",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=root / "data/03_analysis_output/resultados",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    profile = json.loads((args.input / "eda/perfil_global.json").read_text(encoding="utf-8"))
    quality = json.loads((args.input / "calidad_cobertura/calidad_global.json").read_text(encoding="utf-8"))
    sql_state = json.loads((args.input / "validacion_sql/estado.json").read_text(encoding="utf-8"))
    comparison = pd.read_csv(args.input / "comparacion_fuentes/matriz_comparabilidad.csv")
    tsi_method = json.loads((args.input / "indicador_tsi/metodo.json").read_text(encoding="utf-8"))

    source_findings = comparison[
        [
            "ciudad",
            "fuente",
            "metrica_principal",
            "familia_metrica",
            "unidad_conceptual",
            "comparacion_directa",
            "condicion_comparacion",
        ]
    ].to_dict(orient="records")
    report = {
        "estado_fase": "analisis_exploratorio_completado_con_validacion_sql_pendiente",
        "observaciones_evaluadas": profile["filas"],
        "grupos_ciudad_fuente_metrica": profile["grupos_ciudad_fuente_metrica"],
        "calidad": {
            "filas_evaluadas": quality["filas_evaluadas"],
            "controles_de_rango": quality["controles_de_rango"],
        },
        "fases": PHASES,
        "indicador_tsi": {
            "tipo": tsi_method["tipo"],
            "normalizacion": tsi_method["normalizacion"],
            "fuentes_mezcladas": tsi_method["fuentes_mezcladas"],
        },
        "validacion_sql": sql_state,
        "fuentes": source_findings,
        "siguiente_decision": "completar_carga_mysql_y_ejecutar_validacion_sql",
    }
    (args.output / "estado_fase_analisis.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    pd.DataFrame(source_findings).to_csv(args.output / "hallazgos_por_fuente.csv", index=False)
    print(f"estado={report['estado_fase']}")
    print(f"observaciones={report['observaciones_evaluadas']}")
    print(f"salida={args.output}")


if __name__ == "__main__":
    main()
