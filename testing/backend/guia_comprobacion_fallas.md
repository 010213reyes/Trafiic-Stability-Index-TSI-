# Guia para encontrar fallas del backend

## 1. Objetivo

Comprobar las fallas del backend de testing, registrar evidencia y dejar cada incidencia lista para una etapa posterior de correccion.

Herramienta evaluada:

```text
testing/backend/check_backend.py
```

Investigacion evaluada:

```text
Investigacion anterior del proyecto TSI
```

La investigacion anterior se utiliza como linea base porque cuenta con datos, artefactos procesados y resultados de algoritmos disponibles. Esto no significa que sus resultados representen automaticamente a la nueva investigacion.

No se modifica durante esta etapa:

- Datos oficiales del proyecto.
- Resultados historicos.
- Algoritmos existentes.
- Dashboard principal.
- Backend nuevo en construccion.

## 2. Ejecutar el diagnostico

Desde la raiz del proyecto:

```powershell
.\.venv\Scripts\python.exe testing/backend/check_backend.py
```

Tambien puede ejecutarse con:

```powershell
python testing/backend/check_backend.py
```

El resultado utiliza los estados:

```text
[OK] Comprobacion correcta
[FALLO] Se encontro una inconsistencia
```

El comando debe terminar con codigo `0` si todas las comprobaciones pasan. Si existe una falla, debe terminar con un codigo diferente de `0`.

## 3. Metodo de comprobacion

Para cada prueba:

1. Leer el ID de la falla en `fallas_encontradas.md`.
2. Ejecutar el diagnostico desde la raiz del proyecto.
3. Comparar el resultado observado con el resultado esperado.
4. Registrar la salida de PowerShell como evidencia.
5. Registrar fecha, version de Python y entorno utilizado.
6. Marcar la falla como `reproducida`.
7. Corregir en una etapa posterior.
8. Ejecutar nuevamente el diagnostico.

## 4. Formato de evidencia

Usar esta ficha para cada falla:

```text
ID:
Fecha:
Comando ejecutado:
Entorno:
Pasos realizados:
Resultado esperado:
Resultado observado:
Archivo de evidencia:
Impacto:
Estado: reproducida
```

Nombres sugeridos para evidencias:

```text
F-001_archivos_processed_faltantes.txt
F-002_metadatos_sensores.txt
F-004_filas_pems_bay.txt
F-006_pipeline_completo.txt
F-007_reproducibilidad_algoritmos.txt
```

## 5. Prueba general del backend

### Todas las fallas

1. Abrir PowerShell.
2. Ubicarse en la raiz del proyecto TSI.
3. Ejecutar `python testing/backend/check_backend.py`.
4. Guardar la salida completa de la consola.
5. Comparar cada mensaje `[FALLO]` con `fallas_encontradas.md`.
6. Registrar el codigo de salida del comando.

Guardar la salida en un archivo de evidencia:

```powershell
python testing/backend/check_backend.py *> testing/backend/evidencia_diagnostico.txt
```

## 6. Pruebas de inventario y rutas

### F-001, F-002 y F-003

1. Abrir `data/01_processed/data_inventory.csv`.
2. Revisar las columnas `path`, `processed_output` y `clean_output`.
3. Comprobar que cada ruta exista en el proyecto.
4. Ejecutar el diagnostico.
5. Comparar las rutas faltantes reportadas con el inventario.

Comprobacion de rutas desde PowerShell:

```powershell
Test-Path .\data\01_processed\traffic_data_normalized.parquet
Test-Path .\data\01_processed\scraped_traffic_normalized.parquet
Test-Path .\data\01_processed\external\metr_la_sensor_locations.csv
Test-Path .\data\02_clean\external\metr_la_sensor_locations.csv
```

El resultado esperado es `True` para cada archivo que el inventario declara como existente.

## 7. Pruebas de filas y esquema

### F-004 y F-005

1. Abrir el archivo de metadatos de sensores de PEMS-BAY.
2. Contar sus filas.
3. Registrar sus columnas.
4. Comparar los valores con `data_inventory.csv`.
5. Ejecutar el diagnóstico.
6. Guardar la diferencia como evidencia.

