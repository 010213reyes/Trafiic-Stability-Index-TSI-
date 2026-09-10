# 2.1 Inventario y linaje de datos

## Estado

Completado.

## Actividades

- Listar las fuentes de `data/00_raw/`.
- Registrar formato, columnas, cantidad de registros y cobertura temporal.
- Identificar fuentes locales, externas y sintéticas.
- Registrar el origen de cada dataset.
- Relacionar cada fuente con su salida prevista en `data/01_processed/` y `data/02_clean/`.

## Fuentes iniciales

- `traffic_data.csv`
- `scraped_traffic.csv`
- `crowdsourcing_raw.csv`
- `crowdsourcing_aggregated.csv`
- `synthetic_traffic.csv`
- METR-LA
- PEMS-BAY

## Entregables

```text
data/01_processed/data_inventory.csv
data/01_processed/data_lineage.csv
```

El inventario se genera con:

```text
python docs/02_ingenieria_datos/01_inventario_linaje/generar_inventario_linaje.py
```

## Resultado

Se registraron nueve entradas raw: cinco fuentes locales, dos datasets externos y dos catálogos de sensores. Cada entrada incluye formato, filas, columnas, nulos, duplicados, cobertura temporal cuando existe, origen y salida prevista.
