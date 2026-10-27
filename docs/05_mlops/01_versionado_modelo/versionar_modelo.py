"""Entrena y registra el candidato internacional del TSI."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


MODEL_FAMILY = "rf_tsi_internacional"
PREDICTORS = [
    "tsi_provisional_media",
    "tsi_lag_1",
    "tsi_lag_7",
    "delta_1",
    "media_movil_3",
    "media_movil_7",
    "desviacion_movil_7",
    "dia_semana",
    "mes",
    "es_fin_de_semana",
    "observaciones",
]
TARGET = "objetivo_tsi_siguiente"
MODEL_PARAMETERS = {
    "n_estimators": 150,
    "min_samples_leaf": 5,
    "random_state": 42,
    "n_jobs": -1,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model-version",
        help="Version manual opcional; si se omite, incrementa automaticamente el parche.",
    )
    return parser.parse_args()


def next_model_version(root: Path) -> str:
    registry_dir = root / "data" / "05_mlops" / "model_registry"
    pattern = re.compile(rf"^{re.escape(MODEL_FAMILY)}_v(\d+)\.(\d+)\.(\d+)$")
    versions = []
    for candidate in registry_dir.iterdir() if registry_dir.exists() else []:
        match = pattern.match(candidate.name)
        if match and candidate.is_dir():
            versions.append(tuple(int(part) for part in match.groups()))
    if not versions:
        return f"{MODEL_FAMILY}_v1.0.0"
    major, minor, patch = max(versions)
    return f"{MODEL_FAMILY}_v{major}.{minor}.{patch + 1}"


def project_root() -> Path:
    root = Path(__file__).resolve().parents[3]
    if not (root / "data").exists():
        raise FileNotFoundError("No se encontro la carpeta data del proyecto")
    return root


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_training_data(features: pd.DataFrame) -> tuple[pd.DataFrame, list[str], dict[str, int]]:
    missing = sorted(set(PREDICTORS + [TARGET, "fuente", "fecha"]) - set(features.columns))
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {missing}")

    model_data = features.dropna(subset=PREDICTORS + [TARGET]).copy()
    model_data["fecha"] = pd.to_datetime(model_data["fecha"])
    parts = []
    split_counts: dict[str, int] = {"train": 0, "validation": 0, "test": 0}

    for source, group in model_data.groupby("fuente", sort=False):
        group = group.sort_values("fecha").copy()
        train_end = int(len(group) * 0.60)
        validation_end = int(len(group) * 0.80)
        group["split"] = (
            ["train"] * train_end
            + ["validation"] * (validation_end - train_end)
            + ["test"] * (len(group) - validation_end)
        )
        for split, count in group["split"].value_counts().items():
            split_counts[split] += int(count)
        parts.append(group)

    model_data = pd.concat(parts, ignore_index=True)
    model_data = pd.get_dummies(model_data, columns=["fuente"], dtype=float)
    source_columns = sorted(column for column in model_data.columns if column.startswith("fuente_"))
    feature_columns = PREDICTORS + source_columns
    return model_data, feature_columns, split_counts


def main() -> None:
    args = parse_args()
    root = project_root()
    model_version = args.model_version or next_model_version(root)
    input_path = root / "data" / "04_model_output" / "features" / "tsi_daily_features.parquet"
    metrics_path = root / "data" / "04_model_output" / "modeling" / "metricas_modelos.csv"
    registry_dir = root / "data" / "05_mlops" / "model_registry" / model_version
    registry_dir.mkdir(parents=True, exist_ok=True)

    features = pd.read_parquet(input_path)
    model_data, feature_columns, split_counts = build_training_data(features)
    train_validation = model_data[model_data["split"].isin(["train", "validation"])]

    model = RandomForestRegressor(**MODEL_PARAMETERS)
    model.fit(train_validation[feature_columns], train_validation[TARGET])

    model_path = registry_dir / "model.joblib"
    joblib.dump(model, model_path)

    reference_profile = {}
    for column in feature_columns:
        values = train_validation[column].astype(float)
        reference_profile[column] = {
            "mean": float(values.mean()),
            "std": float(values.std(ddof=0)),
            "min": float(values.min()),
            "max": float(values.max()),
        }

    metrics = pd.read_csv(metrics_path)
    selected_metrics = metrics.loc[metrics["modelo"] == "random_forest"].to_dict("records")
    if not selected_metrics:
        raise ValueError("No se encontro la metrica de random_forest")

    manifest = {
        "model_version": model_version,
        "model_name": "random_forest",
        "task": "pronostico_del_tsi_provisional_del_siguiente_dia",
        "status": "seleccionado_para_demostracion_internacional",
        "target": TARGET,
        "predictors": PREDICTORS,
        "feature_columns": feature_columns,
        "model_parameters": MODEL_PARAMETERS,
        "reference_profile": reference_profile,
        "training_policy": "train_plus_validation_temporal_por_fuente",
        "rows": {
            "features_input": int(len(features)),
            "eligible": int(len(model_data)),
            "train": split_counts["train"],
            "validation": split_counts["validation"],
            "test_reserved": split_counts["test"],
            "fit": int(len(train_validation)),
        },
        "evaluation_metrics": selected_metrics[0],
        "data": {
            "path": "data/04_model_output/features/tsi_daily_features.parquet",
            "sha256": sha256_file(input_path),
        },
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "limitations": [
            "TSI provisional y especifico por fuente",
            "sin etiqueta externa de pre_colapso",
            "sin calibracion local de Guadalajara",
        ],
    }
    (registry_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=True), encoding="utf-8"
    )
    print(json.dumps({"model_path": str(model_path), "manifest": manifest}, indent=2))


if __name__ == "__main__":
    main()
