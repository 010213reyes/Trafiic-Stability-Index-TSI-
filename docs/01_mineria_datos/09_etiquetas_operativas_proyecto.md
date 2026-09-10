# Etiquetas operativas del proyecto punta a punta

Este documento define las etiquetas que utilizará la implementación nueva del TSI. No reemplaza las definiciones exploratorias de la investigación inicial.

## Evento objetivo: congestión

Una observación se considera parte de un evento de congestión cuando el comportamiento del segmento se encuentra claramente por debajo de su patrón esperado para la misma ciudad, sensor o segmento y franja temporal.

La etiqueta se construirá en dos niveles:

### Nivel 1: fuentes con velocidad

Para METR-LA, PEMS-BAY y fuentes que solo tengan velocidad:

- calcular una línea base por `ciudad`, `segmento_id`, día de la semana y franja horaria;
- comparar la velocidad observada contra esa línea base;
- marcar congestión cuando la velocidad permanezca bajo el umbral relativo definido durante al menos dos observaciones consecutivas;
- conservar el umbral utilizado y el tamaño de la ventana en los metadatos.

### Nivel 2: fuentes multivariable

Cuando exista flujo, ocupación, densidad o tiempo de viaje:

- combinar la velocidad con las variables disponibles;
- verificar que la señal represente pérdida de eficiencia y no solo una lectura aislada;
- conservar la regla específica de la fuente, ciudad y tipo de vía.

No se aplicará un umbral absoluto idéntico a todas las ciudades o sensores.

## Etiqueta de pre-colapso

`pre_colapso = 1` cuando, antes de una congestión etiquetada, exista una secuencia temporal de deterioro observable en las variables disponibles.

La secuencia debe cumplir:

- ocurrir antes del inicio del evento objetivo;
- mostrar deterioro sostenido o aumento de inestabilidad;
- no utilizar observaciones posteriores al inicio de la congestión;
- conservar el inicio del evento, el segmento y la fuente;
- permitir reconstruir qué información estaba disponible en cada instante.

Cuando solo exista velocidad, el deterioro se medirá con cambios relativos frente a la línea base y variación entre observaciones. Con variables adicionales se incorporarán señales de flujo, ocupación, densidad o tiempo de viaje sin inventar valores faltantes.

## Horizonte de anticipación

La hipótesis operativa se evaluará con un horizonte de **18–20 minutos**.

Para series con intervalo de 5 minutos:

- las características se calculan hasta el instante `t`;
- el evento objetivo debe iniciar entre `t + 18` y `t + 20` minutos;
- solo se utilizarán datos disponibles hasta `t`;
- se registrará si el evento quedó dentro, antes o después del horizonte.

Para series con otra frecuencia, el horizonte se expresará en minutos y se convertirá al número de observaciones correspondiente, sin afirmar una precisión superior a la resolución disponible.

## Estados de etiqueta

| Campo | Valores | Significado |
|---|---|---|
| `congestion_event` | `0`, `1` | Existe o no un evento objetivo en el horizonte |
| `pre_colapso` | `0`, `1` | Existe o no deterioro previo identificable |
| `event_start` | datetime o nulo | Inicio del evento objetivo |
| `horizon_minutes` | numérico | Distancia entre `t` y el inicio del evento |
| `label_status` | `valid`, `insufficient_history`, `insufficient_resolution`, `ambiguous` | Estado de construcción de la etiqueta |

## Exclusiones

- No se etiquetan como congestión los valores extremos aislados sin continuidad.
- No se usa la etiqueta `anomalia` de los datos sintéticos como verdad de campo.
- No se mezclan eventos de autopista con eventos de avenida urbana sin conservar `tipo_via`.
- No se calculan etiquetas en filas con timestamp inválido o segmento no identificable.

## Validación de las etiquetas

Antes de entrenar se verificará:

1. número de eventos por ciudad y fuente;
2. duración de cada evento;
3. distribución de horizontes;
4. proporción de clases;
5. ausencia de solapamiento temporal entre entrenamiento y prueba;
6. ausencia de fuga de información futura.

La capacidad anticipatoria se reportará por fuente y ciudad, con Guadalajara como referencia local cuando exista una serie suficiente.