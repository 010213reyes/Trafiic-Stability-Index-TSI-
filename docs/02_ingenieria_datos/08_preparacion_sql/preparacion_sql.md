# 2.8 Preparación de datos para SQL

## Estado

Completado.

## Actividades

- Definir las entidades que pasarán a SQL.
- Preparar claves e identificadores.
- Separar catálogos y observaciones.
- Revisar tipos compatibles con la base de datos.
- Dejar el manifiesto de preparación listo para la Fase 3.

## Implementación

El proceso se ejecuta con:

```text
python docs/02_ingenieria_datos/08_preparacion_sql/preparar_sql.py
```

Estas son las entidades que quedan preparadas para SQL:

```text
- fact_observaciones
- dim_segmento
- dim_fuente
- dim_catalogo_sensores
- fact_aggregates
```

La salida se genera en:

```text
data/02_clean/dataset_clean/sql_preparation_manifest.json
```

### Regla de modelado propuesta

- `fact_observaciones` representa la tabla principal de mediciones temporales.
- `dim_segmento` contiene dimensiones de avenida, ruta o segmento.
- `dim_fuente` registra la procedencia de la observación.
- `dim_catalogo_sensores` mantiene metadatos espaciales.
- `fact_aggregates` queda disponible para cálculos agregados y reportes.

## Entregable

Dataset y especificación de carga preparados para la Fase 3, con tipos SQL sugeridos y entidades del modelo lógico definidas.

## Resultado

- El conjunto limpio de observaciones queda listo para cargar en SQL.
- La estructura lógica está separada por hechos y dimensiones.
- Se conserva la trazabilidad de origen y el contrato del dataset limpio.
