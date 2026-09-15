from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = [
    "data/00_raw",
    "data/01_processed/pipeline/pipeline_manifest.json",
    "data/01_processed/normalized/normalization_manifest.json",
    "data/01_processed/quality/quality_report.json",
    "data/02_clean/consolidated/consolidation_manifest.json",
    "data/02_clean/dataset_clean/dataset_clean_manifest.json",
    "data/02_clean/dataset_clean/clean_observations.parquet",
    "docs/02_ingenieria_datos/sql/tsi_stage.sqlite",
    "docs/02_ingenieria_datos/sql/sql_load_manifest.json",
]


def build_manifest() -> dict[str, object]:
    checked = []
    for relative in ARTIFACTS:
        path = PROJECT_ROOT / relative
        checked.append(
            {
                "artifact": relative.replace("\\", "/"),
                "exists": path.exists(),
                "type": "directory" if path.is_dir() else "file",
            }
        )

    return {
        "pipeline": "reproducibility_and_traceability",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(PROJECT_ROOT).replace("\\", "/"),
        "checks": checked,
        "status": "ok" if all(item["exists"] for item in checked) else "warning",
    }


def main() -> None:
    manifest = build_manifest()
    output_path = PROJECT_ROOT / "docs" / "02_ingenieria_datos" / "10_reproducibilidad_trazabilidad" / "reproducibility_manifest.json"
    output_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"status": manifest["status"], "output": str(output_path.relative_to(PROJECT_ROOT)).replace("\\", "/")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
