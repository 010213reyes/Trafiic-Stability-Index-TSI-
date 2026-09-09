# Datos externos procesados

Esta carpeta contiene representaciones Parquet derivadas de los CSV originales de `data/00_raw/external/traffic_datasets/`.

- `metr_la.parquet`: timestamps y 207 sensores de METR-LA.
- `pems_bay.parquet`: timestamps y 325 sensores de PEMS-BAY.
- `external_traffic_quality.json`: reporte reproducible de dimensiones, cobertura, frecuencia, faltantes y valores negativos.

Los CSV originales permanecen sin modificar en `data/00_raw/`. La matriz conserva el formato ancho porque cada columna representa un sensor y todavía no se requiere convertir toda la información a formato largo.