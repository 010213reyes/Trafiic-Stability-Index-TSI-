FASE 2: INGENIERÍA DE DATOS

2.1 Inventario y linaje de datos
2.2 Diseño de arquitectura de datos
2.3 Pipeline RAW -> PROCESSED
2.4 Estandarización y normalización
2.5 Calidad y validación de datos
2.6 Integración y consolidación
2.7 Dataset CLEAN listo para análisis
2.8 Preparación de datos para SQL
2.9 Pipeline de carga hacia SQL
2.10 Reproducibilidad y trazabilidad
2.11 Validación final de la tubería

## Extensión multiciudad: estrategia de trabajo para 5 ciudades internacionales

El proyecto ya no se limitará a una sola ciudad de origen. A partir de este punto, la arquitectura debe operar con el mismo contrato para todas las ciudades, conservando una jerarquía clara de roles.

### Principio de diseño

- Guadalajara será la ciudad objetivo de validación local.
- Las ciudades internacionales serán fuentes de transferencia y comparación.
- Los datos sintéticos se mantienen para pruebas técnicas y regresión.
- La estructura del pipeline no cambia; lo que cambia es el catálogo de fuentes y el rol de cada ciudad.

### Flujo de trabajo por ciudad

1. Definición de la ciudad y metadatos del conjunto.
   - `ciudad`, `pais`, `timezone`, `fuente`, `rol_dato`, `fecha_inicio`, `fecha_fin`.
2. Descarga o captura del archivo raw.
   - Documentar licencia, alcance temporal y método de recolección.
3. Transformación a formato processed.
   - Normalización de columnas, timestamps y unidades.
4. Validación de calidad.
   - Completitud, rangos, duplicados, valores nulos, outliers reales.
5. Integración con el contrato común.
   - Unificación a esquema persistente de tráfico urbano.
6. Consolidación con el dataset principal.
   - Markers de `es_real`, `ciudad_objetivo` y `rol_dato`.
7. Preparación para SQL y análisis.
   - Tablas normalizadas y mantener solo la mínima versión de producción.

### Estructura esperada del conjunto

Cada ciudad debe entrar con la misma lógica:

- `raw/`: archivos originales con procedencia y fecha.
- `processed/`: datos estructurados y estandarizados.
- `clean/`: versión consolidada con contrato final.
- `sql/`: tabla de hecho y dimensiones de contexto.

### Recomendación ejecutiva

La implementación de estas 5 ciudades se hará en bloque, manteniendo el mismo proceso que para Guadalajara, pero con un criterio de transferencia explícito. Esto permite:

- ampliar el volumen de datos,
- mejorar la generalización del modelo,
- preservar la trazabilidad de cada ciudad,
- y evitar mezclar fuentes reales con sintéticas o locales con internacionales.