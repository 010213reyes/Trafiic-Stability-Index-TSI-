# Protocolo inicial de validacion

## Objetivo

Medir si un modelo generaliza hacia periodos futuros y si sus resultados son estables entre fuentes, sin utilizar informacion posterior al instante de prediccion.

## Particion temporal

Cada fuente debe ordenarse por `timestamp` y dividirse en tres bloques cronologicos:

1. entrenamiento: periodo inicial;
2. validacion: periodo posterior para seleccionar parametros;
3. prueba: periodo final reservado para la medicion definitiva.

No se deben barajar observaciones entre bloques.

## Controles contra fuga

- Las ventanas moviles solo utilizan observaciones anteriores o del mismo instante.
- Las etiquetas futuras no pueden aparecer como caracteristicas.
- Los limites de normalizacion se calculan usando entrenamiento y se aplican sin recalcular en validacion o prueba.
- Las imputaciones se ajustan en entrenamiento y se reutilizan sin aprender del futuro.
- Los segmentos y fuentes se mantienen identificables en cada salida.

## Evaluacion por nivel

Los resultados deben reportarse en cuatro niveles:

- global, para conocer el comportamiento agregado;
- por fuente, para detectar dependencia del proveedor;
- por periodo, para medir estabilidad temporal;
- Guadalajara, como validacion local objetivo.

## Metricas

### Clasificacion

- precision;
- recall;
- F1;
- PR-AUC;
- matriz de confusion;
- anticipacion media de la alerta.

### Regresion

- MAE;
- RMSE;
- error mediano absoluto;
- error por fuente y periodo.

### Alertas

- tasa de falsas alarmas;
- eventos no detectados;
- tiempo medio de anticipacion;
- estabilidad de la tasa de alertas.

## Comparacion

Todo modelo debe compararse contra el baseline temporal definido en `02_modelado/01_plan_experimentos.md`. Una mejora promedio no es suficiente si oculta deterioro severo en una fuente o en Guadalajara.

## Criterio de aprobacion

Un modelo solo pasa a interpretacion si supera el baseline en la metrica principal, mantiene desempeño razonable por fuente y periodo, no presenta fuga temporal y conserva trazabilidad de datos, parametros y version.

## Bloqueos

- Definir la etiqueta de pre-colapso.
- Confirmar la ventana de anticipacion real por fuente.
- Incorporar datos de Guadalajara con el mismo contrato analitico.
