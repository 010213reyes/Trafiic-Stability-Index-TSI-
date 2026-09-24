# Reporte de fallas en el backend de testing

## Estado

Reporte inicial. Las fallas permanecen sin corregir para documentar el ciclo de pruebas de la materia Laboratorio Abierto.

## Alcance

- Herramienta evaluada: `testing/backend/check_backend.py`.
- Tipo de prueba: diagnóstico funcional y estático por consola.
- Fecha: 2026-09-24.
- Entorno: Python local con `.venv`.
- Investigación evaluada: investigación anterior del proyecto TSI, utilizada como línea base técnica.
- Estado del backend nuevo: todavía en construcción; no evaluado como backend completo.

## Nota sobre la investigación evaluada

El diagnóstico utiliza los datos, archivos procesados y resultados de algoritmos de la investigación anterior porque es la versión que cuenta con artefactos completos para realizar pruebas.

Estos resultados sirven como referencia para diseñar y transferir validaciones al backend de la nueva investigación. No se consideran automáticamente resultados de la nueva investigación.

### F-001: Archivos processed declarados en el inventario no encontrados

- **Sección:** Integridad del pipeline.
- **Cómo reproducir:** ejecutar `python testing/backend/check_backend.py` y revisar la validación de artefactos.
- **Resultado esperado:** todos los archivos registrados en el inventario deben existir en sus rutas declaradas.
- **Resultado observado:** no se encontraron `traffic_data_normalized.parquet`, `scraped_traffic_normalized.parquet`, `crowdsourcing_normalized.parquet`, `crowdsourcing_aggregated_normalized.parquet` y `synthetic_traffic_normalized.parquet`.
- **Impacto:** alto; no es posible comprobar completamente la transición de raw a processed.
- **Estado:** pendiente.

### F-002: Archivos procesados de metadatos de sensores no encontrados

- **Sección:** Fuentes externas.
- **Cómo reproducir:** ejecutar el diagnóstico y revisar las rutas de `metr_la_sensor_locations` y `pems_bay_sensor_locations`.
- **Resultado esperado:** deben existir los archivos procesados de metadatos en `data/01_processed/external/`.
- **Resultado observado:** no se encontraron los archivos procesados de metadatos de sensores.
- **Impacto:** medio; no se puede comprobar la trazabilidad espacial de los sensores externos.
- **Estado:** pendiente.

### F-003: Archivos clean de metadatos de sensores no encontrados

- **Sección:** Fuentes externas.
- **Cómo reproducir:** ejecutar el diagnóstico y revisar las rutas clean registradas para los metadatos.
- **Resultado esperado:** deben existir los archivos clean de metadatos en `data/02_clean/external/`.
- **Resultado observado:** no se encontraron las salidas clean de `metr_la_sensor_locations` y `pems_bay_sensor_locations`.
- **Impacto:** medio; la etapa clean de los metadatos externos no puede ser validada.
- **Estado:** pendiente.

### F-004: El inventario declara una cantidad incorrecta de sensores PEMS-BAY

- **Sección:** Validación de registros.
- **Cómo reproducir:** comparar el campo `rows` del inventario con el número real de filas de `pems_bay_sensor_locations`.
- **Resultado esperado:** la cantidad declarada debe coincidir con la cantidad real del archivo.
- **Resultado observado:** el inventario declara 325 registros, pero el archivo contiene 324.
- **Impacto:** medio; existe una inconsistencia entre la documentación y el archivo utilizado.
- **Estado:** pendiente.

### F-005: Las columnas declaradas de PEMS-BAY no coinciden con el archivo real

- **Sección:** Validación de esquema.
- **Cómo reproducir:** comparar `column_names` del inventario con las columnas reales de `pems_bay_sensor_locations`.
- **Resultado esperado:** las columnas documentadas deben coincidir con las columnas del archivo.
- **Resultado observado:** el diagnóstico detecta una diferencia entre el esquema declarado y el esquema real.
- **Impacto:** medio; el backend no puede garantizar que utiliza el esquema documentado.
- **Estado:** pendiente.

### F-006: El pipeline completo todavía no se ejecuta durante el diagnóstico

- **Sección:** Ejecución del pipeline.
- **Hallazgo:** `check_backend.py` valida artefactos existentes, pero no reconstruye el flujo completo desde raw hasta clean.
- **Resultado esperado:** ejecutar el pipeline en un entorno temporal y verificar sus salidas.
- **Resultado observado:** solamente se comprueba la existencia, lectura y consistencia básica de resultados ya generados.
- **Impacto:** alto; no se confirma la reproducibilidad del procesamiento.
- **Estado:** pendiente.

### F-007: No se valida la reproducibilidad de los algoritmos

- **Sección:** Algoritmos y modelos.
- **Hallazgo:** el diagnóstico compara archivos filtrados con sus resúmenes, pero no vuelve a ejecutar Isolation Forest, LOF ni DBSCAN.
- **Resultado esperado:** repetir la ejecución con la misma configuración y comparar resultados.
- **Resultado observado:** se validan salidas guardadas, no una nueva ejecución del entrenamiento.
- **Impacto:** alto; no se puede confirmar que los resultados sean reproducibles.
- **Estado:** pendiente.

### F-008: Isolation Forest no cuenta con archivo resumen validado

- **Sección:** Resultados de algoritmos.
- **Hallazgo:** se verifica que `filtered_isolation_forest.csv` tiene menos registros que la base, pero no existe un resumen equivalente incluido en la validación.
- **Resultado esperado:** contar con un resumen que indique registros totales, retenidos, anomalías y parámetros.
- **Resultado observado:** solo se valida la relación básica entre el dataset base y la salida.
- **Impacto:** medio; la evidencia de Isolation Forest es menos completa que la de LOF y DBSCAN.
- **Estado:** pendiente.

### F-009: No se valida la calidad interna completa de los datos

- **Sección:** Calidad de datos.
- **Hallazgo:** el diagnóstico comprueba archivos, filas y columnas, pero no valida de forma completa rangos, tipos, duplicados y valores negativos en todos los artefactos.
- **Resultado esperado:** aplicar reglas de calidad específicas para cada dataset.
- **Resultado observado:** la validación actual es estructural y básica.
- **Impacto:** medio; podrían existir valores inválidos sin ser reportados.
- **Estado:** pendiente.

### F-010: No existe una separación automatizada entre artefactos históricos y resultados nuevos

- **Sección:** Trazabilidad de investigaciones.
- **Hallazgo:** el diagnóstico trabaja sobre las rutas actuales, pero no identifica automáticamente si un artefacto pertenece a la investigación anterior o a la nueva.
- **Resultado esperado:** mostrar el origen, versión y fecha de cada artefacto evaluado.
- **Resultado observado:** los archivos históricos se utilizan como línea base sin un registro de versionado automatizado.
- **Impacto:** medio; puede confundirse una referencia histórica con un resultado nuevo.
- **Estado:** pendiente.

## Resumen

| Grupo | Cantidad | Estado |
|---|---:|---|
| Fallas de integridad de datos | 5 | Sin corregir |
| Limitaciones del diagnóstico | 5 | Pendiente de ampliación |
| Total documentado | 10 | Pendiente de priorización |

## Regla de trabajo

Este reporte documenta los problemas encontrados y las limitaciones actuales del diagnóstico. No se aplican correcciones en esta etapa. La siguiente etapa será priorizar los fallos, reproducirlos con evidencia y repararlos uno por uno.
