# Fase 04: Ciencia de datos

Esta fase transforma los hallazgos del analisis en variables, modelos y validaciones reproducibles para el TSI.

## Orden de trabajo

1. `00_planificacion`: objetivos, hipotesis y criterios de evaluacion.
2. `01_ingenieria_caracteristicas`: variables derivadas y ventanas temporales.
3. `02_modelado`: modelos candidatos y configuracion experimental.
4. `03_validacion`: particiones, metricas, sensibilidad y comparacion.
5. `04_interpretacion`: explicabilidad, limites y lectura operativa.
6. `05_resultados`: resultados reproducibles y decision del modelo.
7. `07_precolapso_horizontes`: proxy de deterioro anticipado y seleccion de horizonte.
8. `08_deteccion_anomalias`: baseline estadistico e Isolation Forest sobre alta frecuencia.
9. `09_formulacion_tsi`: formula, direcciones, escala y limites del TSI provisional.

## Dependencias

- La calidad y cobertura deben estar documentadas en `docs/03_analisis_datos/`.
- La carga SQL y su validacion forman parte de la base reproducible de esta fase.
- El EDA inicial y las pruebas exploratorias estan en `01_ingenieria_caracteristicas/01_EDA_Ciencia_Datos_Internacional.ipynb`.
- Las caracteristicas sin fuga se guardan en `data/04_model_output/features/tsi_daily_features.parquet`.
- La seleccion temporal de modelos esta en `02_modelado/01_Seleccion_Modelos_Internacional.ipynb`.
- La estabilidad por fuente esta en `03_validacion/01_Validacion_Modelos_Internacional.ipynb`.
- El experimento de deterioro anticipado esta en `07_precolapso_horizontes/`.
- La deteccion exploratoria de anomalias esta en `08_deteccion_anomalias/`.
- La formulacion matematica del TSI esta en `09_formulacion_tsi/`.
- Guadalajara se mantiene como ciudad objetivo para calibracion y validacion local.
- El indicador TSI provisional no se considera una etiqueta final ni un modelo validado.
