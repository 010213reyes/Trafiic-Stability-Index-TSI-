"""Construye una matriz de comparabilidad entre las fuentes internacionales."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


SOURCE_DEFINITIONS = {
    "istanbul_traffic_index": {
        "familia_metrica": "indice_congestion",
        "unidad_conceptual": "indice relativo",
        "interpretacion": "nivel de congestion reportado por la fuente",
    },
    "metr_la": {
        "familia_metrica": "velocidad",
        "unidad_conceptual": "velocidad de sensor",
        "interpretacion": "velocidad observada por sensor",
    },
    "madrid_traffic_points": {
        "familia_metrica": "intensidad",
        "unidad_conceptual": "intensidad de trafico",
        "interpretacion": "intensidad reportada por punto de trafico",
    },
    "pems_bay": {
        "familia_metrica": "velocidad",
        "unidad_conceptual": "velocidad de sensor",
        "interpretacion": "velocidad observada por sensor",
    },
    "sao_paulo_cet": {
        "familia_metrica": "congestion_longitud",
        "unidad_conceptual": "longitud congestionada",
        "interpretacion": "longitud de congestion reportada por la fuente",
    },
}


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--eda",
        type=Path,
        default=root / "data/03_analysis_output/eda/resumen_por_fuente.json",
    )
    parser.add_argument(
        "--coverage",
        type=Path,
        default=root / "data/03_analysis_output/analisis_temporal/cobertura_diaria.csv",
    )
    parser.add_argument(
        "--hourly",
        type=Path,
        default=root / "data/03_analysis_output/analisis_temporal/resumen_por_hora.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=root / "data/03_analysis_output/comparacion_fuentes",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    eda = pd.DataFrame(json.loads(args.eda.read_text(encoding="utf-8")))
    coverage = pd.read_csv(args.coverage)
    coverage_summary = coverage.groupby(
        ["ciudad", "fuente", "metrica_principal"], as_index=False
    ).agg(
        fecha_minima=("fecha", "min"),
        fecha_maxima=("fecha", "max"),
        dias_observados=("fecha", "nunique"),
    )
    hourly = pd.read_csv(args.hourly)
    hourly_summary = hourly.groupby(
        ["ciudad", "fuente", "metrica_principal"], as_index=False
    ).agg(horas_observadas=("hora", "nunique"))
    rows = []
    for _, row in eda.iterrows():
        definition = SOURCE_DEFINITIONS.get(row["fuente"], {})
        rows.append(
            {
                "ciudad": row["ciudad"],
                "fuente": row["fuente"],
                "metrica_principal": row["metrica_principal"],
                "familia_metrica": definition.get("familia_metrica", "no_documentada"),
                "unidad_conceptual": definition.get("unidad_conceptual", "no_documentada"),
                "interpretacion": definition.get("interpretacion", "no_documentada"),
                "observaciones": row["observaciones"],
                "media_valor_principal": row["valor_principal"]["mean"],
                "minimo_valor_principal": row["valor_principal"]["min"],
                "maximo_valor_principal": row["valor_principal"]["max"],
            }
        )
    profiles = pd.DataFrame(rows).merge(
        coverage_summary,
        on=["ciudad", "fuente", "metrica_principal"],
        how="left",
    )
    profiles = profiles.merge(
        hourly_summary,
        on=["ciudad", "fuente", "metrica_principal"],
        how="left",
    )
    profiles["comparacion_directa"] = profiles["familia_metrica"].eq("velocidad")
    profiles["condicion_comparacion"] = profiles["comparacion_directa"].map(
        {
            True: "verificar unidad y alinear ventana temporal",
            False: "no comparar en escala original",
        }
    )
    profiles.to_csv(args.output / "perfil_comparativo_fuentes.csv", index=False)

    matrix = profiles[
        [
            "ciudad",
            "fuente",
            "metrica_principal",
            "familia_metrica",
            "unidad_conceptual",
            "comparacion_directa",
            "condicion_comparacion",
        ]
    ].sort_values(["familia_metrica", "fuente"])
    matrix.to_csv(args.output / "matriz_comparabilidad.csv", index=False)
    print(f"fuentes={len(profiles)}")
    print(f"candidatas_comparacion_directa={int(profiles['comparacion_directa'].sum())}")
    print(f"salida={args.output}")


if __name__ == "__main__":
    main()
