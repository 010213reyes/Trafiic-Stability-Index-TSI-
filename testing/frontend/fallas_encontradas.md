# Reporte de fallas  en el frontend de testing

## Estado

Reporte inicial. Las fallas permanecen sin corregir para documentar el ciclo de pruebas de la materia Laboratorio Abierto.

## Alcance

- Aplicación evaluada: `testing/streamlit/app_testing.py`.
- Tipo de prueba: revisión funcional y estática del frontend.
- Fecha: 2026-09-13.
- Entorno: Streamlit local con `.venv`.
- Estado del dashboard principal: no evaluado ni modificado.



### F-001: El cierre de sesión conserva el usuario en memoria

- **Sección:** sesión.
- **Cómo reproducir:** iniciar sesión, cerrar sesión y revisar el estado de la sesión.
- **Resultado esperado:** limpiar todas las variables del usuario.
- **Resultado observado:** `username` permanece almacenado.
- **Impacto:** bajo; puede dejar información de la sesión anterior disponible.
- **Estado:** pendiente.

### F-002: El mensaje de bienvenida no utiliza el usuario autenticado

- **Sección:** sesión.
- **Cómo reproducir:** iniciar sesión y observar el mensaje de bienvenida.
- **Resultado esperado:** mostrar el usuario autenticado.
- **Resultado observado:** muestra siempre `Luis`, aunque la sesión usa el identificador `admin`.
- **Impacto:** bajo; información inconsistente para el usuario.
- **Estado:** pendiente.

### F-003: El indicador Raw consulta la ruta Processed

- **Sección:** Fuentes de datos.
- **Cómo reproducir:** seleccionar cualquier fuente y comparar el indicador `Raw` con la ruta real.
- **Resultado esperado:** verificar la existencia del archivo en `data/00_raw/`.
- **Resultado observado:** consulta la ruta `processed`.
- **Impacto:** medio; el estado visual del linaje puede ser incorrecto.
- **Estado:** pendiente.

### F-004: El indicador Processed consulta la ruta Raw

- **Sección:** Fuentes de datos.
- **Cómo reproducir:** seleccionar una fuente y revisar el indicador `Processed`.
- **Resultado esperado:** verificar el archivo de `data/01_processed/`.
- **Resultado observado:** consulta el archivo raw.
- **Impacto:** medio; puede reportar una etapa procesada como disponible sin estarlo.
- **Estado:** pendiente.

### F-005: El indicador Normalized consulta la ruta Clean

- **Sección:** Fuentes de datos.
- **Cómo reproducir:** revisar el estado `Normalized` de una fuente.
- **Resultado esperado:** consultar `data/01_processed/normalized/`.
- **Resultado observado:** consulta la salida clean.
- **Impacto:** medio; estado de pipeline incorrecto.
- **Estado:** pendiente.

### F-006: El indicador Clean consulta la ruta Normalized

- **Sección:** Fuentes de datos.
- **Cómo reproducir:** revisar el estado `Clean` de una fuente.
- **Resultado esperado:** consultar `data/02_clean/`.
- **Resultado observado:** consulta la salida normalized.
- **Impacto:** medio; confunde la etapa final con la intermedia.
- **Estado:** pendiente.

### F-007: La ruta mostrada para Processed repite la ruta Raw

- **Sección:** Fuentes de datos.
- **Cómo reproducir:** seleccionar una fuente y comparar las rutas Raw y Processed.
- **Resultado esperado:** mostrar dos rutas diferentes.
- **Resultado observado:** ambas muestran el archivo raw.
- **Impacto:** medio; rompe la trazabilidad visual.
- **Estado:** pendiente.

### F-008: La ruta mostrada para Normalized apunta a Clean

- **Sección:** Fuentes de datos.
- **Cómo reproducir:** revisar las rutas Normalized y Clean.
- **Resultado esperado:** Normalized debe apuntar a `data/01_processed/normalized/`.
- **Resultado observado:** apunta a la salida clean.
- **Impacto:** medio; información incorrecta de linaje.
- **Estado:** pendiente.

### F-009: La vista Processed carga el archivo Normalized

- **Sección:** vista previa de fuentes.
- **Cómo reproducir:** seleccionar `Salida processed` y presionar `Cargar vista previa`.
- **Resultado esperado:** cargar el Parquet de `data/01_processed/pipeline/`.
- **Resultado observado:** carga la salida normalized.
- **Impacto:** medio; la evidencia visual no corresponde a la etapa seleccionada.
- **Estado:** pendiente.

