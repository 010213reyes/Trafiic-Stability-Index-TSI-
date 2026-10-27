"""Evalua calidad, drift y desempeño de una ejecución del flujo TSI."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


MISSING_WARNING = 0.01
MISSING_ALERT = 0.05
DRIFT_WARNING = 2.0
DRIFT_ALERT = 3.0
MAE_WARNING = 3.5
MAE_ALERT = 5.0
ANOMALY_WARNING = 0.10
ANOMALY_ALERT = 0.20
MODEL_FAMILY = "rf_tsi_internacional"


def project_root() -> Path:
    root = Path(__file__).resolve().parents[3]
    if not (root / "data").exists():
        raise FileNotFoundError("No se encontro la carpeta data del proyecto")
    return root


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model-version",
        help="Version registrada; si se omite, se usa automaticamente la mas reciente",
    )
    return parser.parse_args()


def level(value: float, warning: float, alert: float) -> str:
    if value >= alert:
        return "alert"
    if value >= warning:
        return "warning"
    return "ok"


def add_check(checks: list[dict], name: str, value: float, status: str, threshold: dict, detail: str) -> None:
    checks.append(
        {
            "name": name,
            "value": value,
            "status": status,
            "threshold": threshold,
            "detail": detail,
        }
    )


def main() -> None:
    args = parse_args()
    root = project_root()
    model_version = args.model_version or latest_model_version(root)
    registry_dir = root / "data" / "05_mlops" / "model_registry" / model_version
    manifest = json.loads((registry_dir / "manifest.json").read_text(encoding="utf-8"))
    features_path = root / "data" / "04_model_output" / "features" / "tsi_daily_features.parquet"
    predictions_path = root / "data" / "05_mlops" / "inference" / "predicciones_tsi.csv"
    anomaly_path = root / "data" / "04_model_output" / "anomalies" / "resumen_anomalias.csv"
    output_dir = root / "data" / "05_mlops" / "monitoring"
    output_dir.mkdir(parents=True, exist_ok=True)

    features = pd.read_parquet(features_path)
    predictions = pd.read_csv(predictions_path)
    checks: list[dict] = []
    predictors = manifest["predictors"]
    reference_profile = manifest.get("reference_profile", {})

    missing_rates = features[predictors].isna().mean()
    incomplete_rate = float(features[predictors].isna().any(axis=1).mean())
    add_check(
        checks,
        "filas_incompletas_features",
        incomplete_rate,
        level(incomplete_rate, MISSING_WARNING, MISSING_ALERT),
        {"warning": MISSING_WARNING, "alert": MISSING_ALERT},
        f"{int((features[predictors].isna().any(axis=1)).sum())} filas con al menos una feature faltante",
    )

    for column, rate in missing_rates.items():
        add_check(
            checks,
            f"nulos_{column}",
            float(rate),
            level(float(rate), MISSING_WARNING, MISSING_ALERT),
            {"warning": MISSING_WARNING, "alert": MISSING_ALERT},
            f"{int(features[column].isna().sum())} valores faltantes",
        )

    drift_values = {}
    for column in predictors:
        current = pd.to_numeric(features[column], errors="coerce")
        reference = reference_profile.get(column)
        if reference is None or current.notna().sum() == 0:
            continue
        denominator = reference["std"] if reference["std"] > 0 else 1.0
        shift = abs(float(current.mean()) - reference["mean"]) / denominator
        drift_values[column] = shift
        add_check(
            checks,
            f"drift_media_{column}",
            shift,
            level(shift, DRIFT_WARNING, DRIFT_ALERT),
            {"warning": DRIFT_WARNING, "alert": DRIFT_ALERT},
            "distancia de la media actual respecto al perfil de entrenamiento en desviaciones estandar",
        )

    prediction_column = "prediccion_tsi_siguiente"
    out_of_range_rate = float(
        ((predictions[prediction_column] < 0) | (predictions[prediction_column] > 100)).mean()
    )
    add_check(
        checks,
        "predicciones_fuera_de_rango_tsi",
        out_of_range_rate,
        "alert" if out_of_range_rate > 0 else "ok",
        {"alert": 0.0},
        "el TSI provisional debe permanecer entre 0 y 100",
    )

    performance = {
        "rows": int(len(predictions)),
        "mae": None,
        "rmse": None,
        "p95_error_absoluto": None,
    }
    if "error_absoluto" in predictions.columns:
        errors = pd.to_numeric(predictions["error_absoluto"], errors="coerce").dropna()
        if not errors.empty:
            mae = float(errors.mean())
            rmse = float((errors.pow(2).mean()) ** 0.5)
            p95 = float(errors.quantile(0.95))
            performance.update({"mae": mae, "rmse": rmse, "p95_error_absoluto": p95})
            add_check(
                checks,
                "mae_inferencia",
                mae,
                level(mae, MAE_WARNING, MAE_ALERT),
                {"warning": MAE_WARNING, "alert": MAE_ALERT},
                "error observado en las filas con objetivo disponible",
            )

    anomaly_summary = None
    if anomaly_path.exists():
        anomalies = pd.read_csv(anomaly_path)
        anomalies["tasa_isolation"] = anomalies["isolation_anomalias"] / anomalies["observaciones"]
        total_observations = anomalies["observaciones"].sum()
        total_anomalies = anomalies["isolation_anomalias"].sum()
        anomaly_rate = float(total_anomalies / total_observations)
        add_check(
            checks,
            "tasa_anomalias_isolation_forest",
            anomaly_rate,
            level(anomaly_rate, ANOMALY_WARNING, ANOMALY_ALERT),
            {"warning": ANOMALY_WARNING, "alert": ANOMALY_ALERT},
            "tasa agregada reportada por el detector exploratorio",
        )
        anomaly_summary = {
            "observaciones": int(total_observations),
            "isolation_anomalias": int(total_anomalies),
            "tasa_isolation": anomaly_rate,
            "por_fuente": anomalies.to_dict("records"),
        }

    statuses = [check["status"] for check in checks]
    overall_status = "alert" if "alert" in statuses else "warning" if "warning" in statuses else "ok"
    report = {
        "report_at_utc": datetime.now(timezone.utc).isoformat(),
        "model_version": manifest["model_version"],
        "status": overall_status,
        "inputs": {
            "features": "data/04_model_output/features/tsi_daily_features.parquet",
            "predictions": "data/05_mlops/inference/predicciones_tsi.csv",
            "anomalies": "data/04_model_output/anomalies/resumen_anomalias.csv",
        },
        "rows": {"features": int(len(features)), "predictions": int(len(predictions))},
        "performance": performance,
        "drift_max_mean_shift": max(drift_values.values(), default=None),
        "anomalies": anomaly_summary,
        "checks": checks,
        "limitations": [
            "el drift es descriptivo y usa cambios de media por feature",
            "las anomalias no tienen ground truth externo",
            "el desempeño depende del objetivo TSI provisional disponible",
        ],
    }
    output_path = output_dir / "reporte_monitoreo.json"
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=True), encoding="utf-8")
    print(json.dumps({"status": overall_status, "output": str(output_path), "checks": len(checks)}, indent=2))


if __name__ == "__main__":
    main()
