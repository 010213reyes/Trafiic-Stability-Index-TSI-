# 2.3 Pipeline RAW -> PROCESSED

## Estado



## Actividades

- Leer las fuentes originales.
- Registrar la ejecución.
- Generar archivos procesados sin modificar `data/00_raw/`.
- Mantener la procedencia de cada registro.

## Implementación

El pipeline se ejecuta con:

```text
python docs/02_ingenieria_datos/03_pipeline_raw_processed/pipeline_raw_processed.py
```

Las nueve fuentes se leen desde `data/00_raw/` y se escriben como Parquet en:

```text
data/01_processed/pipeline/
```

El manifiesto de ejecución se genera en:

```text
data/01_processed/pipeline/pipeline_manifest.json
```

## Entregable

Pipeline de ingesta y procesamiento inicial con procedencia, conteos y cobertura temporal por fuente.
