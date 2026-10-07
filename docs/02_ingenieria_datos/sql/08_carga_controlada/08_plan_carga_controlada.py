from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pyarrow.parquet as parquet


PROJECT_ROOT = Path(__file__).resolve().parents[4]
OBSERVATIONS_PATH = PROJECT_ROOT / "data" / "02_clean" / "consolidated" / "international_observations.parquet"
CONSOLIDATION_MANIFEST_PATH = PROJECT_ROOT / "data" / "02_clean" / "consolidated" / "international_consolidation_manifest.json"
SQL_DIR = PROJECT_ROOT / "docs" / "02_ingenieria_datos" / "sql"
DEFAULT_OUTPUT_PATH = SQL_DIR / "sql08_controlled_load_plan.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera el plan de carga controlada SQL-08")
    parser.add_argument("--batch-rows", type=int, default=250_000)
    parser.add_argument("--output-path", default=str(DEFAULT_OUTPUT_PATH))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.batch_rows <= 0:
        raise ValueError("--batch-rows debe ser mayor que cero")

    parquet_file = parquet.ParquetFile(OBSERVATIONS_PATH)
    consolidation_manifest = json.loads(CONSOLIDATION_MANIFEST_PATH.read_text(encoding="utf-8"))
    rows_per_group = [parquet_file.metadata.row_group(index).num_rows for index in range(parquet_file.metadata.num_row_groups)]
    total_rows = sum(rows_per_group)
    batches = (total_rows + args.batch_rows - 1) // args.batch_rows
    sources = consolidation_manifest["consolidated_output"]["sources"]

    plan = {
        "pipeline": "sql08_controlled_load_plan",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "planned_not_executed",
        "source_dataset": str(OBSERVATIONS_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "target_engine": "mysql_innodb",
        "batch_rows": args.batch_rows,
        "total_rows": total_rows,
        "parquet_row_groups": len(rows_per_group),
        "planned_batches": batches,
        "row_group_sizes": {
            "min": min(rows_per_group),
            "max": max(rows_per_group),
            "first": rows_per_group[0],
        },
        "sources": sources,
        "execution_order": [
            "crear esquema y restricciones en MySQL",
            "cargar dim_ciudad y dim_fuente desde el contrato",
            "cargar dim_segmento con claves fuente + segmento_id",
            "leer el Parquet por grupos y enviar lotes a fact_observaciones",
            "registrar cada lote en log_cargas",
            "crear índices temporales después de la carga de hechos",
            "ejecutar SQL-09 sobre conteos y relaciones",
        ],
        "controls": {
            "max_rows_in_memory": args.batch_rows,
            "transactions": "una transaccion por lote",
            "retry_policy": "reintentar el lote fallido sin duplicar cargas",
            "duplicate_guard": "clave de lote y conteo confirmado antes de commit",
            "null_policy": "conservar NULL en metricas; normalizar tipo_via ausente como no_especificado",
        },
        "not_run_reason": "La carga completa requiere una instancia MySQL disponible y credenciales fuera del repositorio.",
    }
    output_path = Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(plan, ensure_ascii=False))


if __name__ == "__main__":
    main()