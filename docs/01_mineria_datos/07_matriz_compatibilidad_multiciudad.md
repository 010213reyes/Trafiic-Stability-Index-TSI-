# Matriz de compatibilidad multiciudad

## Objetivo

Evaluar fuentes públicas de tráfico antes de descargarlas e incorporarlas al proyecto. Las fuentes externas se utilizarán para aprender patrones generales y Guadalajara conservará la función de calibración y validación local.

## Criterios de aceptación

Una fuente entra al conjunto de transferencia cuando cumple:

- datos observados o metodología de medición documentada;
- timestamp y zona horaria identificables;
- resolución de 5 a 15 minutos;
- al menos 30 días o un periodo continuo equivalente;
- varios sensores o segmentos;
- condiciones de uso compatibles con el proyecto;
- velocidad disponible y, cuando exista, flujo, ocupación o tiempo de viaje.

Las variables que no existan no se inventan ni se imputan para completar el esquema. Se conservan como valores ausentes y la fuente se usa solo con las variables compatibles.

## Evaluación inicial

| Fuente | Ciudad o región | Origen | Periodo | Resolución | Variables confirmadas | Estado | Uso previsto |
|---|---|---|---|---|---|---|---|
| METR-LA | Los Angeles County | Sensores de autopista | 2012-03-01 a 2012-06-27 | 5 min | Velocidad; 207 sensores; 34,272 registros temporales | Verificada | Preentrenamiento temporal |
| PEMS-BAY | San Francisco Bay Area | Caltrans PeMS | 2017-01-01 a 2017-06-30 | 5 min | Velocidad; 325 sensores; 52,116 registros temporales | Verificada | Preentrenamiento temporal |
| Caltrans PeMS | California | Detectores de autopista | Histórico y tiempo real | 5 min | Flujo, velocidad, ocupación | Por verificar | Ampliación de variables |
| Madrid tráfico | Madrid | Portal municipal abierto | Por verificar | Por verificar | Intensidad y nivel de tráfico | Por verificar | Captura propia y contraste |
| Guadalajara actual | Guadalajara | Archivos locales existentes | Periodos fragmentados | Inconsistente | Velocidad y variables parciales | Insuficiente | Calibración exploratoria |
| Guadalajara futura | Guadalajara | Fuente pública por capturar | Por construir | Objetivo 5-15 min | Por definir | Pendiente | Validación final |

## Variables comunes iniciales

| Variable común | Obligatoria | Regla |
|---|---:|---|
| `timestamp` | Sí | Convertir a fecha/hora con zona horaria documentada |
| `ciudad` | Sí | Catálogo controlado de ciudades |
| `segmento_id` | Sí | Identificador del sensor o tramo; no usar solo el nombre de la avenida |
| `tipo_via` | Sí | Autopista, arterial urbana u otra categoría documentada |
| `velocidad_kmh` | Sí | Confirmar unidad y método de medición |
| `flujo_veh_h` | No | Mantener ausente cuando la fuente no lo mida |
| `ocupacion_pct` | No | No convertirla automáticamente en densidad |
| `densidad_veh_km` | No | Solo conservar si la fuente la mide o documenta su cálculo |
| `tiempo_viaje_seg` | No | Mantener separado de la velocidad del sensor |
| `fuente` | Sí | Nombre del dataset o portal original |
| `es_real` | Sí | `true` para observaciones reales; `false` para sintéticas o simuladas |

## Separación para modelado

```text
METR-LA, PEMS-BAY y otras fuentes aceptadas -> patrones generales
Guadalajara disponible                         -> calibración
Guadalajara capturada posteriormente           -> validación final
Fuentes sintéticas                             -> pruebas técnicas
```

La validación de la hipótesis de anticipación de **18–20 minutos** se reportará por separado para Guadalajara y para las ciudades externas.

## Evidencia de verificación

El repositorio público de DCRNN documenta los archivos históricos `metr-la.h5` y `pems-bay.h5` y sus instrucciones de descarga. Los archivos históricos utilizados en esta etapa provienen del registro público de Zenodo `5724362`, publicado como **PEMS-BAY and METR-LA in csv**.

Los archivos históricos descargados son:

- `data/00_raw/external/traffic_datasets/METR-LA.csv`: 34,272 timestamps, 207 sensores, del 1 de marzo al 27 de junio de 2012, intervalo dominante de 5 minutos.
- `data/00_raw/external/traffic_datasets/PEMS-BAY.csv`: 52,116 timestamps, 325 sensores, del 1 de enero al 30 de junio de 2017, intervalo dominante de 5 minutos.

También se conservaron los metadatos de ubicación de sensores:

- `data/00_raw/external/sensor_metadata/metr_la_sensor_locations.csv`: 207 filas, encabezados presentes, sin valores nulos.
- `data/00_raw/external/sensor_metadata/pems_bay_sensor_locations.csv`: 325 filas, tres columnas sin encabezados, sin valores nulos.

El archivo de PEMS-BAY debe normalizarse asignando las columnas `sensor_id`, `latitude` y `longitude` durante la ingeniería de datos, conservando el archivo original sin modificar.

## Próxima revisión

1. Descargar METR-LA y PEMS-BAY desde sus repositorios públicos.
2. Confirmar formato, licencia, columnas y frecuencia real.
3. Medir faltantes, duplicados, sensores y continuidad.
4. Actualizar esta matriz con evidencia de descarga.
5. Seleccionar las fuentes que pasarán a `data/00_raw/`.