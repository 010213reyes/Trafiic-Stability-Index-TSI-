# 2.9 Pipeline de carga hacia SQL

## Estado

En desarrollo.

## Actividades

- Implementar la carga del dataset validado.
- Registrar ejecuciones y resultados de carga.
- Controlar duplicados y errores.
- Probar la lectura de los datos cargados.
- Dejar la base SQLite preparada para la Fase 3.

## Implementación

El script de carga se ejecuta con:

```text
python docs/02_ingenieria_datos/09_pipeline_carga_sql/cargar_sql.py
```

La carga se dirige a:

```text
docs/02_ingenieria_datos/sql/tsi_stage.sqlite
```

El manifiesto de ejecución queda en:

```text
docs/02_ingenieria_datos/sql/sql_load_manifest.json
```

### Tablas creadas

```text
- fact_observaciones
- dim_segmento
- dim_fuente
- fact_aggregates
```

## Entregable

Carga reproducible hacia la base SQL con tablas fact/dimension y trazabilidad de la ejecución.

## Resultado

- La carga del dataset limpio queda preparada para la etapa de SQL.
- La base local es el punto de entrada para consultas analíticas y validación posterior.
