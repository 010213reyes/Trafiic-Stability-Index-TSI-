# Plan inicial de experimentos

## Objetivo

Evaluar modelos capaces de identificar deterioro operativo o condiciones de pre-colapso sin fuga temporal y con trazabilidad por fuente.

## Orden experimental

1. Baseline ingenuo temporal.
2. Regla interpretable basada en cambios y variabilidad.
3. Modelo lineal o logistico como referencia explicable.
4. Modelo de arboles para relaciones no lineales.
5. Modelos adicionales solo si mejoran la evidencia y pueden validarse temporalmente.

## Baseline

El baseline debe predecir el estado futuro usando el ultimo valor disponible o una regla de persistencia. Ningun modelo se considerara util si no supera este baseline fuera de muestra.

## Particion temporal

- Entrenamiento: periodo inicial.
- Validacion: periodo posterior separado.
- Prueba: periodo final no utilizado para decisiones.
- Nunca mezclar observaciones futuras en el entrenamiento de una observacion pasada.

Las proporciones exactas se definiran por fuente despues de revisar su cobertura temporal.

## Tareas candidatas

### Clasificacion

Predecir si ocurrira un deterioro operacional dentro de la ventana de 18 a 20 minutos. Requiere una etiqueta operacional validada.

### Regresion

Predecir el cambio futuro de la metrica dentro de la ventana definida. Requiere una unidad comparable y suficiente frecuencia temporal.

### Deteccion de cambios

Identificar transiciones anormales sin etiqueta supervisada. Debe evaluarse contra eventos documentados y no confundirse con ruido de muestreo.

## Metricas

- Clasificacion: precision, recall, F1, PR-AUC y matriz de confusion.
- Regresion: MAE, RMSE y error por fuente.
- Deteccion: tasa de alertas, anticipacion, falsos positivos y estabilidad temporal.

La metrica principal se elegira de acuerdo con el costo operativo de las falsas alarmas y de los eventos no detectados.

## Criterio de seleccion

Un modelo debe superar el baseline, mantenerse estable por periodo y fuente, ser interpretable para la decision TSI y conservar una ruta reproducible de datos, parametros y resultados.

## Bloqueos

- Definir la etiqueta de pre-colapso.
- Confirmar frecuencia y unidades.
- Validar SQL y la integridad del consolidado.
- Incorporar Guadalajara como validacion local.