### F-010: La vista Normalized carga el archivo Processed

- **Sección:** vista previa de fuentes.
- **Cómo reproducir:** seleccionar `Salida normalized` y presionar `Cargar vista previa`.
- **Resultado esperado:** cargar el Parquet de `data/01_processed/normalized/`.
- **Resultado observado:** carga la salida processed.
- **Impacto:** medio; confunde el recorrido del dato.
- **Estado:** pendiente.

# adicionales

### F-011: Credenciales simuladas escritas directamente en el código

- **Sección:** login.
- **Hallazgo:** usuario y contraseña están definidos como constantes en `app_testing.py`.
- **Riesgo:** no es apropiado para producción y facilita exposición accidental de credenciales.
- **Estado:** pendiente.

### F-012: No hay manejo de excepciones al leer archivos

- **Sección:** carga de datos.
- **Hallazgo:** un CSV corrupto, un Parquet inválido o un problema de permisos puede detener la aplicación.
- **Resultado esperado:** mostrar un error controlado y conservar la navegación.
- **Estado:** pendiente.

### F-013: Los algoritmos no se ejecutan realmente desde la interfaz

- **Sección:** Laboratorio de algoritmos.
- **Hallazgo:** el botón carga archivos filtrados previamente; no ejecuta Isolation Forest, LOF ni DBSCAN.
- **Riesgo:** el texto de la interfaz puede hacer creer que se ejecutó un entrenamiento nuevo.
- **Estado:** pendiente.

### F-014: Carga completa de archivos para calcular métricas

- **Sección:** Laboratorio de algoritmos.
- **Hallazgo:** `read_csv` carga archivos completos en memoria.
- **Riesgo:** tiempos altos o agotamiento de memoria cuando los artefactos crezcan.
- **Estado:** pendiente.

### F-015: El catálogo visual no incluye los metadatos de sensores

- **Sección:** Fuentes de datos.
- **Hallazgo:** METR-LA y PEMS-BAY aparecen, pero sus catálogos de ubicaciones no tienen una entrada propia.
- **Riesgo:** el usuario no puede inspeccionar desde la interfaz el origen espacial de los sensores.
- **Estado:** pendiente.

### F-016: Dos fuentes apuntan a la misma salida clean

- **Sección:** linaje.
- **Hallazgo:** `traffic_data` y `scraped_traffic` muestran `data/02_clean/traffic_data.csv` como salida.
- **Riesgo:** la interfaz no distingue si el archivo es compartido, consolidado o sobrescrito.
- **Estado:** pendiente.

### F-017: No se valida el esquema antes de mostrar una vista previa

- **Sección:** Fuentes de datos.
- **Hallazgo:** se comprueba la existencia del archivo, pero no sus columnas, tipos ni formato esperado.
- **Riesgo:** una salida incorrecta puede mostrarse como válida.
- **Estado:** pendiente.

### F-018: Un resultado vacío se reporta como prueba aprobada

- **Sección:** Laboratorio de algoritmos.
- **Hallazgo:** si el archivo existe pero no tiene filas, la prueba mantiene el estado `passed`.
- **Resultado esperado:** advertencia o fallo controlado.
- **Estado:** pendiente.

### F-019: No existe registro persistente de ejecuciones

- **Sección:** reportes.
- **Hallazgo:** el reporte se conserva solo en `st.session_state` durante la sesión actual.
- **Riesgo:** al cerrar o reiniciar la app se pierde la evidencia de la prueba.
- **Estado:** pendiente.

### F-020: La interfaz no diferencia artefactos históricos de resultados nuevos

- **Sección:** reportes y algoritmos.
- **Hallazgo:** los archivos de `data/02_clean` y `data/03_algorithm_output` se presentan como resultados disponibles, sin versión de ejecución visible.
- **Riesgo:** no se puede confirmar cuándo ni con qué configuración se generó el resultado.
- **Estado:** pendiente.

## Resumen

| Grupo | Cantidad | Estado |
|---|---:|---|
| Fallas | 10 | Sin corregir |
| Fallas del frontend | 10 | Sin corregir |
| Total documentado | 20 | Pendiente de priorización |

## Regla de trabajo

Este reporte documenta los problemas encontrados. No se aplican correcciones en esta etapa. La siguiente etapa será priorizar los fallos, reproducirlos con evidencia y repararlos uno por uno.
