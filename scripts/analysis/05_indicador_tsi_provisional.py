"""Calcula un componente TSI provisional normalizado dentro de cada fuente."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import pandas as pd
import pyarrow.dataset as ds


COLUMNS = ["timestamp", "ciudad", "fuente", "metrica_principal", "valor_principal"]
DIRECTIONS = {
    "indice_congestion": "lower_is_better",
    "velocidad_sensor": "higher_is_better",
    "intensidad": "lower_is_better",
    "congestion_longitud_m": "lower_is_better",
}


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=root / "data/02_clean/consolidated/international_observations.parquet",
    )
    parser.add_argument(
        "--eda",
        type=Path,
        default=root / "data/03_analysis_output/eda/resumen_por_fuente.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=root / "data/03_analysis_output/indicador_tsi",
    )
    parser.add_argument("--batch-size", type=int, default=250_000)
    parser.add_argument("--max-rows", type=int, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    source_profiles = json.loads(args.eda.read_text(encoding="utf-8"))
    bounds = {
        (row["fuente"], row["metrica_principal"]): (
            float(row["valor_principal"]["min"]),
            float(row["valor_principal"]["max"]),
        )
        for row in source_profiles
    }
    aggregates: dict[tuple[str, ...], dict[str, float]] = defaultdict(
        lambda: {"observaciones": 0.0, "suma_tsi": 0.0, "min_tsi": 100.0, "max_tsi": 0.0}
    )
    total_rows = 0
    dataset = ds.dataset(args.input, format="parquet")
    for batch in dataset.scanner(columns=COLUMNS, batch_size=args.batch_size).to_batches():
        frame = batch.to_pandas()
        if args.max_rows is not None:
            remaining = args.max_rows - total_rows
            if remaining <= 0:
                break
            frame = frame.iloc[:remaining]
        total_rows += len(frame)
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], errors="coerce")
        frame["valor_principal"] = pd.to_numeric(frame["valor_principal"], errors="coerce")
        frame = frame.dropna(subset=["timestamp", "valor_principal"])
        frame["fecha"] = frame["timestamp"].dt.strftime("%Y-%m-%d")
        for keys, group in frame.groupby(["ciudad", "fuente", "metrica_principal", "fecha"], sort=False):
            ciudad, fuente, metrica, fecha = keys
            minimum, maximum = bounds[(fuente, metrica)]
            spread = maximum - minimum
            if spread == 0:
                score = pd.Series(50.0, index=group.index)
            elif DIRECTIONS[metrica] == "higher_is_better":
                score = (group["valor_principal"] - minimum) / spread * 100
            else:
                score = (maximum - group["valor_principal"]) / spread * 100
            score = score.clip(0, 100)
            key = (ciudad, fuente, metrica, fecha)
            state = aggregates[key]
            state["observaciones"] += len(score)
            state["suma_tsi"] += float(score.sum())
            state["min_tsi"] = min(state["min_tsi"], float(score.min()))
            state["max_tsi"] = max(state["max_tsi"], float(score.max()))

    rows = []
    for keys, state in sorted(aggregates.items()):
        ciudad, fuente, metrica, fecha = keys
        rows.append(
            {
                "ciudad": ciudad,
                "fuente": fuente,
                "metrica_principal": metrica,
                "fecha": fecha,
                "observaciones": int(state["observaciones"]),
                "tsi_provisional_media": state["suma_tsi"] / state["observaciones"],
                "tsi_provisional_minimo": state["min_tsi"],
                "tsi_provisional_maximo": state["max_tsi"],
                "direccion": DIRECTIONS[metrica],
            }
        )
    pd.DataFrame(rows).to_csv(args.output / "tsi_provisional_diario.csv", index=False)
    (args.output / "metodo.json").write_text(
        json.dumps(
            {
                "tipo": "provisional",
                "normalizacion": "min_max_dentro_de_cada_fuente_y_metrica",
                "escala": "0_100",
                "fuentes_mezcladas": False,
                "filas_evaluadas": total_rows,
                "limitacion": "requiere validacion de unidades, sensibilidad a extremos y calibracion local",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"filas={total_rows}")
    print(f"dias_fuente={len(rows)}")
    print(f"salida={args.output}")


if __name__ == "__main__":
    main()
