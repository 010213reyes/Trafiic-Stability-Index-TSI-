# Plan de inicio de ciencia de datos

## Objetivo

Evaluar si las variables de trafico disponibles permiten identificar estados de inestabilidad antes de un deterioro operativo, manteniendo trazabilidad por fuente y evitando fuga temporal.

## Hipotesis de trabajo

- H1: cambios sostenidos de velocidad, intensidad o congestion contienen senales de deterioro previo.
- H2: las caracteristicas temporales y de variabilidad aportan informacion adicional frente a una medicion puntual.
- H3: un modelo calibrado con datos internacionales requiere validacion separada con Guadalajara.

## Unidad de analisis

La unidad inicial sera una observacion temporal por ciudad, fuente y segmento cuando el segmento este disponible. La ventana temporal exacta se definira despues de revisar la granularidad de cada fuente.

## Ventana de anticipacion

La ventana de 18 a 20 minutos se conserva como hipotesis del proyecto, no como resultado confirmado. Solo se usara cuando exista cobertura temporal suficiente para construir etiquetas futuras sin fuga.

## Criterios de evaluacion

- separacion temporal entre entrenamiento y evaluacion;
- metricas adecuadas al tipo de tarea;
- estabilidad por fuente y periodo;
- interpretabilidad de variables;
- validacion local con Guadalajara;
- documentacion de falsos positivos, falsos negativos y limites.

## Estado de inicio experimental

1. La carga completa en MySQL y su control por conteos estan documentados.
2. Las unidades y semantica siguen separadas por fuente.
3. La primera tarea reproducible es pronosticar el TSI provisional del siguiente dia.
4. La etiqueta operacional de pre-colapso queda fuera de este experimento hasta contar con una regla validada.
5. Las caracteristicas temporales usan solo informacion pasada y conservan la fuente para evaluar estabilidad.

## Criterio para iniciar modelado

No se declara un modelo final: primero se registran baseline, validacion temporal, estabilidad por fuente y limites de interpretacion.
