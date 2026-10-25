from __future__ import annotations

import argparse
import getpass
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
    "id_ciudad", "id_fuente", "id_segmento", "timestamp_observacion", "es_real", "calidad_registro",
    "periodo_integracion_min", "metrica_principal", "valor_principal", "valor_fuente",
    "velocidad_kmh", "flujo_veh_h", "ocupacion_pct", "densidad_veh_km", "tiempo_viaje_seg",
    "congestion_longitud_m", "indice_congestion", "intensidad_fuente", "carga_fuente", "vmed_fuente",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Carga el consolidado internacional a MySQL por lotes")
    parser.add_argument("--batch-rows", type=int, default=DEFAULT_BATCH_ROWS)
    parser.add_argument("--skip-rows", type=int, default=0, help="Salta filas ya confirmadas para reanudar una carga")
    parser.add_argument("--max-rows", type=int, default=None, help="Limita filas para una prueba")
    parser.add_argument("--rows-per-source", type=int, default=None, help="Limita filas por fuente para una prueba")
    parser.add_argument("--source-ids", default=None, help="Fuentes separadas por coma para una prueba")
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

    required = ["TSI_MYSQL_HOST", "TSI_MYSQL_USER", "TSI_MYSQL_DATABASE"]
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise RuntimeError(f"Faltan variables de entorno MySQL: {', '.join(missing)}")
    password = os.environ.get("TSI_MYSQL_PASSWORD") or getpass.getpass("Contrasena MySQL: ")

    return mysql.connector.connect(
        host=os.environ["TSI_MYSQL_HOST"],
        port=int(os.environ.get("TSI_MYSQL_PORT", "3306")),
        user=os.environ["TSI_MYSQL_USER"],
        password=password,
        database=os.environ["TSI_MYSQL_DATABASE"],
    )


def select_source_sample(frame: pd.DataFrame, source_counts: dict, rows_per_source: int | None, source_filter: set[str] | None) -> pd.DataFrame:
    if source_filter is not None:
        frame = frame[frame["fuente"].isin(source_filter)]
    if rows_per_source is None:
        return frame

    selected = []
    for source_id, source_frame in frame.groupby("fuente", sort=False):
        remaining = rows_per_source - source_counts.get(source_id, 0)
        if remaining <= 0:
            continue
        sample = source_frame.head(remaining)
        source_counts[source_id] = source_counts.get(source_id, 0) + len(sample)
        selected.append(sample)
    return pd.concat(selected, ignore_index=True) if selected else frame.head(0)


def collect_segments_and_real_flags(batch_rows: int, max_rows: int | None = None, rows_per_source: int | None = None, source_filter: set[str] | None = None) -> tuple[dict, dict]:
    parquet_file = parquet.ParquetFile(OBSERVATIONS_PATH)
    segments = {}
    real_flags = {}
    columns = ["fuente", "es_real", "ciudad", "segmento_id", "tipo_via", "latitud", "longitud"]
    scanned_rows = 0
    source_counts = {}
    for group_index, batch in enumerate(parquet_file.iter_batches(columns=columns, batch_size=batch_rows), start=1):
        frame = batch.to_pandas()
        if max_rows is not None:
            remaining = max_rows - scanned_rows
            if remaining <= 0:
                break
            frame = frame.head(remaining)
        frame = select_source_sample(frame, source_counts, rows_per_source, source_filter)
        if frame.empty:
            continue

        real_frame = frame[["fuente", "es_real"]].drop_duplicates("fuente")
        for row in real_frame.itertuples(index=False):
            real_flags.setdefault(row.fuente, bool(row.es_real))

        segment_frame = frame.drop_duplicates(["fuente", "segmento_id"])
        for row in segment_frame.itertuples(index=False):
            key = (row.fuente, row.segmento_id)
            if key not in segments:
                segments[key] = {
                    "ciudad": row.ciudad,
                    "codigo": row.segmento_id,
                    "tipo_via": clean_value(row.tipo_via) or "no_especificado",
                    "latitud": clean_value(row.latitud),
                    "longitud": clean_value(row.longitud),
                }
        scanned_rows += len(frame)
        if max_rows is None and group_index % 10 == 0:
            print(f"Preparando dimensiones: grupo {group_index}/{parquet_file.metadata.num_row_groups}", flush=True)
        if max_rows is not None and scanned_rows >= max_rows:
            break
        if rows_per_source is not None and source_filter is not None and source_filter.issubset(source_counts) and all(source_counts[source_id] >= rows_per_source for source_id in source_filter):
            break
    return segments, real_flags


