# Criterios de comparabilidad

## Unidad de comparacion

La unidad base sera una observacion identificada por `timestamp`, `ciudad`, `fuente` y `segmento_id` cuando este disponible.

## Reglas

1. Comparar solo registros con fechas y periodos de cobertura conocidos.
2. Separar fuentes reales y sinteticas mediante `es_real`.
3. Conservar `metrica_principal` y `valor_principal` como referencia comun solo cuando su semantica este documentada.
4. Mantener separadas las metricas especificas: `indice_congestion`, `intensidad_fuente`, `congestion_longitud_m` y `vmed_fuente` no son intercambiables automaticamente.
5. No comparar valores sin verificar unidad, sentido y rango esperado.
6. Reportar por separado diferencias de cobertura, frecuencia, sensores y metodo de recoleccion.
7. Aplicar filtros de calidad antes de estimar estadisticos o construir el indicador TSI.
8. Documentar cualquier normalizacion, agregacion temporal o imputacion.

## Orden de decision

Antes de afirmar que dos ciudades o fuentes son comparables, se debe comprobar:

- misma definicion de la metrica;
- unidad compatible;
- ventana temporal compatible;
- granularidad comparable;
- calidad suficiente;
- ausencia de sesgo evidente por cobertura.

## Guadalajara

Guadalajara se mantiene como ciudad objetivo para calibracion y validacion del TSI. Las comparaciones internacionales sirven como referencia metodologica y no sustituyen la validacion local.
