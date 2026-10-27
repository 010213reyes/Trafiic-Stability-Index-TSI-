"""Ejecuta inferencia con un modelo TSI versionado, sin reentrenar."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd

PREDICTION_DECIMALS = 10
MODEL_FAMILY = "rf_tsi_internacional"


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


def latest_model_version(root: Path) -> str:
    registry_dir = root / "data" / "05_mlops" / "model_registry"
    pattern = re.compile(rf"^{re.escape(MODEL_FAMILY)}_v(\d+)\.(\d+)\.(\d+)$")
    versions = []
    for candidate in registry_dir.iterdir() if registry_dir.exists() else []:
        match = pattern.match(candidate.name)
        if match and (candidate / "manifest.json").exists():
            versions.append((tuple(int(part) for part in match.groups()), candidate.name))
    if not versions:
        raise FileNotFoundError("No hay versiones registradas del modelo")
    return max(versions)[1]


def load_registry(root: Path, model_version: str) -> tuple[object, dict, Path]:
    registry_dir = root / "data" / "05_mlops" / "model_registry" / model_version
    model_path = registry_dir / "model.joblib"
    manifest_path = registry_dir / "manifest.json"
    if not model_path.exists() or not manifest_path.exists():
        raise FileNotFoundError(f"Registro incompleto para la version: {model_version}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return joblib.load(model_path), manifest, registry_dir


def prepare_features(data: pd.DataFrame, manifest: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    predictors = manifest["predictors"]
    feature_columns = manifest["feature_columns"]
    required = sorted(set(predictors + ["fuente"]))
    missing = sorted(set(required) - set(data.columns))
    if missing:
        raise ValueError(f"Faltan columnas requeridas para inferencia: {missing}")

    eligible = data.dropna(subset=predictors).copy()
    if eligible.empty:
        raise ValueError("No hay filas completas para inferencia")

    encoded = pd.get_dummies(eligible, columns=["fuente"], dtype=float)
    encoded = encoded.reindex(columns=feature_columns, fill_value=0.0)
    return eligible, encoded


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="Archivo Parquet o CSV de entrada")
    parser.add_argument(
        "--model-version",
        help="Version registrada; si se omite, se usa automaticamente la mas reciente",
    )
    parser.add_argument("--output", type=Path, help="Archivo CSV de predicciones")
    return parser.parse_args()


def read_input(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    raise ValueError("La entrada debe ser un archivo .parquet o .csv")


def main() -> None:
    args = parse_args()
    root = project_root()
    input_path = args.input or (
        root / "data" / "04_model_output" / "features" / "tsi_daily_features.parquet"
    )
    output_path = args.output or (
        root / "data" / "05_mlops" / "inference" / "predicciones_tsi.csv"
    )
    output_path = output_path if output_path.is_absolute() else root / output_path
    input_path = input_path if input_path.is_absolute() else root / input_path

    model_version = args.model_version or latest_model_version(root)
    model, manifest, registry_dir = load_registry(root, model_version)
    data = read_input(input_path)
    eligible, encoded = prepare_features(data, manifest)
    predictions = model.predict(encoded)

    output_columns = [
        column for column in ["fecha", "ciudad", "fuente", "metrica_principal"] if column in eligible
    ]
    results = eligible[output_columns].copy()
    results["prediccion_tsi_siguiente"] = predictions.round(PREDICTION_DECIMALS)
    target = manifest["target"]
    if target in eligible.columns:
        results[target] = eligible[target].to_numpy()
        results["error_absoluto"] = (
            results[target] - results["prediccion_tsi_siguiente"]
        ).abs().round(PREDICTION_DECIMALS)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_path, index=False)
    metadata = {
        "run_at_utc": datetime.now(timezone.utc).isoformat(),
        "model_version": manifest["model_version"],
        "model_name": manifest["model_name"],
        "input_path": str(input_path.relative_to(root)),
        "input_sha256": sha256_file(input_path),
        "registry_path": str(registry_dir.relative_to(root)),
        "output_path": str(output_path.relative_to(root)),
        "rows_input": int(len(data)),
        "rows_inferred": int(len(results)),
        "rows_skipped_incomplete": int(len(data) - len(results)),
        "prediction_column": "prediccion_tsi_siguiente",
        "prediction_decimals": PREDICTION_DECIMALS,
    }
    metadata_path = output_path.with_suffix(".json")
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=True), encoding="utf-8")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
