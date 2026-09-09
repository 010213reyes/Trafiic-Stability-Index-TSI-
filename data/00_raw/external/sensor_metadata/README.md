# Metadatos de sensores externos

Archivos originales descargados del repositorio público de DCRNN para documentar la ubicación de los sensores de METR-LA y PEMS-BAY.

| Archivo | Fuente original | Contenido | Observación |
|---|---|---|---|
| `metr_la_sensor_locations.csv` | `https://raw.githubusercontent.com/liyaguang/DCRNN/master/data/sensor_graph/graph_sensor_locations.csv` | 207 sensores con `sensor_id`, latitud y longitud | Encabezados presentes |
| `pems_bay_sensor_locations.csv` | `https://raw.githubusercontent.com/liyaguang/DCRNN/master/data/sensor_graph/graph_sensor_locations_bay.csv` | 325 sensores con identificador y coordenadas | Archivo original sin encabezados |

Estos archivos se conservan sin modificar. La asignación de nombres de columnas de PEMS-BAY se realizará en `data/01_processed/`.