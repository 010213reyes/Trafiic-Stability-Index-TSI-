# Streamlit Dashboard TSI

Esta carpeta agrupa la capa de visualizacion del proyecto TSI. Aqui no va el pipeline de analisis ni los notebooks de construccion; solo la interfaz para consultar los resultados ya validados.

## Objetivo

Mostrar de forma resumida y accionable los elementos que realmente aportan al cierre del proyecto:

- comparacion entre Isolation Forest, Local Outlier Factor y DBSCAN
- retencion, ruido y estabilidad estructural
- distribucion del TSI propuesto
- conclusion final del algoritmo que aporta mejor señal
- graficas clave para lectura ejecutiva

## Fuentes de datos que lee la aplicacion actual

- `data/00_raw/external/international_sources_contract.json`
- `data/02_clean/external/international_clean_quality.json`
- `data/02_clean/consolidated/international_consolidation_manifest.json`
- `data/02_clean/consolidated/international_observations.parquet`
- Parquet CLEAN por fuente dentro de `data/02_clean/external/`

## Estructura actual

```text
streamlit_dashboard/
├── README.md
├── app.py
└── [imagenes reutilizadas desde data/03_algorithm_output/]
```

## Pantallas actuales dentro de la app

### 1. Avance del pipeline

- contexto del proyecto
- datos base usados
- estado actual del pipeline

### 2. Fuentes internacionales

- contrato de cada fuente
- estado de calidad CLEAN
- muestra acotada del dataset por ciudad

### 3. Fase SQL

- estado de SQL-01 a SQL-07
- artefactos y modelo de carga previsto

## Criterio de implementacion

La version actual de `app.py` usa pestañas para mantener el flujo de lectura dentro de un solo dashboard. Si mas adelante se requiere una version mas formal, se puede migrar a `pages/`, pero no es necesario para el cierre actual.

## Criterio de diseno

El dashboard debe mostrar solo lo que ayuda a decidir. Si una grafica no cambia la conclusion, no debe entrar.

## Despliegue en Streamlit Community Cloud

La aplicacion de produccion es `streamlit_dashboard/app.py`. En la configuracion de la app en Streamlit Community Cloud usa exactamente:

- **Repository:** `010213reyes/Trafiic-Stability-Index-TSI-`
- **Branch:** `main`
- **Main file path:** `streamlit_dashboard/app.py`

`testing/streamlit/app_testing.py` es una aplicacion separada y no debe configurarse como punto de entrada de produccion. Streamlit Community Cloud guarda esta seleccion fuera del repositorio; despues de cambiarla, pulsa **Redeploy**. Los siguientes pushes a `main` actualizaran esta nueva aplicacion.

La app carga muestras acotadas y metadatos versionados. Los datasets internacionales grandes estan excluidos de Git mediante `.gitignore`, por lo que no deben incorporarse al despliegue como archivos completos.

## Estado

Esta carpeta es la capa de presentacion de la nueva investigacion internacional. La app consume los artefactos de contrato, calidad y consolidacion sin reutilizar la interfaz legacy de algoritmos.

## Estado de uso

La app ya esta montada y enlazada con los artefactos relevantes. Lo que sigue es ajuste fino de contenido, jerarquia visual y texto de presentacion.
