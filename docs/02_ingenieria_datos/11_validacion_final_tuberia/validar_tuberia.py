from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

CHECKS = [
    PROJECT_ROOT / "data" / "00_raw",
    PROJECT_ROOT / "data" / "01_processed" / "pipeline" / "pipeline_manifest.json",
    PROJECT_ROOT / "data" / "01_processed" / "normalized" / "normalization_manifest.json",
    PROJECT_ROOT / "data" / "01_processed" / "quality" / "quality_report.json",
    PROJECT_ROOT / "data" / "02_clean" / "consolidated" / "consolidation_manifest.json",
    PROJECT_ROOT / "data" / "02_clean" / "dataset_clean" / "dataset_clean_manifest.json",
    PROJECT_ROOT / "data" / "02_clean" / "dataset_clean" / "clean_observations.parquet",
    PROJECT_ROOT / "docs" / "02_ingenieria_datos" / "sql" / "tsi_stage.sqlite",
    PROJECT_ROOT / "docs" / "02_ingenieria_datos" / "sql" / "sql_load_manifest.json",
]


def check_path(path: Path) -> dict[str, object]:
    return {
        "path": str(path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "exists": path.exists(),
    }


def main() -> None:
    results = [check_path(path) for path in CHECKS]
    missing = [item for item in results if not item["exists"]]
    if missing:
        payload = {
            "status": "fail",
            "missing": missing,
            "checked": results,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    ok = {
        "status": "ok",
        "checked": results,
        "pipeline_summary": {
            "raw_dir": True,
            "processed_manifest": True,
            "normalization_manifest": True,
            "quality_report": True,
            "consolidation_manifest": True,
            "dataset_clean_manifest": True,
            "clean_observations": True,
            "sqlite_db": True,
            "sql_load_manifest": True,
        },
    }
    print(json.dumps(ok, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
