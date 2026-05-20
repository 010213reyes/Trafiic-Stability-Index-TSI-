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

## Estructura recomendada

```text
streamlit_dashboard/
├── README.md
├── app.py
├── pages/
│   ├── 1_Resumen.py
│   ├── 2_Comparacion_Algoritmos.py
│   ├── 3_TSI_Final.py
│   └── 4_Conclusiones.py
└── assets/
    └── [imagenes o recursos estaticos]
```

## Pantallas sugeridas

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

## Criterio de diseno

El dashboard debe mostrar solo lo que ayuda a decidir. Si una grafica no cambia la conclusion, no debe entrar.

## Estado

Esta carpeta es la capa de presentacion del proyecto. El proximo paso es construir `app.py` y las paginas de Streamlit a partir de los artefactos ya generados por los notebooks.