Comprobacion con Python:

```powershell
.\.venv\Scripts\python.exe -c "import pandas as pd; p='data/00_raw/external/sensor_metadata/pems_bay_sensor_locations.csv'; df=pd.read_csv(p); print('filas:', len(df)); print('columnas:', list(df.columns))"
```

La cantidad real y las columnas deben coincidir con la información registrada en el inventario.

## 8. Pruebas del pipeline completo

### F-006

1. Revisar los scripts disponibles en `scripts/`.
2. Identificar el proceso que conecta raw, processed y clean.
3. Confirmar si existe un punto de entrada único para ejecutar todo el pipeline.
4. Ejecutar el diagnóstico.
5. Registrar que actualmente valida artefactos existentes, pero no reconstruye todas las etapas.

Resultado esperado:

```text
El pipeline completo se ejecuta en un directorio temporal y produce salidas verificables sin alterar los datos oficiales.
```

## 9. Pruebas de reproducibilidad de algoritmos

### F-007 y F-008

Revisar por separado:

- Isolation Forest
- Local Outlier Factor
- DBSCAN

Para cada algoritmo:

1. Identificar el dataset de entrada.
2. Identificar la salida filtrada.
3. Identificar el resumen y los parámetros utilizados.
4. Ejecutar el diagnóstico.
5. Comparar los registros de entrada y salida.
6. Confirmar si el algoritmo se vuelve a ejecutar o si solo se lee un archivo histórico.
7. Registrar si existe un resumen completo del resultado.

Archivos relacionados:

```text
data/02_clean/filtered_isolation_forest.csv
data/02_clean/filtered_local_outlier_factor.csv
data/02_clean/filtered_dbscan.csv
data/03_algorithm_output/local_outlier_factor_summary.csv
data/03_algorithm_output/dbscan_summary.csv
```

## 10. Pruebas de calidad de datos

### F-009

Para cada dataset validado:

1. Confirmar que el archivo pueda abrirse.
2. Revisar si contiene filas.
3. Revisar columnas y tipos.
4. Revisar fechas invalidas.
5. Revisar valores nulos.
6. Revisar duplicados.
7. Revisar rangos y valores negativos cuando corresponda.
8. Comparar los resultados con la salida del diagnostico.

La validacion debe reportar la regla especifica que no se cumple.

## 11. Pruebas de trazabilidad entre investigaciones

### F-010

1. Revisar la documentacion de la investigacion anterior.
2. Revisar la fecha y origen de cada artefacto.
3. Identificar si el archivo pertenece a la investigacion anterior o a la nueva.
4. Ejecutar el diagnostico.
5. Registrar si la herramienta muestra el origen y version del artefacto.

Resultado esperado:

```text
Cada artefacto debe indicar su origen, version, fecha y etapa del pipeline.
```

## 12. Hallazgos que requieren revision del codigo

Los siguientes hallazgos no necesariamente se detectan solo ejecutando el comando:

- **F-006:** revisar si existe un punto de entrada para ejecutar todo el pipeline.
- **F-007:** revisar si los algoritmos pueden ejecutarse nuevamente con la misma configuracion.
- **F-008:** revisar si Isolation Forest tiene un resumen equivalente al de los otros algoritmos.
- **F-009:** revisar las reglas de calidad aplicadas a cada dataset.
- **F-010:** revisar como se identifica el origen y version de los artefactos.

## 13. Orden recomendado

```text
1. Ejecutar el diagnostico general
2. Validar rutas del inventario
3. Comprobar archivos processed faltantes
4. Comprobar metadatos de sensores
5. Validar filas y columnas de PEMS-BAY
6. Revisar el pipeline completo
7. Revisar reproducibilidad de algoritmos
8. Completar reglas de calidad de datos
9. Separar artefactos historicos y nuevos
10. Registrar evidencias y resultados
```

Las correcciones se realizaran en una etapa posterior y se volveran a probar usando esta misma guia.
