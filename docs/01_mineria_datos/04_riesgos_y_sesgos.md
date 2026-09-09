# Riesgos y sesgos

## Riesgos por fuente

- **Sintética:** representa reglas del generador y no evidencia comportamiento real.
- **Scraping:** depende de la fuente, momento de captura, estabilidad del sitio y reglas de extracción.
- **Histórica/base:** tiene faltantes, nombres de avenida inconsistentes y procedencia que debe confirmarse.
- **Crowdsourcing:** depende de quién reporta, dónde circula, qué dispositivo usa y qué nivel de confianza tiene.
- **Agregada:** puede ocultar variabilidad individual y no es una fuente independiente de la raw.

## Riesgos metodológicos

- Confundir un valor atípico con una anomalía de tráfico.
- Usar umbrales iguales para avenidas con comportamientos distintos.
- Mezclar años y periodos como si fueran observaciones comparables.
- Introducir fuga de información al calcular variables con datos futuros.
- Tratar datos sintéticos como validación de capacidad predictiva real.
- Transferir patrones entre ciudades con distinta infraestructura, clima, geometría vial o método de medición.
- Confundir datos reales de otra ciudad con evidencia de validez para Guadalajara.
- Combinar sensores de autopista con avenidas urbanas sin conservar el tipo de vía.
- Duplicar evidencia al usar raw y agregado de crowdsourcing en el mismo análisis.
- Imputar faltantes sin documentar el supuesto.

## Riesgo de anticipación

Actualmente no hay evidencia suficiente para afirmar anticipación de 18 a 20 minutos. La fuente sintética tiene intervalos de 10 minutos, pero eso solo demuestra resolución temporal, no capacidad predictiva. Para validar anticipación se requiere una secuencia temporal real con un evento definido y datos anteriores y posteriores al evento.

## Controles propuestos

- Mantener separadas las fuentes por origen.
- Documentar unidades y transformaciones.
- Usar división temporal para validación.
- Crear etiquetas o reglas de evento antes de evaluar modelos.
- Reportar cobertura y faltantes junto con cualquier métrica.
- Comparar resultados contra una línea base simple.
- Mantener `ciudad`, `fuente`, `segmento_id`, `tipo_via` y `es_real` en el esquema común.
- Ajustar umbrales por ciudad y avenida antes de comparar desempeño.
- Evaluar por separado: entrenamiento externo, calibración local y prueba de Guadalajara.
