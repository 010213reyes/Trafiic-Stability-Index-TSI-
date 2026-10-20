"""Genera un perfil exploratorio por lotes del consolidado internacional."""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

import pandas as pd
import pyarrow.dataset as ds


COLUMNS = [
    "timestamp",
    "ciudad",
    "fuente",
    "es_real",
    "segmento_id",
    "tipo_via",
    "calidad_registro",
    "metrica_principal",
    "valor_principal",
    "valor_fuente",
    "periodo_integracion_min",
]
NUMERIC_COLUMNS = ["valor_principal", "valor_fuente", "periodo_integracion_min"]
GROUP_COLUMNS = ["ciudad", "fuente", "metrica_principal"]


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=root / "data/02_clean/consolidated/international_observations.parquet",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=root / "data/03_analysis_output/eda",
    )
    parser.add_argument("--batch-size", type=int, default=250_000)
    parser.add_argument("--max-rows", type=int, default=None)
    return parser.parse_args()


def text_value(value: object) -> str:
    if pd.isna(value):
        return "__NULL__"
    return str(value)


def update_numeric_stats(stats: dict[str, float], values: pd.Series) -> None:
    numeric = pd.to_numeric(values, errors="coerce").dropna()
    if numeric.empty:
        return
    stats["count"] += int(numeric.count())
    stats["sum"] += float(numeric.sum())
    stats["sum_sq"] += float((numeric**2).sum())
    stats["min"] = min(stats["min"], float(numeric.min()))
    stats["max"] = max(stats["max"], float(numeric.max()))


def finalize_numeric_stats(stats: dict[str, float]) -> dict[str, float | int | None]:
    count = int(stats["count"])
    if count == 0:
        return {"count": 0, "mean": None, "std": None, "min": None, "max": None}
    variance = max(
        (stats["sum_sq"] - (stats["sum"] ** 2 / count)) / max(count - 1, 1),
        0.0,
    )
    return {
        "count": count,
        "mean": stats["sum"] / count,
        "std": math.sqrt(variance),
        "min": stats["min"],
        "max": stats["max"],
    }


def main() -> None:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    dataset = ds.dataset(args.input, format="parquet")
    null_counts = defaultdict(int)
    group_counts = defaultdict(int)
    numeric_stats = defaultdict(
        lambda: {
            "count": 0,
            "sum": 0.0,
            "sum_sq": 0.0,
            "min": float("inf"),
            "max": float("-inf"),
        }
    )
    total_rows = 0
    min_timestamp = None
    max_timestamp = None

    scanner = dataset.scanner(columns=COLUMNS, batch_size=args.batch_size)
    for batch in scanner.to_batches():
        frame = batch.to_pandas()
        if args.max_rows is not None:
            remaining = args.max_rows - total_rows
            if remaining <= 0:
                break
            frame = frame.iloc[:remaining]
        total_rows += len(frame)
        for column in COLUMNS:
            null_counts[column] += int(frame[column].isna().sum())

        timestamps = pd.to_datetime(frame["timestamp"], errors="coerce").dropna()
        if not timestamps.empty:
            batch_min = timestamps.min()
            batch_max = timestamps.max()
            min_timestamp = batch_min if min_timestamp is None else min(min_timestamp, batch_min)
            max_timestamp = batch_max if max_timestamp is None else max(max_timestamp, batch_max)

        for keys, group in frame.groupby(GROUP_COLUMNS, dropna=False, sort=False):
            normalized_keys = tuple(text_value(value) for value in keys)
            group_counts[normalized_keys] += len(group)
            for column in NUMERIC_COLUMNS:
                update_numeric_stats(numeric_stats[normalized_keys + (column,)], group[column])

    summary_rows = []
    for keys, count in sorted(group_counts.items()):
        row = dict(zip(GROUP_COLUMNS, keys))
        row["observaciones"] = count
        for column in NUMERIC_COLUMNS:
            row[column] = finalize_numeric_stats(numeric_stats[keys + (column,)])
        summary_rows.append(row)

    pd.DataFrame(summary_rows).to_json(
        args.output / "resumen_por_fuente.json",
        orient="records",
        indent=2,
        force_ascii=True,
    )
    pd.DataFrame(
        [{"campo": column, "nulos": null_counts[column], "total": total_rows} for column in COLUMNS]
    ).assign(porcentaje_nulo=lambda frame: frame["nulos"] / total_rows * 100).to_csv(
        args.output / "nulos_por_campo.csv", index=False
    )
    (args.output / "perfil_global.json").write_text(
        json.dumps(
            {
                "filas": total_rows,
                "grupos_ciudad_fuente_metrica": len(group_counts),
                "timestamp_minimo": min_timestamp.isoformat() if min_timestamp is not None else None,
                "timestamp_maximo": max_timestamp.isoformat() if max_timestamp is not None else None,
                "batch_size": args.batch_size,
                "max_rows": args.max_rows,
                "input": str(args.input),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"filas={total_rows}")
    print(f"grupos={len(group_counts)}")
    print(f"salida={args.output}")


if __name__ == "__main__":
    main()
