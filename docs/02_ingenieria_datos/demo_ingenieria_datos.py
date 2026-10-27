from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ARTIFACTS = {
    "RAW": PROJECT_ROOT / "data" / "00_raw",
    "PROCESSED - pipeline manifest": PROJECT_ROOT / "data" / "01_processed" / "pipeline" / "pipeline_manifest.json",
    "PROCESSED - normalization manifest": PROJECT_ROOT / "data" / "01_processed" / "normalized" / "normalization_manifest.json",
    "PROCESSED - quality report": PROJECT_ROOT / "data" / "01_processed" / "quality" / "quality_report.json",
    "CLEAN - consolidation manifest": PROJECT_ROOT / "data" / "02_clean" / "consolidated" / "consolidation_manifest.json",
    "CLEAN - international quality": PROJECT_ROOT / "data" / "02_clean" / "external" / "international_clean_quality.json",
    "CLEAN - consolidated observations": PROJECT_ROOT / "data" / "02_clean" / "consolidated" / "international_observations.parquet",
    "SQL-07 - SQLite test database": PROJECT_ROOT / "docs" / "02_ingenieria_datos" / "sql" / "07_carga_prueba" / "tsi_international_stage.sqlite",
    "SQL-07 - test manifest": PROJECT_ROOT / "docs" / "02_ingenieria_datos" / "sql" / "07_carga_prueba" / "sql07_international_load_manifest.json",
    "SQL legacy - SQLite database": PROJECT_ROOT / "docs" / "02_ingenieria_datos" / "sql" / "legacy_prototipo" / "tsi_stage.sqlite",
    "SQL legacy - load manifest": PROJECT_ROOT / "docs" / "02_ingenieria_datos" / "sql" / "legacy_prototipo" / "sql_load_manifest.json",
    "SQL-08 - controlled-load plan": PROJECT_ROOT / "docs" / "02_ingenieria_datos" / "sql" / "08_carga_controlada" / "sql08_controlled_load_plan.json",
    "SQL-08 - execution manifest": PROJECT_ROOT / "docs" / "02_ingenieria_datos" / "sql" / "08_carga_controlada" / "sql08_execution_manifest.json",
}


def relative(path: Path) -> str:
    return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")


def load_json(path: Path) -> dict[str, object] | None:
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def main() -> None:
    print("TSI - DEMOSTRACION DE INGENIERIA DE DATOS")
    print("=" * 48)
    print("Evidencia basada en artefactos existentes; no simula ejecuciones.")
    print()

    available = 0
    for label, path in ARTIFACTS.items():
        exists = path.exists()
        available += int(exists)
        status = "DISPONIBLE" if exists else "NO DISPONIBLE"
        print(f"[{status:9}] {label}: {relative(path)}")

    print()
    print(f"Artefactos disponibles: {available}/{len(ARTIFACTS)}")

    manifest_path = ARTIFACTS["PROCESSED - pipeline manifest"]
    manifest = load_json(manifest_path)
    if manifest is not None:
        sources = manifest.get("sources")
        source_count = len(sources) if isinstance(sources, list) else "no disponible"
        print(f"Fuentes registradas en el manifiesto: {source_count}")

    consolidation = load_json(ARTIFACTS["CLEAN - consolidation manifest"])
    if consolidation is not None:
        observation_output = consolidation.get("observation_output")
        if isinstance(observation_output, dict):
            print("Consolidacion de observaciones: disponible")
            print(f"Salida consolidada: {observation_output.get('output_path', 'no disponible')}")

    test_manifest = load_json(ARTIFACTS["SQL-07 - test manifest"])
    if test_manifest is not None:
        validation = test_manifest.get("validation")
        fact_rows = validation.get("fact_rows") if isinstance(validation, dict) else "no disponible"
        print(f"SQL-07 - prueba SQLite validada: {fact_rows} filas")

    legacy_manifest = load_json(ARTIFACTS["SQL legacy - load manifest"])
    if legacy_manifest is not None:
        tables = legacy_manifest.get("tables")
        fact_rows = tables.get("fact_observaciones") if isinstance(tables, dict) else "no disponible"
        print(f"SQL legacy - SQLite cargada: {fact_rows} filas")

    controlled_plan = load_json(ARTIFACTS["SQL-08 - controlled-load plan"])
    if controlled_plan is not None:
        print(
            "SQL-08 - carga MySQL planificada: "
            f"{controlled_plan.get('total_rows', 'no disponible')} filas"
        )
        print(f"Estado registrado: {controlled_plan.get('status', 'no disponible')}")

    execution = load_json(ARTIFACTS["SQL-08 - execution manifest"])
    if execution is not None:
        validation = execution.get("validation")
        load_log_history = execution.get("load_log_history")
        print(
            "SQL-08 - carga MySQL ejecutada: "
            f"{execution.get('observations_current', 'no disponible')} filas actuales"
        )
        rejected_rows = validation.get("rows_rejected_current", "no disponible") if isinstance(validation, dict) else "no disponible"
        print(f"Filas rechazadas actuales: {rejected_rows}")
        print(
            "Estado de validacion: "
            f"{validation.get('status', 'no disponible') if isinstance(validation, dict) else 'no disponible'}"
        )
        if isinstance(load_log_history, dict):
            print(
                "Historial de log_cargas: "
                f"{load_log_history.get('states', 'no disponible')}"
            )

    print()
    print("Flujo documentado: raw -> processed -> clean -> SQL")
    print("SQL-07 y SQL legacy corresponden a cargas SQLite verificables.")
    print("SQL-08 incluye el plan y la evidencia de ejecucion de la carga controlada hacia MySQL.")


if __name__ == "__main__":
    main()
