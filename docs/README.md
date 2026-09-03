# Documentación del proyecto TSI

Esta carpeta concentra la documentación de la solución de inteligencia artificial de punta a punta. Aquí se registran decisiones, diseños, resultados y criterios de cada fase.

## Organización

- `00_arq_y_decisiones/`: arquitectura general, alcance, decisiones técnicas y criterios del proyecto.
- `01_mineria_datos/`: fuentes, definiciones, calidad inicial, sesgos y hallazgos de minería de datos.
- `02_ingenieria_datos/`: pipeline, transformaciones, validaciones y flujos de datos.
- `02_ingenieria_datos/sql/`: modelo relacional, tablas, relaciones, consultas y decisiones de la base SQL.
- `03_analisis_datos/`: análisis exploratorio, indicadores, visualizaciones e interpretaciones.
- `04_ciencia_datos/`: características, experimentos, modelos, métricas y validación del TSI.
- `05_mlops/`: versionado, automatización, pruebas, despliegue y monitoreo.
- `06_interfaz_minima/`: alcance, flujo de usuario, vistas y decisiones de UX/UI para Streamlit.

## Orden de trabajo

1. Arquitectura y decisiones.
2. Minería de datos.
3. Ingeniería de datos y SQL.
4. Análisis de datos.
5. Ciencia de datos y machine learning.
6. Interfaz mínima.
7. MLOps y despliegue.

La primera demostración será local con Streamlit. El despliegue en la nube se planificará después de estabilizar los datos, la base SQL, el modelo y la interfaz.
