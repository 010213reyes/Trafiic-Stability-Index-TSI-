# Fase 03: Analisis de datos

Esta fase transforma los datos limpios y consolidados en evidencia analitica para el proyecto TSI.

## Fuente de trabajo inicial

El analisis exploratorio comienza con:

`data/02_clean/consolidated/international_observations.parquet`

La base MySQL se incorporara despues de completar la carga controlada y validar sus conteos contra Parquet.

## Orden de trabajo

1. `00_planificacion`: preguntas, alcance y criterios de salida.
2. `01_eda`: distribuciones, nulos, frecuencias y resumen por fuente.
3. `02_calidad_cobertura`: completitud, cobertura temporal y granularidad.
4. `03_analisis_temporal`: comportamiento por fecha, hora y periodo.
5. `04_comparacion_fuentes`: comparacion metodologica entre ciudades y fuentes.
6. `05_indicador_tsi`: preparacion y calculo documentado del indicador TSI.
7. `06_validacion_sql`: comparacion entre Parquet y MySQL despues de la carga total.
8. `07_resultados`: hallazgos, tablas y conclusiones listas para comunicar.

## Regla metodologica

Las metricas de cada fuente conservan su semantica original. No se mezclan directamente `indice_congestion`, `intensidad`, `congestion_longitud_m` y `velocidad_sensor` sin una transformacion documentada.
