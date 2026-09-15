# 2.11 Validación final de la tubería

## Estado

Completado.

## Actividades

- Ejecutar el pipeline completo desde las entradas definidas.
- Verificar todas las salidas esperadas.
- Confirmar que los datos raw no fueron modificados.
- Revisar calidad, trazabilidad y carga SQL.
- Validar la continuidad entre Fase 2 y Fase 3.

## Implementación

La validación puede ejecutarse con:

```text
python docs/02_ingenieria_datos/11_validacion_final_tuberia/validar_tuberia.py
```

La verificación comprueba que existan las rutas clave:

```text
- data/00_raw/
- data/01_processed/pipeline/pipeline_manifest.json
- data/01_processed/normalized/normalization_manifest.json
- data/01_processed/quality/quality_report.json
- data/02_clean/consolidated/consolidation_manifest.json
- data/02_clean/dataset_clean/dataset_clean_manifest.json
- data/02_clean/dataset_clean/clean_observations.parquet
- docs/02_ingenieria_datos/sql/tsi_stage.sqlite
- docs/02_ingenieria_datos/sql/sql_load_manifest.json
```

## Entregable

Pipeline de ingeniería de datos validado y listo para la Fase 3.

## Resultado

- El pipeline mantiene trazabilidad y estructura por etapas.
- Los artefactos de raw, processed, clean y SQL quedaron presentes.
- La fase 2 culmina con una base de trabajo lista para la Fase 3 de modelado y SQL.
