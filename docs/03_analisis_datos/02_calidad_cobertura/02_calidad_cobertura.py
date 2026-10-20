"""Evalua calidad y cobertura del consolidado internacional por lotes."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
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
    "latitud",
    "longitud",
    "periodo_integracion_min",
]
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
        default=root / "data/03_analysis_output/calidad_cobertura",
    )
    parser.add_argument("--batch-size", type=int, default=250_000)
    parser.add_argument("--max-rows", type=int, default=None)
    return parser.parse_args()


def key_value(value: object) -> str:
    return "__NULL__" if pd.isna(value) else str(value)


def add_counter(target: Counter, values: pd.Series) -> None:
    target.update(values.map(key_value).value_counts().to_dict())


def main() -> None:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    dataset = ds.dataset(args.input, format="parquet")
    groups: dict[tuple[str, ...], dict[str, object]] = defaultdict(
        lambda: {
            "observaciones": 0,
            "timestamp_minimo": None,
            "timestamp_maximo": None,
            "nulos": Counter(),
            "calidad": Counter(),
            "es_real": Counter(),
        }
    )
    range_checks = Counter()
    total_rows = 0
    scanner = dataset.scanner(columns=COLUMNS, batch_size=args.batch_size)

    for batch in scanner.to_batches():
        frame = batch.to_pandas()
        if args.max_rows is not None:
            remaining = args.max_rows - total_rows
            if remaining <= 0:
                break
            frame = frame.iloc[:remaining]
        total_rows += len(frame)
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], errors="coerce")
        for keys, group in frame.groupby(GROUP_COLUMNS, dropna=False, sort=False):
            normalized = tuple(key_value(value) for value in keys)
            state = groups[normalized]
            state["observaciones"] += len(group)
            timestamp = group["timestamp"].dropna()
            if not timestamp.empty:
                current_min = timestamp.min()
                current_max = timestamp.max()
                state["timestamp_minimo"] = current_min if state["timestamp_minimo"] is None else min(state["timestamp_minimo"], current_min)
                state["timestamp_maximo"] = current_max if state["timestamp_maximo"] is None else max(state["timestamp_maximo"], current_max)
            for column in COLUMNS:
                state["nulos"][column] += int(group[column].isna().sum())
            add_counter(state["calidad"], group["calidad_registro"])
            add_counter(state["es_real"], group["es_real"])

        checks = {
            "timestamp_invalido": frame["timestamp"].isna(),
            "valor_principal_negativo": pd.to_numeric(frame["valor_principal"], errors="coerce") < 0,
            "valor_fuente_negativo": pd.to_numeric(frame["valor_fuente"], errors="coerce") < 0,
            "latitud_fuera_rango": frame["latitud"].notna() & ~frame["latitud"].between(-90, 90, inclusive="both"),
            "longitud_fuera_rango": frame["longitud"].notna() & ~frame["longitud"].between(-180, 180, inclusive="both"),
            "periodo_no_positivo": pd.to_numeric(frame["periodo_integracion_min"], errors="coerce") <= 0,
        }
        for name, invalid in checks.items():
            range_checks[name] += int(invalid.fillna(False).sum())

    coverage_rows = []
    quality_rows = []
    for keys, state in sorted(groups.items()):
        row = dict(zip(GROUP_COLUMNS, keys))
        row["observaciones"] = state["observaciones"]
        row["timestamp_minimo"] = state["timestamp_minimo"].isoformat() if state["timestamp_minimo"] is not None else None
        row["timestamp_maximo"] = state["timestamp_maximo"].isoformat() if state["timestamp_maximo"] is not None else None
        for column in COLUMNS:
            row[f"nulos_{column}"] = state["nulos"][column]
        coverage_rows.append(row)
        for label, counter in [("calidad_registro", state["calidad"]), ("es_real", state["es_real"])]:
            for value, count in sorted(counter.items()):
                quality_rows.append({**dict(zip(GROUP_COLUMNS, keys)), "campo": label, "valor": value, "observaciones": count})

    pd.DataFrame(coverage_rows).to_csv(args.output / "cobertura_por_fuente.csv", index=False)
    pd.DataFrame(quality_rows).to_csv(args.output / "etiquetas_por_fuente.csv", index=False)
    pd.DataFrame([{"control": name, "registros_invalidos": count} for name, count in sorted(range_checks.items())]).to_csv(
        args.output / "controles_de_rango.csv", index=False
    )
    (args.output / "calidad_global.json").write_text(
        json.dumps(
            {
                "filas_evaluadas": total_rows,
                "grupos_evaluados": len(groups),
                "controles_de_rango": dict(sorted(range_checks.items())),
                "input": str(args.input),
                "max_rows": args.max_rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"filas={total_rows}")
    print(f"grupos={len(groups)}")
    print(f"salida={args.output}")


if __name__ == "__main__":
    main()
