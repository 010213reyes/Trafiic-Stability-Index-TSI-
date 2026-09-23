# Contrato de fuentes internacionales

## Objetivo

Definir la ficha de minería y el contrato de ingeniería para las fuentes internacionales que apoyarán el modelado del TSI. Guadalajara permanece como ciudad objetivo de calibración y validación; las fuentes externas no se presentan como evidencia directa del tráfico local.

El registro operativo está en `data/00_raw/external/international_sources_contract.json`.

## Fuentes aceptadas

| Fuente | Ciudad | Variable principal | Rol | Estado |
|---|---|---|---|---|
| Istanbul Traffic Index | Istanbul | Índice de congestión | Comparación agregada | Raw validado |
| CET lentidão por trechos | Sao Paulo | Longitud de congestión | Comparación urbana | Fuente validada; raw pendiente |
| Histórico de puntos de tráfico | Madrid | Intensidad, ocupación y velocidad | Transferencia urbana | Fuente validada; raw pendiente |
| METR-LA | Los Angeles County | Velocidad por sensor | Preentrenamiento | Raw y processed validados |
| PEMS-BAY | San Francisco Bay Area | Velocidad por sensor | Transferencia | Raw y processed validados |

## Contrato común

Campos obligatorios en la salida normalizada:

- `timestamp`
- `ciudad`
- `fuente`
- `es_real`
- `segmento_id`
- `tipo_via`
- `calidad_registro`

Campos opcionales: `latitud`, `longitud`, `velocidad_kmh`, `flujo_veh_h`, `ocupacion_pct`, `densidad_veh_km`, `tiempo_viaje_seg`, `congestion_longitud_m` e `indice_congestion`.

Las variables que una fuente no mida permanecen nulas. No se transforma automáticamente ocupación en densidad, índice en velocidad ni longitud de congestionamiento en flujo.

## Proceso de minería por fuente

1. Registrar origen, licencia, zona horaria y periodo.
2. Revisar columnas, tipos, nulos, duplicados y cobertura temporal.
3. Medir frecuencia real y continuidad.
4. Identificar unidades y separar variables observadas de variables derivadas.
5. Documentar sesgos: autopistas, segmentos urbanos, índice agregado o cobertura irregular.
6. Emitir una decisión: aceptada, aceptada con advertencias o rechazada.

## Proceso de ingeniería por fuente

1. Conservar el archivo original en `data/00_raw/external/`.
2. Transformar a Parquet en `data/01_processed/external/`.
3. Mapear columnas al contrato común sin inventar mediciones.
4. Generar reporte de calidad y linaje.
5. Consolidar únicamente fuentes normalizadas en `data/02_clean/external/`.
6. Mantener `ciudad`, `fuente`, `rol_dato`, zona horaria y tipo de vía.

## Decisión metodológica

METR-LA y PEMS-BAY aportan volumen para velocidad temporal. Madrid aporta el mejor conjunto urbano multivariable. Sao Paulo aporta congestionamiento medido como longitud. Istanbul se conserva como índice agregado de comparación. La calibración de umbrales, pesos y horizonte de 18 a 20 minutos se realizará posteriormente con Guadalajara.