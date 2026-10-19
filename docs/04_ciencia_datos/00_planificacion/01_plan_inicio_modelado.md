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

## Bloqueos actuales

1. Validar la carga completa en MySQL.
2. Confirmar unidades y semantica de las metricas.
3. Definir una etiqueta operacional de inestabilidad.
4. Elegir caracteristicas sin mezclar escalas incompatibles.

## Criterio para iniciar modelado

No se entrenara un modelo final hasta cerrar los cuatro bloqueos y registrar una particion temporal reproducible.
