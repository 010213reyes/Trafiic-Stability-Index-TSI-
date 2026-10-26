# Fase 05: MLOps

Esta fase convierte los resultados de ciencia de datos en un flujo reproducible, versionado y observable para calcular el TSI y sus señales asociadas.

## Objetivo

Definir y demostrar un ciclo operativo local que permita:

- identificar la versión del código, los datos, la configuración y el modelo;
- ejecutar inferencia sin depender de un notebook interactivo;
- validar entradas y salidas antes de publicar resultados;
- monitorear calidad de datos, distribución de variables y tasas de anomalías;
- integrar los resultados aprobados con la demostración Streamlit;
- documentar límites, evidencias y próximos pasos de despliegue.

Esta fase no declara un despliegue productivo ni una operación en tiempo real. La primera entrega es una demostración local reproducible.

## Orden de trabajo

1. `00_planificacion`: alcance operativo, contratos, criterios de aceptación y límites.
2. `01_versionado_modelo`: registro del modelo, parámetros, métricas, hashes y procedencia de datos.
3. `02_inferencia_reproducible`: carga del modelo versionado, validación de entradas y generación de predicciones.
4. `03_monitoreo`: controles de calidad, cambios de distribución, tasas de anomalías y desempeño cuando existan etiquetas.
5. `04_integracion_demo`: conexión del flujo operativo con la demostración Streamlit.
6. `05_resultados`: evidencias de ejecución, resultados consolidados, riesgos y decisión de cierre.

## Entradas principales

- Características: `data/04_model_output/features/tsi_daily_features.parquet`.
- Métricas y predicciones de evaluación: `data/04_model_output/modeling/`.
- Resultados de anomalías: `data/04_model_output/anomalies/`.
- Configuración y perfiles del TSI: `data/04_model_output/tsi/`.
- Código y notebooks de `docs/04_ciencia_datos/`.

## Salidas esperadas

- Modelo serializado y manifiesto de versión.
- Ejecución de inferencia reproducible con salida CSV o Parquet y metadatos JSON.
- Reporte de validaciones y monitoreo.
- Flujo demostrable desde entrada hasta resultado TSI/anomalía.
- Registro de limitaciones y requisitos para una futura operación productiva.

## Criterios de aceptación

- Una ejecución identifica explícitamente sus versiones y rutas de entrada.
- El modelo se carga sin reentrenar y produce resultados deterministas con los mismos insumos.
- Las entradas inválidas generan un error controlado antes de inferir.
- Los resultados incluyen fecha de ejecución, versión del modelo y fuente de datos.
- Los controles de monitoreo se ejecutan sin modificar los datos raw.
- Streamlit consume resultados generados por el flujo, sin contener lógica de entrenamiento.

## Dependencias y límites

- La definición del TSI sigue siendo provisional y específica por fuente y métrica.
- El proxy de deterioro no equivale a una etiqueta externa de colapso.
- Guadalajara permanece como objetivo futuro de calibración y validación local.
- El monitoreo de desempeño supervisado queda condicionado a disponer de etiquetas observadas.
