# 2.7 Dataset CLEAN listo para análisis

## Estado

Completado.

## Actividades

- Congelar la versión limpia del dataset.
- Confirmar el contrato común.
- Confirmar cobertura temporal y espacial.
- Separar datos reales, externos, locales y sintéticos.
- Dejar la salida lista para preparación SQL.

## Implementación

El proceso se ejecuta con:

```text
python docs/02_ingenieria_datos/07_dataset_clean/generar_dataset_clean.py
```

Las salidas se escriben en:

```text
data/02_clean/dataset_clean/
```

Archivos generados:

```text
data/02_clean/dataset_clean/clean_observations.parquet
data/02_clean/dataset_clean/clean_aggregates.parquet
data/02_clean/dataset_clean/clean_sensor_catalog.parquet
data/02_clean/dataset_clean/dataset_clean_manifest.json
```

La versión limpia conserva solo registros con la firma mínima requerida para análisis: `timestamp`, `ciudad`, `fuente`, `es_real`, `segmento_id` y `tipo_via`. Los registros no válidos se excluyen de la entrega final.

## Entregable

Dataset clean listo para análisis y modelado posterior, con particiones lógicas para observaciones, agregados y catálogo espacial.

## Resultado

- Observaciones limpias generadas.
- Agregados separados en archivo limpio.
- Catálogo de sensores validado y separado.
- Manifesto de generación y trazabilidad registrado.
