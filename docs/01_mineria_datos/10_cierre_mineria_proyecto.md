# Cierre de la minería de datos

## 1. Alcance del documento

Este documento cierra la Fase 1 de minería de datos del proyecto de inteligencia artificial. Consolida los acuerdos de los documentos 01 al 09 de esta carpeta.

La investigación inicial del TSI se conserva como antecedente. Sus notebooks, experimentos, datos sintéticos y resultados no se reinterpretan como evidencia del proyecto nuevo. Esta fase toma sus hallazgos como punto de partida y establece el contrato para una implementación reproducible con fuentes reales.

## 2. Problema operativo

El proyecto busca identificar condiciones de pre-colapso del tráfico y estimar la probabilidad de que un segmento entre en congestión dentro de un horizonte de **18–20 minutos**.

La capacidad anticipatoria se medirá usando únicamente información disponible hasta el instante de predicción. La evaluación final se separará por ciudad y fuente, con Guadalajara como referencia local cuando exista una serie suficiente.

## 3. Decisiones de datos

- Se aceptan fuentes públicas de cualquier país cuando cumplan los criterios técnicos definidos.
- Las fuentes externas se utilizarán para aprender patrones generales de tráfico.
- Guadalajara conservará la función de calibración y validación local.
- Los datos sintéticos se utilizarán para pruebas técnicas, no como evidencia de comportamiento real.
- Los archivos originales se conservan en `data/00_raw/` sin modificaciones.
- Las transformaciones se realizan en `data/01_processed/`.
- Las variables ausentes permanecen nulas; no se inventan para igualar esquemas.
- Autopistas y avenidas urbanas conservarán su clasificación mediante `tipo_via`.

## 4. Fuentes evaluadas

### Fuentes externas reales

| Fuente | Cobertura | Resolución | Estado |
|---|---|---:|---|
| METR-LA | 207 sensores, Los Angeles County, 2012-03-01 a 2012-06-27 | 5 min | Verificada y procesada |
| PEMS-BAY | 325 sensores, San Francisco Bay Area, 2017-01-01 a 2017-06-30 | 5 min | Verificada y procesada |
| Caltrans PeMS | California; flujo, velocidad y ocupación | 5 min | Pendiente de verificación |
| Madrid tráfico | Portal municipal abierto | Por verificar | Candidata para captura propia |

METR-LA y PEMS-BAY se descargaron desde el registro público de Zenodo `5724362`. Sus CSV originales están en `data/00_raw/external/traffic_datasets/` y sus representaciones Parquet en `data/01_processed/external/`.

### Fuentes locales de Guadalajara

| Fuente | Registros | Estado |
|---|---:|---|
| `traffic_data.csv` | 310 | Fragmentada; velocidad y densidad parciales |
| `scraped_traffic.csv` | 117 | Fragmentada; velocidad y densidad parciales |
| `crowdsourcing_raw.csv` | 500 | Observaciones de usuarios; cobertura no uniforme |
| `crowdsourcing_aggregated.csv` | 148 | Agregado derivado del archivo raw |

Estas fuentes quedan disponibles para calibración exploratoria. Aún no constituyen una serie continua suficiente para la validación local de 18–20 minutos.

## 5. Calidad verificada

- METR-LA: 34,272 timestamps, 207 sensores, intervalo dominante de 5 minutos.
- PEMS-BAY: 52,116 timestamps, 325 sensores, intervalo dominante de 5 minutos.
- Ambos datasets externos tienen cero timestamps inválidos, cero faltantes y cero valores negativos en la validación ejecutada.
- Los metadatos de ubicación contienen 207 sensores de METR-LA y 325 de PEMS-BAY sin valores nulos.
- Las fuentes locales tienen timestamps válidos, pero esquemas, resolución y cobertura heterogéneos.

El reporte reproducible de calidad está en `data/01_processed/external/external_traffic_quality.json`.

## 6. Contrato común aprobado

El pipeline nuevo utilizará, cuando estén disponibles:

```text
timestamp
ciudad
fuente
es_real
segmento_id
tipo_via
latitud
longitud
velocidad_kmh
flujo_veh_h
ocupacion_pct
densidad_veh_km
tiempo_viaje_seg
calidad_registro
```

Los campos obligatorios son `timestamp`, `ciudad`, `fuente`, `es_real`, `segmento_id` y `tipo_via`. La velocidad es la variable común prioritaria, pero puede estar ausente en una fuente concreta hasta verificar su esquema.

## 7. Etiquetas operativas aprobadas

- `congestion_event`: indica si existe un evento objetivo dentro del horizonte.
- `pre_colapso`: indica si existe deterioro observable antes del evento.
- `event_start`: registra el inicio del evento.
- `horizon_minutes`: registra la distancia entre la observación y el evento.
- `label_status`: registra si la etiqueta es válida o si falta historial, resolución o claridad.

Las líneas base y los umbrales se calcularán por ciudad, segmento, tipo de vía y franja temporal. No se aplicará un umbral absoluto idéntico a todas las fuentes.

## 8. Riesgos controlados

- Transferencia de patrones entre ciudades con distinta infraestructura.
- Confusión entre datos reales externos y evidencia local.
- Mezcla de sensores de autopista con avenidas urbanas.
- Fuga de información futura al construir etiquetas.
- Uso de datos sintéticos como validación real.
- Imputación de variables que la fuente no mide.
- Duplicación de evidencia entre datos raw y agregados.

Los controles son conservar metadatos de fuente y segmento, dividir temporalmente los datos, calcular etiquetas antes del entrenamiento y reportar resultados por ciudad.

## 9. Estado de la fase

### Completado

- Problema y horizonte operativo definidos.
- Fuentes externas públicas localizadas y evaluadas.
- METR-LA y PEMS-BAY descargados, procesados y validados.
- Matriz multiciudad documentada.
- Diccionario de datos del proyecto creado.
- Etiquetas de congestión y pre-colapso definidas.
- Riesgos y reglas de separación documentados.

### Pendiente en ingeniería de datos

- Normalizar las fuentes locales de Guadalajara al contrato común.
- Confirmar unidades y metodología de sus variables.
- Crear una serie continua de Guadalajara para calibración y validación.
- Implementar la construcción reproducible de etiquetas.
- Generar el dataset `clean` que pasará a SQL.

## 10. Decisión de avance

La minería de datos queda **cerrada para iniciar la Fase 2: Ingeniería de datos**, con una condición explícita: la validación final de la hipótesis en Guadalajara queda pendiente hasta disponer de una serie local suficiente.

El siguiente flujo autorizado es:

```text
data/00_raw -> data/01_processed -> data/02_clean -> SQL
```

La investigación anterior permanece como etapa histórica independiente; el proyecto punta a punta comienza a partir de este contrato.