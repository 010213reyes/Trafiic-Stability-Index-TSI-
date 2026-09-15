# 2.10 Reproducibilidad y trazabilidad

## Estado

Completado.

## Actividades

- Registrar versiones de código, datos y configuración.
- Mantener manifiestos de ejecución.
- Usar rutas relativas.
- Documentar entradas y salidas de cada etapa.
- Dejar evidencia reproducible de cada etapa del pipeline.

## Implementación

El script de trazabilidad se ejecuta con:

```text
python docs/02_ingenieria_datos/10_reproducibilidad_trazabilidad/generar_reproducibilidad.py
```

Genera:

```text
docs/02_ingenieria_datos/10_reproducibilidad_trazabilidad/reproducibility_manifest.json
```

## Principios de trazabilidad aplicados

- Cada etapa genera un manifiesto propio.
- Las rutas se registran relativas al proyecto.
- Los outputs se documentan por fuente, etapa y destino.
- La carga a SQL y la limpieza final quedan vinculadas al mismo flujo principal.

## Artefactos de trazabilidad

```text
data/01_processed/pipeline/pipeline_manifest.json
data/01_processed/normalized/normalization_manifest.json
data/01_processed/quality/quality_report.json
data/02_clean/consolidated/consolidation_manifest.json
data/02_clean/dataset_clean/dataset_clean_manifest.json
docs/02_ingenieria_datos/sql/sql_load_manifest.json
```

## Entregable

Ejecución reproducible y trazabilidad completa del pipeline, con evidencia de la secuencia de transformación y salida final.

## Resultado

- El flujo queda documentado y verificable.
- Se conservan evidencias de cada etapa para auditoría y reproducción.
- La fase 2 queda cerrada con estructura y trazabilidad explícita.
