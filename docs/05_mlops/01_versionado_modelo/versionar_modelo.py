"""Entrena y registra el candidato internacional del TSI."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


MODEL_VERSION = "rf_tsi_internacional_v1.0.0"
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
    root = project_root()
    input_path = root / "data" / "04_model_output" / "features" / "tsi_daily_features.parquet"
    metrics_path = root / "data" / "04_model_output" / "modeling" / "metricas_modelos.csv"
    registry_dir = root / "data" / "05_mlops" / "model_registry" / MODEL_VERSION
    registry_dir.mkdir(parents=True, exist_ok=True)

    features = pd.read_parquet(input_path)
    model_data, feature_columns, split_counts = build_training_data(features)
    train_validation = model_data[model_data["split"].isin(["train", "validation"])]

    model = RandomForestRegressor(**MODEL_PARAMETERS)
    model.fit(train_validation[feature_columns], train_validation[TARGET])

    model_path = registry_dir / "model.joblib"
    joblib.dump(model, model_path)

    metrics = pd.read_csv(metrics_path)
    selected_metrics = metrics.loc[metrics["modelo"] == "random_forest"].to_dict("records")
    if not selected_metrics:
        raise ValueError("No se encontro la metrica de random_forest")

    manifest = {
        "model_version": MODEL_VERSION,
        "model_name": "random_forest",
        "task": "pronostico_del_tsi_provisional_del_siguiente_dia",
        "status": "candidato_internacional_no_final",
        "target": TARGET,
        "predictors": PREDICTORS,
        "feature_columns": feature_columns,
        "model_parameters": MODEL_PARAMETERS,
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
