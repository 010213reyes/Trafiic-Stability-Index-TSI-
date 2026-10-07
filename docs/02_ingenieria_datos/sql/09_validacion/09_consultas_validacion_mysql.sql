-- SQL-09: consultas de validacion de la base internacional TSI.
-- Ejecutar despues de SQL-08 y guardar los resultados junto al manifiesto de carga.

-- 1. Conteo general y dimensiones.
SELECT COUNT(*) AS observaciones FROM fact_observaciones;
SELECT COUNT(*) AS ciudades FROM dim_ciudad;
SELECT COUNT(*) AS fuentes FROM dim_fuente;
SELECT COUNT(*) AS segmentos FROM dim_segmento;

-- 2. Cobertura por ciudad, fuente y metrica principal.
SELECT c.nombre AS ciudad, f.nombre AS fuente, COUNT(*) AS observaciones
FROM fact_observaciones o
JOIN dim_ciudad c ON c.ciudad_id = o.ciudad_id
JOIN dim_fuente f ON f.fuente_id = o.fuente_id
GROUP BY c.nombre, f.nombre
ORDER BY c.nombre, f.nombre;

SELECT f.nombre AS fuente, o.metrica_principal, COUNT(*) AS observaciones
FROM fact_observaciones o
JOIN dim_fuente f ON f.fuente_id = o.fuente_id
GROUP BY f.nombre, o.metrica_principal
ORDER BY f.nombre, o.metrica_principal;

-- 3. Fechas y calidad.
SELECT MIN(timestamp) AS fecha_inicio, MAX(timestamp) AS fecha_fin
FROM fact_observaciones;

SELECT calidad_registro, COUNT(*) AS observaciones
FROM fact_observaciones
GROUP BY calidad_registro
ORDER BY calidad_registro;

-- 4. Campos obligatorios y relaciones huérfanas.
SELECT COUNT(*) AS nulos_obligatorios
FROM fact_observaciones
WHERE timestamp IS NULL
   OR ciudad_id IS NULL
   OR fuente_id IS NULL
   OR segmento_id IS NULL
   OR metrica_principal IS NULL
   OR valor_principal IS NULL
   OR calidad_registro IS NULL;

SELECT COUNT(*) AS fuentes_sin_ciudad
FROM dim_fuente f
LEFT JOIN dim_ciudad c ON c.ciudad_id = f.ciudad_id
WHERE c.ciudad_id IS NULL;

SELECT COUNT(*) AS segmentos_sin_fuente
FROM dim_segmento s
LEFT JOIN dim_fuente f ON f.fuente_id = s.fuente_id
WHERE f.fuente_id IS NULL;

SELECT COUNT(*) AS hechos_sin_segmento
FROM fact_observaciones o
LEFT JOIN dim_segmento s ON s.segmento_id = o.segmento_id
WHERE s.segmento_id IS NULL;

-- 5. Rangos que deben ser imposibles o sospechosos.
SELECT COUNT(*) AS ocupacion_fuera_de_rango
FROM fact_observaciones
WHERE ocupacion_pct IS NOT NULL AND (ocupacion_pct < 0 OR ocupacion_pct > 100);

SELECT COUNT(*) AS tiempo_viaje_negativo
FROM fact_observaciones
WHERE tiempo_viaje_seg IS NOT NULL AND tiempo_viaje_seg < 0;

SELECT COUNT(*) AS congestion_negativa
FROM fact_observaciones
WHERE congestion_longitud_m IS NOT NULL AND congestion_longitud_m < 0;

-- 6. Trazabilidad de lotes.
SELECT estado, SUM(filas_leidas) AS filas_leidas, SUM(filas_insertadas) AS filas_insertadas,
       SUM(filas_rechazadas) AS filas_rechazadas
FROM log_cargas
GROUP BY estado
ORDER BY estado;