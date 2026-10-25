# Protocolo de etiqueta de deterioro anticipado

## Decision metodologica

La investigacion internacional no dispone de un registro externo de incidentes sincronizado con METR-LA y PEMS-BAY. Por tanto, la etiqueta no se presenta como verdad de campo ni como prueba definitiva de pre-colapso. Se denomina:

```text
proxy_deterioro_anticipado
```

El proxy permite evaluar si las señales disponibles contienen informacion sobre una degradacion futura, manteniendo la limitacion visible.

## Unidad de analisis

Una observacion de una serie de velocidad agregada a partir de sensores de una fuente y un timestamp de 5 minutos.

La velocidad de red se calcula como la mediana de los sensores disponibles en cada timestamp. La mediana reduce la influencia de un sensor aislado, pero no equivale a una medicion de un corredor concreto.

## Definicion operacional

Para un instante `t`, un horizonte `h` y un umbral `delta`:

```text
baseline(t) = mediana de la velocidad en los tres intervalos anteriores

proxy_deterioro(t, h, delta) = 1 si
velocidad(t + h) <= baseline(t) * (1 - delta)
```

La etiqueta se calcula usando el futuro solo para construir el objetivo. Ninguna variable futura entra como predictor.

Se prueban:

- horizontes: 5, 10, 15, 20, 30 y 60 minutos;
- umbrales de deterioro: 10%, 15%, 20%, 25% y 30%;
- persistencia: se registra si la caida se mantiene durante al menos dos intervalos.

## Criterios de calidad de etiqueta

Una combinacion fuente-horizonte-umbral es utilizable para un experimento si cumple:

1. intervalo temporal mediano de 5 minutos;
2. cero timestamps invalidos;
3. ausencia de fuga temporal;
4. dos clases en entrenamiento, validacion y prueba;
5. al menos diez eventos positivos en prueba;
6. eventos positivos y negativos en cada particion;
7. persistencia del deterioro reportada, no asumida.

Las combinaciones que no cumplen se marcan como `insuficiente_evidencia` y no se fuerzan al modelo.

## Resultado actual

Con los datos disponibles, el horizonte de 5 minutos obtuvo la mejor PR-AUC media bajo esta definicion exploratoria y permanecio como ganador al variar el umbral de 10% a 30%. Esto no demuestra que cinco minutos sea un tiempo universal de prevencion.

PEMS-BAY presenta pocas combinaciones con suficientes eventos positivos. METR-LA ofrece mayor soporte estadistico para el experimento inicial.

## Como justificarlo en la investigacion

La afirmacion defendible es:

> Se construyo un proxy reproducible de deterioro anticipado a partir de la caida futura de velocidad respecto a una linea base temporal. La comparacion de horizontes mostro que cinco minutos produjo la mejor señal predictiva en las fuentes y combinaciones con soporte suficiente. El resultado es exploratorio y no equivale a una etiqueta de incidente ni a una validacion de pre-colapso real.

No debe afirmarse:

- que todos los colapsos pueden predecirse cinco minutos antes;
- que la etiqueta representa accidentes o incidentes reales;
- que el resultado se transfiere automaticamente a Guadalajara;
- que un valor p demuestra causalidad.

## Validacion posterior necesaria

Para elevar el proxy a etiqueta validada se requiere sincronizar la velocidad con registros de incidentes, cierres, accidentes o eventos de congestion de una fuente externa. Una muestra revisada por dos expertos debe alcanzar un acuerdo documentado, idealmente con Cohen kappa, antes de usar la etiqueta como verdad supervisada.