def load_dimensions(connection, contract: dict, segments: dict, real_flags: dict) -> tuple[dict, dict, dict]:
    cursor = connection.cursor()
    city_ids = {}
    source_ids = {}
    contract_by_source = {item["source_id"]: item for item in contract["sources"]}

    active_sources = [source for source in contract["sources"] if source["source_id"] in real_flags]

    for source in active_sources:
        cursor.execute(
            """INSERT INTO dim_ciudad (nombre, pais, zona_horaria, es_ciudad_objetivo)
               VALUES (%s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE id_ciudad = LAST_INSERT_ID(id_ciudad)""",
            (source["city"], source["country"], source["timezone"], source["city"] == contract["objective_city"]),
        )
        city_ids[source["city"]] = cursor.lastrowid

    for source in active_sources:
        cursor.execute(
            """INSERT INTO dim_fuente
               (id_ciudad, nombre, tipo_fuente, origen_url, rol_proyecto, unidad_original, frecuencia_documentada)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE id_fuente = LAST_INSERT_ID(id_fuente)""",
            (
                city_ids[source["city"]], source["source_id"], "fuente_internacional", source.get("source_url"),
                source["role"], None, source.get("time_resolution"),
            ),
        )
        source_ids[source["source_id"]] = cursor.lastrowid

    segment_ids = {}
    for (source_id, code), segment in segments.items():
        source = contract_by_source[source_id]
        cursor.execute(
            """INSERT INTO dim_segmento
               (id_ciudad, id_fuente, identificador_origen, tipo_entidad, tipo_via, descripcion, latitud, longitud)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE id_segmento = LAST_INSERT_ID(id_segmento)""",
            (
                city_ids[source["city"]], source_ids[source_id], str(code), "sensor_o_segmento", segment["tipo_via"],
                str(code), segment["latitud"], segment["longitud"],
            ),
        )
        segment_ids[(source_id, code)] = cursor.lastrowid

    connection.commit()
    cursor.close()
    return city_ids, source_ids, segment_ids


def dimension_data(frame: pd.DataFrame) -> tuple[dict, dict]:
    real_flags = {
        row.fuente: bool(row.es_real)
        for row in frame[["fuente", "es_real"]].drop_duplicates("fuente").itertuples(index=False)
    }
    segments = {}
    segment_frame = frame[["fuente", "ciudad", "segmento_id", "tipo_via", "latitud", "longitud"]].drop_duplicates(
        ["fuente", "segmento_id"]
    )
    for row in segment_frame.itertuples(index=False):
        segments[(row.fuente, row.segmento_id)] = {
            "ciudad": row.ciudad,
            "codigo": row.segmento_id,
            "tipo_via": clean_value(row.tipo_via) or "no_especificado",
            "latitud": clean_value(row.latitud),
            "longitud": clean_value(row.longitud),
        }
    return segments, real_flags


def fact_rows(frame: pd.DataFrame, city_ids: dict, source_ids: dict, segment_ids: dict):
    for row in frame.itertuples(index=False):
        values = row._asdict()
        yield (
            city_ids[values["ciudad"]],
            source_ids[values["fuente"]],
            segment_ids[(values["fuente"], values["segmento_id"])],
            pd.Timestamp(values["timestamp"]).to_pydatetime(),
            bool(values["es_real"]),
            clean_value(values["calidad_registro"]),
            clean_value(values["periodo_integracion_min"]),
            clean_value(values["metrica_principal"]), clean_value(values["valor_principal"]),
            clean_value(values["valor_fuente"]),
            clean_value(values["velocidad_kmh"]), clean_value(values["flujo_veh_h"]),
            clean_value(values["ocupacion_pct"]), clean_value(values["densidad_veh_km"]),
            clean_value(values["tiempo_viaje_seg"]), clean_value(values["congestion_longitud_m"]),
            clean_value(values["indice_congestion"]), clean_value(values["intensidad_fuente"]),
            clean_value(values["carga_fuente"]), clean_value(values["vmed_fuente"]),
        )


