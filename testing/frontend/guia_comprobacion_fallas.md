# Guia para encontrar fallas del frontend

## 1. Objetivo

Comprobar las fallas del frontend de testing, registrar evidencia y dejar cada incidencia lista para una etapa posterior de correccion.

Aplicacion evaluada:

```text
testing/streamlit/app_testing.py
```

No se modifica durante esta etapa:

- `streamlit_dashboard/`
- Backend
- Datos del proyecto
- Algoritmos
- Reportes existentes

## 2. Iniciar la aplicacion

Desde la raiz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m streamlit run .\testing\streamlit\app_testing.py
```

Abrir la URL que muestre Streamlit, normalmente:

```text
http://localhost:8501
```

Credenciales del entorno de prueba:

```text
Usuario: admin
Contrasena: admin123
```

## 3. Metodo de comprobacion

Para cada prueba:

1. Leer el ID de la falla en `fallas_encontradas.md`.
2. Ejecutar los pasos indicados.
3. Comparar el resultado observado con el resultado esperado.
4. Tomar una captura de pantalla si la falla aparece.
5. Registrar fecha, navegador, URL y pasos realizados.
6. Marcar la falla como `reproducida` 
7. Corregir 

## 4. Formato de evidencia

Usar esta ficha para cada falla:

```text
ID:
Fecha:
Pantalla:
Usuario:
Pasos realizados:
Resultado esperado:
Resultado observado:
Archivo de evidencia:
Impacto:
Estado: reproducida
```

Nombres sugeridos para capturas:

```text
F-001_cierre_sesion.png
F-003_estado_raw.png
F-009_vista_processed.png
F-013_algoritmo.png
```

## 5. Pruebas de login y sesion

### F-001 y F-002

1. Abrir la aplicacion.
2. Iniciar sesion con `admin` y `admin123`.
3. Revisar el nombre y el mensaje de bienvenida.
4. Presionar `Cerrar sesion`.
5. Volver a iniciar sesion.
6. Comparar el usuario, el nombre mostrado y el estado de la sesion.

Comprobar si el mensaje corresponde al usuario autenticado y si el cierre elimina la informacion de la sesion anterior.

## 6. Pruebas de fuentes y linaje

### F-003 a F-008

1. Abrir la pestaña `Fuentes de datos`.
2. Seleccionar `traffic_data`.
3. Revisar los indicadores `Raw`, `Processed`, `Normalized` y `Clean`.
4. Revisar las rutas mostradas debajo de los indicadores.
5. Comparar cada estado con las rutas reales del proyecto.
6. Repetir con `scraped_traffic`, `crowdsourcing_raw`, `synthetic_traffic`, `metr_la` y `pems_bay`.

Comprobacion de rutas desde PowerShell:

```powershell
Test-Path .\data\00_raw\traffic_data.csv
Test-Path .\data\01_processed\pipeline\traffic_data.parquet
Test-Path .\data\01_processed\normalized\traffic_data.parquet
Test-Path .\data\02_clean\traffic_data.csv
```

El estado mostrado debe coincidir con la existencia real del archivo correspondiente.

## 7. Pruebas de vistas previas

### F-009 y F-010

Para cada fuente:

1. Seleccionar `Salida processed`.
2. Presionar `Cargar vista previa`.
3. Registrar el nombre del archivo y las columnas mostradas.
4. Seleccionar `Salida normalized`.
5. Presionar nuevamente `Cargar vista previa`.
6. Comparar ambas vistas.

Comprobacion directa de un CSV:

```powershell
Get-Content .\data\00_raw\traffic_data.csv -TotalCount 2
```

Comprobacion directa de un Parquet:

```powershell
.\.venv\Scripts\python.exe -c "import pandas as pd; print(pd.read_parquet('data/01_processed/pipeline/traffic_data.parquet').head(2))"
```

La vista mostrada debe corresponder a la etapa seleccionada.

## 8. Pruebas del laboratorio de algoritmos

### F-013, F-014 y F-018

Probar por separado:

- Isolation Forest
- Local Outlier Factor
- DBSCAN

Para cada algoritmo:

1. Abrir `Laboratorio de algoritmos`.
2. Seleccionar el algoritmo.
3. Presionar `Ejecutar prueba del algoritmo`.
4. Registrar filas de entrada, filas de salida y retencion.
5. Comparar el resultado con el archivo de `data/02_clean/`.
6. Verificar si el boton ejecuta el algoritmo o solo lee un archivo existente.
7. Comprobar que un resultado vacio no sea marcado automaticamente como aprobado.

Archivos relacionados:

```text
data/02_clean/filtered_isolation_forest.csv
data/02_clean/filtered_local_outlier_factor.csv
data/02_clean/filtered_dbscan.csv
```

## 9. Pruebas de reportes

### F-019 y F-020

1. Abrir `Reportes y visualizaciones`.
2. Seleccionar un algoritmo.
3. Presionar `Generar reporte de prueba`.
4. Descargar el JSON.
5. Revisar que el nombre, el resultado y la imagen correspondan al algoritmo.
6. Cambiar de algoritmo y repetir.
7. Cerrar y volver a iniciar Streamlit.
8. Comprobar si el reporte permanece disponible.
9. Revisar si se muestra fecha, version o configuracion de ejecucion.

## 10. Hallazgos que requieren revision del codigo

Los siguientes hallazgos no necesariamente se detectan navegando:

- **F-011:** buscar usuario y contrasena definidos como constantes.
- **F-012:** revisar lecturas de archivos sin manejo de excepciones.
- **F-013:** revisar si el boton llama un algoritmo o solo lee un CSV.
- **F-014:** revisar el uso de `pd.read_csv` sobre archivos completos.
- **F-015:** comparar el catalogo visual con los metadatos de sensores.
- **F-016:** comparar las salidas clean asignadas a cada fuente.
- **F-017:** revisar validacion de columnas y tipos antes de la vista previa.
- **F-018:** revisar el comportamiento cuando un archivo esta vacio.
- **F-019:** revisar el uso de `st.session_state` como unico almacenamiento.
- **F-020:** revisar si los artefactos muestran version y fecha de ejecucion.

## 11. Orden recomendado

```text
1. Login y sesion
2. Fuentes de datos
3. Estados del linaje
4. Rutas mostradas
5. Vistas previas
6. Algoritmos
7. Reportes
8. Reinicio de la app
9. Revision del codigo
10. Capturas y registro de resultados
```



Las correcciones se realizaran en una etapa posterior y se volveran a probar usando esta misma guia.
