"""Registra Ridge y el baseline junto al modelo principal del TSI."""

from __future__ import annotations

import hashlib
import json
import re
import argparse
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from versionar_modelo import PREDICTORS, TARGET, build_training_data


MODEL_FAMILIES = {
    "ridge": "ridge_tsi_internacional",
    "baseline": "baseline_persistencia_tsi",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model",
        choices=["all", "ridge", "baseline"],
        default="all",
        help="Modelo comparativo que se registra",
    )
    return parser.parse_args()


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


def next_family_version(root: Path, family: str) -> str:
    registry_dir = root / "data" / "05_mlops" / "model_registry"
    pattern = re.compile(rf"^{re.escape(family)}_v(\d+)\.(\d+)\.(\d+)$")
    versions = []
    for candidate in registry_dir.iterdir() if registry_dir.exists() else []:
        match = pattern.match(candidate.name)
        if match and candidate.is_dir():
            versions.append(tuple(int(part) for part in match.groups()))
    if not versions:
        return f"{family}_v1.0.0"
    major, minor, patch = max(versions)
    return f"{family}_v{major}.{minor}.{patch + 1}"


def common_manifest(
    model_version: str,
    model_name: str,
    status: str,
    features: pd.DataFrame,
    model_data: pd.DataFrame,
    feature_columns: list[str],
    split_counts: dict[str, int],
    metrics: dict,
    input_sha256: str,
    artifact_type: str,
    parameters: dict,
) -> dict:
    return {
        "model_version": model_version,
        "model_name": model_name,
        "task": "pronostico_del_tsi_provisional_del_siguiente_dia",
        "status": status,
        "artifact_type": artifact_type,
        "target": TARGET,
        "predictors": PREDICTORS,
        "feature_columns": feature_columns,
        "model_parameters": parameters,
        "training_policy": "train_plus_validation_temporal_por_fuente",
        "rows": {
            "features_input": int(len(features)),
            "eligible": int(len(model_data)),
            "train": split_counts["train"],
            "validation": split_counts["validation"],
            "test_reserved": split_counts["test"],
            "fit": int(len(model_data[model_data["split"].isin(["train", "validation"])])),
        },
        "evaluation_metrics": metrics,
        "data": {
            "path": "data/04_model_output/features/tsi_daily_features.parquet",
            "sha256": input_sha256,
        },
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "limitations": [
            "TSI provisional y especifico por fuente",
            "sin etiqueta externa de pre_colapso",
            "sin calibracion local de Guadalajara",
        ],
    }


def main() -> None:
    args = parse_args()
    root = project_root()
    input_path = root / "data" / "04_model_output" / "features" / "tsi_daily_features.parquet"
    metrics_path = root / "data" / "04_model_output" / "modeling" / "metricas_modelos.csv"
    features = pd.read_parquet(input_path)
    model_data, feature_columns, split_counts = build_training_data(features)
    train_validation = model_data[model_data["split"].isin(["train", "validation"])]
    metrics_frame = pd.read_csv(metrics_path)
    input_sha256 = sha256_file(input_path)
    results = []

    ridge_metrics = metrics_frame.loc[metrics_frame["modelo"] == "ridge"].to_dict("records")
    if args.model in {"all", "ridge"} and ridge_metrics:
        ridge_version = next_family_version(root, MODEL_FAMILIES["ridge"])
        ridge_dir = root / "data" / "05_mlops" / "model_registry" / ridge_version
        ridge_dir.mkdir(parents=True, exist_ok=True)
        ridge_model = make_pipeline(StandardScaler(), Ridge(alpha=1.0))
        ridge_model.fit(train_validation[feature_columns], train_validation[TARGET])
        joblib.dump(ridge_model, ridge_dir / "model.joblib")
        ridge_manifest = common_manifest(
            ridge_version,
            "ridge",
            "evaluado_no_seleccionado",
            features,
            model_data,
            feature_columns,
            split_counts,
            ridge_metrics[0],
            input_sha256,
            "serialized_model",
            {"alpha": 1.0},
        )
        (ridge_dir / "manifest.json").write_text(json.dumps(ridge_manifest, indent=2, ensure_ascii=True), encoding="utf-8")
        results.append(ridge_version)

    baseline_metrics = metrics_frame.loc[metrics_frame["modelo"] == "baseline_persistencia"].to_dict("records")
    if args.model in {"all", "baseline"} and baseline_metrics:
        baseline_version = next_family_version(root, MODEL_FAMILIES["baseline"])
        baseline_dir = root / "data" / "05_mlops" / "model_registry" / baseline_version
        baseline_dir.mkdir(parents=True, exist_ok=True)
        baseline_manifest = common_manifest(
            baseline_version,
            "baseline_persistencia",
            "referencia_no_entrenable",
            features,
            model_data,
            ["tsi_lag_1"],
            split_counts,
            baseline_metrics[0],
            input_sha256,
            "deterministic_rule",
            {"formula": "prediccion_tsi_siguiente = tsi_lag_1"},
        )
        (baseline_dir / "manifest.json").write_text(json.dumps(baseline_manifest, indent=2, ensure_ascii=True), encoding="utf-8")
        results.append(baseline_version)

    print(json.dumps({"registered_models": results}, indent=2))


if __name__ == "__main__":
    main()
