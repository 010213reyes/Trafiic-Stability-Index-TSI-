# Streamlit Dashboard TSI

Esta carpeta agrupa la capa de visualizacion del proyecto TSI. Aqui no va el pipeline de analisis ni los notebooks de construccion; solo la interfaz para consultar los resultados ya validados.

## Objetivo

Mostrar de forma resumida y accionable los elementos que realmente aportan al cierre del proyecto:

- comparacion entre Isolation Forest, Local Outlier Factor y DBSCAN
- retencion, ruido y estabilidad estructural
- distribucion del TSI propuesto
- conclusion final del algoritmo que aporta mejor señal
- graficas clave para lectura ejecutiva

## Fuentes de datos que deberia leer

- `data/02_clean/filtered_isolation_forest.csv`
- `data/02_clean/filtered_local_outlier_factor.csv`
- `data/02_clean/filtered_dbscan.csv`
- `data/03_algorithm_output/local_outlier_factor_summary.csv`
- `data/03_algorithm_output/dbscan_summary.csv`
- `data/03_algorithm_output/*` para graficas finales
- `data/02_clean/traffic_enriched.csv` para el TSI propuesto

## Estructura actual

```text
streamlit_dashboard/
├── README.md
├── app.py
└── [imagenes reutilizadas desde data/03_algorithm_output/]
```

## Pantallas sugeridas dentro de la app

### 1. Resumen

- contexto del proyecto
- datos base usados
- estado actual del pipeline

### 2. Comparacion de algoritmos

- tabla de retencion
- ruido/outliers
- estabilidad estructural
- lectura final por algoritmo

### 3. TSI final

- formula propuesta
- distribucion del indice
- correlacion con la version actual

### 4. Conclusiones

- por que DBSCAN queda como validacion estructural principal
- que hace Isolation Forest
- que hace LOF
- como se interpreta el cierre del proyecto

## Criterio de implementacion

La version actual de `app.py` usa pestañas para mantener el flujo de lectura dentro de un solo dashboard. Si mas adelante se requiere una version mas formal, se puede migrar a `pages/`, pero no es necesario para el cierre actual.

## Criterio de diseno

El dashboard debe mostrar solo lo que ayuda a decidir. Si una grafica no cambia la conclusion, no debe entrar.

## Estado

Esta carpeta es la capa de presentacion del proyecto. La app ya consume los artefactos generados por los notebooks y sirve para contar la historia final del proyecto sin ruido intermedio.

## Lectura final que debe comunicar

- El proyecto si cumple como flujo completo de data science aplicada.
- La investigacion esta cerrada con una hipotesis, una metrica propia y una comparacion entre algoritmos.
- La señal principal queda en DBSCAN como validacion estructural.
- El dashboard no debe mostrar todo; debe mostrar solo lo que sostiene la conclusion.
