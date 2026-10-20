"""Resume la cobertura y los patrones temporales del consolidado internacional."""

from __future__ import annotations

import argparse
import math
from collections import defaultdict
from pathlib import Path

import pandas as pd
import pyarrow.dataset as ds


COLUMNS = ["timestamp", "ciudad", "fuente", "metrica_principal", "valor_principal"]
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
        default=root / "data/03_analysis_output/analisis_temporal",
    )
    parser.add_argument("--batch-size", type=int, default=250_000)
    parser.add_argument("--max-rows", type=int, default=None)
    return parser.parse_args()


def key_value(value: object) -> str:
    return "__NULL__" if pd.isna(value) else str(value)


def update_stats(stats: dict[str, float], values: pd.Series) -> None:
    numeric = pd.to_numeric(values, errors="coerce").dropna()
    if numeric.empty:
        return
    stats["count"] += int(numeric.count())
    stats["sum"] += float(numeric.sum())
    stats["sum_sq"] += float((numeric**2).sum())
    stats["min"] = min(stats["min"], float(numeric.min()))
    stats["max"] = max(stats["max"], float(numeric.max()))


def stats_row(stats: dict[str, float]) -> dict[str, float | int | None]:
    count = int(stats["count"])
    if count == 0:
        return {"observaciones": 0, "media": None, "desviacion": None, "minimo": None, "maximo": None}
    variance = max((stats["sum_sq"] - stats["sum"] ** 2 / count) / max(count - 1, 1), 0.0)
    return {
        "observaciones": count,
        "media": stats["sum"] / count,
        "desviacion": math.sqrt(variance),
        "minimo": stats["min"],
        "maximo": stats["max"],
    }


def new_stats() -> dict[str, float]:
    return {"count": 0, "sum": 0.0, "sum_sq": 0.0, "min": float("inf"), "max": float("-inf")}


def main() -> None:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    dataset = ds.dataset(args.input, format="parquet")
    daily: dict[tuple[str, ...], dict[str, float]] = defaultdict(new_stats)
    hourly: dict[tuple[str, ...], dict[str, float]] = defaultdict(new_stats)
    weekday: dict[tuple[str, ...], dict[str, float]] = defaultdict(new_stats)
    total_rows = 0

    for batch in dataset.scanner(columns=COLUMNS, batch_size=args.batch_size).to_batches():
        frame = batch.to_pandas()
        if args.max_rows is not None:
            remaining = args.max_rows - total_rows
            if remaining <= 0:
                break
            frame = frame.iloc[:remaining]
        total_rows += len(frame)
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], errors="coerce")
        frame = frame.dropna(subset=["timestamp"])
        frame["fecha"] = frame["timestamp"].dt.strftime("%Y-%m-%d")
        frame["hora"] = frame["timestamp"].dt.hour
        frame["dia_semana"] = frame["timestamp"].dt.dayofweek

        for keys, group in frame.groupby(GROUP_COLUMNS + ["fecha"], dropna=False, sort=False):
            normalized = tuple(key_value(value) for value in keys)
            update_stats(daily[normalized], group["valor_principal"])
        for keys, group in frame.groupby(GROUP_COLUMNS + ["hora"], dropna=False, sort=False):
            normalized = tuple(key_value(value) for value in keys)
            update_stats(hourly[normalized], group["valor_principal"])
        for keys, group in frame.groupby(GROUP_COLUMNS + ["dia_semana"], dropna=False, sort=False):
            normalized = tuple(key_value(value) for value in keys)
            update_stats(weekday[normalized], group["valor_principal"])

    def build_rows(groups: dict[tuple[str, ...], dict[str, float]], extra_columns: list[str]) -> list[dict[str, object]]:
        rows = []
        for keys, stats in sorted(groups.items()):
            row = dict(zip(GROUP_COLUMNS + extra_columns, keys))
            row.update(stats_row(stats))
            rows.append(row)
        return rows

    pd.DataFrame(build_rows(daily, ["fecha"])).to_csv(args.output / "cobertura_diaria.csv", index=False)
    pd.DataFrame(build_rows(hourly, ["hora"])).to_csv(args.output / "resumen_por_hora.csv", index=False)
    pd.DataFrame(build_rows(weekday, ["dia_semana"])).to_csv(args.output / "resumen_por_dia_semana.csv", index=False)
    print(f"filas={total_rows}")
    print(f"salida={args.output}")


if __name__ == "__main__":
    main()
