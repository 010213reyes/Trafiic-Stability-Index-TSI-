# 2.5 Calidad y validación de datos

## Estado

Completado.

## Actividades

- Validar columnas obligatorias y tipos.
- Revisar fechas inválidas, duplicados y faltantes.
- Revisar rangos de las variables.
- Registrar filas aceptadas y rechazadas.

## Implementación

El validador se ejecuta con:

```text
python docs/02_ingenieria_datos/05_calidad_validacion/validar_calidad.py
```

Lee los Parquet de `data/01_processed/normalized/` por lotes y genera:

```text
data/01_processed/quality/quality_report.json
data/01_processed/quality/rejected_rows.csv
```

Las columnas obligatorias son `timestamp`, `ciudad`, `fuente`, `es_real`, `segmento_id` y `tipo_via`. Los catálogos de sensores no requieren `timestamp`; las variables operativas no disponibles permanecen nulas.

## Resultado

- 9 fuentes validadas.
- METR-LA, PEMS-BAY y sus catálogos de sensores: `valido`.
- Fuentes locales y sintéticas: `advertencia` por `tipo_via` no documentado.
- No se detectaron timestamps inválidos ni duplicados.
- Las advertencias quedan registradas sin eliminar registros ni asignar categorías no verificadas.

## Entregable

Reporte de calidad y reglas de validación ejecutables por fuente.
