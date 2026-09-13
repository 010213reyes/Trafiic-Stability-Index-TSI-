# 2.6 Integración y consolidación

## Estado

Completado.

## Actividades

- Integrar las fuentes compatibles.
- Conservar ciudad, fuente, segmento y tipo de vía.
- Evitar duplicar fuentes raw y agregadas.
- Separar observaciones incompatibles o rechazadas.

## Implementación

El proceso se ejecuta con:

```text
python docs/02_ingenieria_datos/06_integracion_consolidacion/consolidar_datos.py
```

Salidas:

```text
data/02_clean/consolidated/consolidated_observations.parquet
data/02_clean/consolidated/derived_aggregates.parquet
data/02_clean/consolidated/sensor_catalog.parquet
data/02_clean/consolidated/consolidation_manifest.json
```

`crowdsourcing_aggregated` se conserva separado para no duplicar `crowdsourcing_raw`. Los metadatos de sensores se conservan como catálogo espacial.

## Entregable

Dataset consolidado por observación y segmento, con agregados y catálogos separados.

## Resultado

- 6 fuentes integradas como observaciones.
- 24,037,971 observaciones consolidadas.
- 148 registros agregados separados.
- 532 sensores en el catálogo espacial.
- Procedencia y estado de calidad conservados en el manifiesto.
