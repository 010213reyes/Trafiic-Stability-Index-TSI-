# Plan de implementación para 5 ciudades internacionales

## Objetivo

Ampliar la base de conocimiento del proyecto con cinco ciudades internacionales que comparten patrones urbanos de congestión y movilidad. La finalidad no es reemplazar a Guadalajara, sino construir una red de transferencia de aprendizaje para mejorar la generalización del modelo y mantener a Guadalajara como ciudad objetivo de validación local.

## Ciudades seleccionadas

| Ciudad | País | Región | Prioridad | Rol en el proyecto | Fuente esperada |
|---|---|---|---:|---|---|
| Bangkok | Tailandia | Asia | 1 | Entrenamiento general | Datos abiertos de tránsito urbano y sensores |
| Istanbul | Turquía | Europa/Asia | 2 | Entrenamiento y comparación | Sensores de flujo/velocidad y red vial urbana |
| Dubai | Emiratos Árabes Unidos | Medio Oriente | 3 | Comparación de crecimiento veloz y alta demanda | Datos urbanos y arterias principales |
| Madrid | España | Europa | 4 | Comparación con ciudad europea | Portales públicos y sensores de tráfico |
| Barcelona | España | Europa | 5 | Validación y comparación | Datos de tránsito urbano y congestionamiento |

## Principio de diseño

- Guadalajara se mantiene como ciudad objetivo local.
- Las ciudades externas se usan para transferencia, comparación y generalización.
- Todas las fuentes deben responder al mismo contrato de datos del proyecto.
- No se aceptan datos sin metadatos de ciudad, país, timestamp y fuente.

## Contrato mínimo por ciudad

Cada ciudad debe documentarse con:

- ciudad
- país
- region
- timezone
- fuente
- rol_dato
- fecha_inicio
- fecha_fin
- frecuencia
- variables disponibles
- licencia
- enlace de consulta
- estado (`pendiente`, `validada`, `normalizada`, `integrada`)

## Esquema común de trabajo

Para cada ciudad se aplicará la misma secuencia:

1. Definición del catálogo de fuentes.
2. Verificación de acceso y licencia.
3. Descarga de datos raw.
4. Validación de cobertura temporal y calidad.
5. Normalización y mapeo a esquema común.
6. Generación del dataset processed.
7. Consolidación con el contrato del proyecto.
8. Generación de dataset clean.
9. Preparación para SQL.
10. Registro de trazabilidad y reproducibilidad.

## Directorio sugerido por ciudad

Cada ciudad debe quedar en una estructura equivalente a la siguiente:

- data/00_raw/external/<ciudad>/
- data/01_processed/external/<ciudad>/
- data/02_clean/external/<ciudad>/
- docs/01_mineria_datos/fuentes/<ciudad>/
- docs/02_ingenieria_datos/<ciudad>/

## Variables mínimas esperadas

Se acepta una ciudad si aporta al menos una de estas combinaciones:

- velocidad
- flujo
- ocupación
- tiempo de viaje
- intensidad de tráfico
- nivel de congestión

## Reglas de aceptación

Una fuente internacional se incorpora si cumple:

- origen medido o metodología documentada
- timestamp explícito y zona horaria identificable
- resolución de 5 a 15 minutos
- al menos 30 días de continuidad o un bloque equivalente
- cobertura con varios segmentos o sensores
- licencias compatibles con el proyecto
- esquema compatible con el pipeline de ingeniería

## Orden de ejecución recomendado

1. Bangkok
2. Madrid
3. Istanbul
4. Barcelona
5. Dubai

Este orden prioriza primero la ciudad con mejor probabilidad de disponibilidad extendida y luego completa la diversidad geográfica.

## Criterio de integración

Toda ciudad externa se integrará con el mismo contrato del proyecto, pero siempre conservando:

- ciudad
- pais
- fuente
- rol_dato
- ciudad_objetivo
- es_real
- segmento_id
- timestamp_local
- timezone

## Resultado esperado

El proyecto debe quedar preparado para:

- entrenar con patrones generales multiciudad,
- validar con Guadalajara de forma local,
- mantener trazabilidad por ciudad,
- y evitar mezclar fuentes reales, sintéticas y locales en una sola capa analítica.
