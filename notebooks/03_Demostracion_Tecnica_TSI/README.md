# Demostracion Tecnica TSI

Esta carpeta contiene un solo notebook curado para mostrar el flujo tecnico esencial del proyecto TSI sin repetir todo el pipeline de investigacion.

## Proposito

El notebook de esta carpeta esta pensado para una lectura tecnica completa y breve:

1. Cargar los artefactos finales ya generados por los notebooks principales.
2. Comparar Isolation Forest, Local Outlier Factor y DBSCAN con las mismas metricas.
3. Construir y revisar el TSI propuesto.
4. Mostrar solo las visualizaciones que aportan a la narrativa final.

## Archivo principal

- `01_Demostracion_Tecnica_TSI.ipynb`

## Artefactos que consume

- `data/02_clean/traffic_enriched.csv`
- `data/02_clean/filtered_isolation_forest.csv`
- `data/02_clean/filtered_local_outlier_factor.csv`
- `data/02_clean/filtered_dbscan.csv`
- `data/03_algorithm_output/local_outlier_factor_summary.csv`
- `data/03_algorithm_output/dbscan_summary.csv`
- `data/03_algorithm_output/02_algorithm_ranking.png`
- `data/03_algorithm_output/01_algorithm_comparison.png`
- `data/03_algorithm_output/10_variability_comparison.png`
- `data/03_algorithm_output/11_isolation_forest_summary.png`
- `data/03_algorithm_output/12_isolation_forest_boxplots.png`
- `data/03_algorithm_output/local_outlier_factor_pca.png`
- `data/03_algorithm_output/dbscan_pca_clusters.png`
- `data/03_algorithm_output/dbscan_kdistance_curve.png`
- `data/03_algorithm_output/dbscan_cluster_sizes.png`

## Estructura

```text
notebooks/03_Demostracion_Tecnica_TSI/
├── README.md
└── 01_Demostracion_Tecnica_TSI.ipynb
```

## Uso recomendado

Abrir el notebook principal y ejecutar las celdas en orden. El notebook esta organizado para que cada bloque cuente un paso del proyecto:

- contexto y carga
- comparacion de algoritmos
- revision del TSI
- señal estructural de DBSCAN
- cierre tecnico
