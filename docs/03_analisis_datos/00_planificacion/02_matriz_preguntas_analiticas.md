# Matriz de preguntas analiticas

| ID | Pregunta | Campos principales | Herramienta inicial | Evidencia esperada |
|---|---|---|---|---|
| P01 | Que ciudades y fuentes estan representadas? | `ciudad`, `fuente` | Python/Jupyter/SQL | Conteos por ciudad y fuente |
| P02 | Que cobertura temporal tiene cada fuente? | `timestamp`, `ciudad`, `fuente` | Python/Jupyter/SQL | Fecha minima, maxima y dias observados |
| P03 | Cual es la granularidad de observacion? | `timestamp`, `periodo_integracion_min` | Python/Jupyter | Intervalos y frecuencia por fuente |
| P04 | Que tan completos son los registros? | Todos los campos, `calidad_registro` | Python/SQL | Porcentaje de nulos y calidad |
| P05 | Existen duplicados o registros inconsistentes? | `timestamp`, `ciudad`, `fuente`, `segmento_id` | Python/SQL | Duplicados y reglas incumplidas |
| P06 | Como se distribuye la metrica principal? | `metrica_principal`, `valor_principal`, `valor_fuente` | Python/Jupyter/SQL | Estadisticos, cuantiles y visualizaciones |
| P07 | Que diferencias existen entre fuentes? | `fuente`, metricas especificas | Python/Jupyter/SQL | Comparacion con semantica documentada |
| P08 | Que patrones temporales aparecen? | `timestamp`, `valor_principal` | Python/Jupyter | Resumen por hora, dia y periodo |
| P09 | Que observaciones deben excluirse del analisis? | `es_real`, `calidad_registro`, rangos | Python/SQL | Reglas de inclusion y exclusion |
| P10 | Que variables pueden alimentar el TSI? | Metricas normalizadas y cobertura | Python/Jupyter | Candidatos con justificacion |

## Criterio de respuesta

Cada pregunta debe tener una salida reproducible, indicar la fuente de datos y conservar la unidad de medida. Las conclusiones comparativas requieren revisar primero cobertura, calidad y semantica.