def load_facts(connection, contract: dict, batch_rows: int, skip_rows: int, max_rows: int | None, rows_per_source: int | None, source_filter: set[str] | None) -> int:
    cursor = connection.cursor()
    placeholders = ", ".join(["%s"] * len(FACT_COLUMNS))
    columns = ", ".join(f"`{column}`" for column in FACT_COLUMNS)
    statement = f"INSERT INTO fact_observaciones ({columns}) VALUES ({placeholders})"
    loaded = 0
    source_counts = {}
    parquet_file = parquet.ParquetFile(OBSERVATIONS_PATH)
    city_ids = {}
    source_ids = {}
    segment_ids = {}
    rows_to_skip = skip_rows
    for group_index, batch in enumerate(parquet_file.iter_batches(batch_size=batch_rows), start=1):
        frame = batch.to_pandas()
        if rows_to_skip:
            if rows_to_skip >= len(frame):
                rows_to_skip -= len(frame)
                continue
            frame = frame.iloc[rows_to_skip:].reset_index(drop=True)
            rows_to_skip = 0
        if max_rows is not None:
            remaining = max_rows - loaded
            if remaining <= 0:
                break
            frame = frame.head(remaining)
        frame = select_source_sample(frame, source_counts, rows_per_source, source_filter)
        if frame.empty:
            if rows_per_source is not None and source_filter is not None and source_filter.issubset(source_counts) and all(source_counts[source_id] >= rows_per_source for source_id in source_filter):
                break
            continue
        segments, real_flags = dimension_data(frame)
        batch_city_ids, batch_source_ids, batch_segment_ids = load_dimensions(connection, contract, segments, real_flags)
        city_ids.update(batch_city_ids)
        source_ids.update(batch_source_ids)
        segment_ids.update(batch_segment_ids)
        rows = list(fact_rows(frame, city_ids, source_ids, segment_ids))
        started_at = datetime.now(timezone.utc)
        try:
            cursor.executemany(statement, rows)
            cursor.execute(
                """INSERT INTO log_cargas
                   (nombre_archivo, id_fuente, fecha_inicio, fecha_fin, registros_leidos,
                    registros_insertados, registros_rechazados, estado, mensaje)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (str(OBSERVATIONS_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/"), None, started_at, datetime.now(timezone.utc), len(rows), len(rows), 0, "completada", f"lote parquet {group_index}"),
            )
            connection.commit()
            loaded += len(rows)
            print(f"Lote {group_index}: {loaded:,} filas insertadas", flush=True)
        except Exception:
            connection.rollback()
            raise
    cursor.close()
    return loaded


def main() -> None:
    args = parse_args()
    if args.batch_rows <= 0:
        raise ValueError("--batch-rows debe ser mayor que cero")
    if args.skip_rows < 0:
        raise ValueError("--skip-rows no puede ser negativo")
    if args.max_rows is not None and args.rows_per_source is not None:
        raise ValueError("Usa --max-rows o --rows-per-source, no ambos")
    if args.skip_rows and (args.rows_per_source is not None or args.source_ids):
        raise ValueError("--skip-rows solo se puede combinar con una carga completa, sin filtros por fuente")
    if args.rows_per_source is not None and args.rows_per_source <= 0:
        raise ValueError("--rows-per-source debe ser mayor que cero")

    source_filter = set(args.source_ids.split(",")) if args.source_ids else None

    parquet_file = parquet.ParquetFile(OBSERVATIONS_PATH)
    print(f"Entrada: {OBSERVATIONS_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Filas: {parquet_file.metadata.num_rows:,} | grupos: {parquet_file.metadata.num_row_groups} | lote: {args.batch_rows:,}")
    if args.max_rows is not None:
        print(f"Limite de prueba: {args.max_rows:,} filas")
    if args.skip_rows:
        print(f"Reanudacion: se saltan {args.skip_rows:,} filas ya confirmadas")
    if args.rows_per_source is not None:
        print(f"Limite por fuente: {args.rows_per_source:,} filas")
    if source_filter:
        print(f"Fuentes seleccionadas: {', '.join(sorted(source_filter))}")
    if not args.execute:
        print("Modo validacion: no se conecta a MySQL. Usa --execute para cargar.")
        return

    contract = read_contract()
    contract_source_ids = {source["source_id"] for source in contract["sources"]}
    if source_filter and not source_filter.issubset(contract_source_ids):
        unknown = sorted(source_filter - contract_source_ids)
        raise ValueError(f"Fuentes desconocidas: {unknown}")
    connection = connect_mysql()
    try:
        loaded = load_facts(connection, contract, args.batch_rows, args.skip_rows, args.max_rows, args.rows_per_source, source_filter)
        print(f"Filas insertadas: {loaded:,}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()