from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pyarrow.parquet as parquet


PROJECT_ROOT = Path(__file__).resolve().parents[4]
DATA_ROOT = PROJECT_ROOT / "data"
OBSERVATIONS_PATH = DATA_ROOT / "02_clean" / "consolidated" / "international_observations.parquet"
CONTRACT_PATH = DATA_ROOT / "00_raw" / "external" / "international_sources_contract.json"
DEFAULT_BATCH_ROWS = 250_000

FACT_COLUMNS = [
    "timestamp", "ciudad_id", "fuente_id", "segmento_id", "metrica_principal", "valor_principal",
    "velocidad_kmh", "flujo_veh_h", "ocupacion_pct", "densidad_veh_km", "tiempo_viaje_seg",
    "congestion_longitud_m", "indice_congestion", "intensidad_fuente", "carga_fuente", "vmed_fuente",
    "calidad_registro",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Carga el consolidado internacional a MySQL por lotes")
    parser.add_argument("--batch-rows", type=int, default=DEFAULT_BATCH_ROWS)
    parser.add_argument("--execute", action="store_true", help="Ejecuta la carga; sin esta bandera solo valida el plan")
    return parser.parse_args()


def clean_value(value):
    return None if pd.isna(value) else value


def read_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def connect_mysql():
    try:
        import mysql.connector
    except ModuleNotFoundError as error:
        raise RuntimeError("Falta mysql-connector-python. Instala dependencias antes de usar --execute.") from error

    required = ["TSI_MYSQL_HOST", "TSI_MYSQL_USER", "TSI_MYSQL_PASSWORD", "TSI_MYSQL_DATABASE"]
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise RuntimeError(f"Faltan variables de entorno MySQL: {', '.join(missing)}")

    return mysql.connector.connect(
        host=os.environ["TSI_MYSQL_HOST"],
        port=int(os.environ.get("TSI_MYSQL_PORT", "3306")),
        user=os.environ["TSI_MYSQL_USER"],
        password=os.environ["TSI_MYSQL_PASSWORD"],
        database=os.environ["TSI_MYSQL_DATABASE"],
    )


def collect_segments_and_real_flags(batch_rows: int) -> tuple[dict, dict]:
    parquet_file = parquet.ParquetFile(OBSERVATIONS_PATH)
    segments = {}
    real_flags = {}
    columns = ["fuente", "es_real", "ciudad", "segmento_id", "tipo_via", "latitud", "longitud"]
    for batch in parquet_file.iter_batches(columns=columns, batch_size=batch_rows):
        frame = batch.to_pandas()
        for row in frame.itertuples(index=False):
            real_flags.setdefault(row.fuente, bool(row.es_real))
            key = (row.fuente, row.segmento_id)
            if key not in segments:
                segments[key] = {
                    "ciudad": row.ciudad,
                    "codigo": row.segmento_id,
                    "tipo_via": clean_value(row.tipo_via) or "no_especificado",
                    "latitud": clean_value(row.latitud),
                    "longitud": clean_value(row.longitud),
                }
    return segments, real_flags


def load_dimensions(connection, contract: dict, segments: dict, real_flags: dict) -> tuple[dict, dict, dict]:
    cursor = connection.cursor()
    city_ids = {}
    source_ids = {}
    contract_by_source = {item["source_id"]: item for item in contract["sources"]}

    for source in contract["sources"]:
        cursor.execute(
            """INSERT INTO dim_ciudad (nombre, pais, zona_horaria, es_ciudad_objetivo)
               VALUES (%s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE ciudad_id = LAST_INSERT_ID(ciudad_id)""",
            (source["city"], source["country"], source["timezone"], source["city"] == contract["objective_city"]),
        )
        city_ids[source["city"]] = cursor.lastrowid

    for source in contract["sources"]:
        cursor.execute(
            """INSERT INTO dim_fuente
               (ciudad_id, nombre, tipo_fuente, origen_url, rol_dato, es_real, frecuencia_documentada)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE fuente_id = LAST_INSERT_ID(fuente_id)""",
            (
                city_ids[source["city"]], source["source_id"], "fuente_internacional", source.get("source_url"),
                source["role"], real_flags[source["source_id"]], source.get("time_resolution"),
            ),
        )
        source_ids[source["source_id"]] = cursor.lastrowid

    segment_ids = {}
    for (source_id, code), segment in segments.items():
        source = contract_by_source[source_id]
        cursor.execute(
            """INSERT INTO dim_segmento
               (ciudad_id, fuente_id, codigo_segmento, nombre_segmento, tipo_via, latitud, longitud)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE segmento_id = LAST_INSERT_ID(segmento_id)""",
            (
                city_ids[source["city"]], source_ids[source_id], str(code), str(code), segment["tipo_via"],
                segment["latitud"], segment["longitud"],
            ),
        )
        segment_ids[(source_id, code)] = cursor.lastrowid

    connection.commit()
    cursor.close()
    return city_ids, source_ids, segment_ids


def fact_rows(frame: pd.DataFrame, city_ids: dict, source_ids: dict, segment_ids: dict):
    for row in frame.itertuples(index=False):
        values = row._asdict()
        yield (
            pd.Timestamp(values["timestamp"]).to_pydatetime(),
            city_ids[values["ciudad"]],
            source_ids[values["fuente"]],
            segment_ids[(values["fuente"], values["segmento_id"])],
            clean_value(values["metrica_principal"]), clean_value(values["valor_principal"]),
            clean_value(values["velocidad_kmh"]), clean_value(values["flujo_veh_h"]),
            clean_value(values["ocupacion_pct"]), clean_value(values["densidad_veh_km"]),
            clean_value(values["tiempo_viaje_seg"]), clean_value(values["congestion_longitud_m"]),
            clean_value(values["indice_congestion"]), clean_value(values["intensidad_fuente"]),
            clean_value(values["carga_fuente"]), clean_value(values["vmed_fuente"]),
            clean_value(values["calidad_registro"]),
        )


def load_facts(connection, city_ids: dict, source_ids: dict, segment_ids: dict, batch_rows: int) -> int:
    cursor = connection.cursor()
    placeholders = ", ".join(["%s"] * len(FACT_COLUMNS))
    columns = ", ".join(f"`{column}`" for column in FACT_COLUMNS)
    statement = f"INSERT INTO fact_observaciones ({columns}) VALUES ({placeholders})"
    loaded = 0
    parquet_file = parquet.ParquetFile(OBSERVATIONS_PATH)
    for group_index, batch in enumerate(parquet_file.iter_batches(batch_size=batch_rows), start=1):
        frame = batch.to_pandas()
        rows = list(fact_rows(frame, city_ids, source_ids, segment_ids))
        started_at = datetime.now(timezone.utc)
        try:
            cursor.executemany(statement, rows)
            cursor.execute(
                """INSERT INTO log_cargas
                   (archivo_origen, fecha_inicio, fecha_fin, filas_leidas, filas_insertadas,
                    filas_rechazadas, estado, mensaje)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (str(OBSERVATIONS_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"), started_at, datetime.now(timezone.utc), len(rows), len(rows), 0, "completada", f"lote parquet {group_index}"),
            )
            connection.commit()
            loaded += len(rows)
        except Exception:
            connection.rollback()
            raise
    cursor.close()
    return loaded


def main() -> None:
    args = parse_args()
    if args.batch_rows <= 0:
        raise ValueError("--batch-rows debe ser mayor que cero")

    parquet_file = parquet.ParquetFile(OBSERVATIONS_PATH)
    print(f"Entrada: {OBSERVATIONS_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Filas: {parquet_file.metadata.num_rows:,} | grupos: {parquet_file.metadata.num_row_groups} | lote: {args.batch_rows:,}")
    if not args.execute:
        print("Modo validacion: no se conecta a MySQL. Usa --execute para cargar.")
        return

    contract = read_contract()
    segments, real_flags = collect_segments_and_real_flags(args.batch_rows)
    connection = connect_mysql()
    try:
        city_ids, source_ids, segment_ids = load_dimensions(connection, contract, segments, real_flags)
        loaded = load_facts(connection, city_ids, source_ids, segment_ids, args.batch_rows)
        print(f"Filas insertadas: {loaded:,}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()