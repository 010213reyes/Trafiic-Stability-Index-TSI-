-- Manual SQL de validacion para tsi_db.
-- Ejecutar una consulta a la vez desde MySQL Workbench.
-- Estas consultas no modifican datos.

USE tsi_db;

-- 1. Conteo total de hechos.
SELECT COUNT(*) AS observaciones_mysql
FROM fact_observaciones;

-- 2. Conteo por fuente.
SELECT
    f.nombre AS fuente,
    COUNT(*) AS observaciones
FROM fact_observaciones AS o
JOIN dim_fuente AS f ON f.id_fuente = o.id_fuente
GROUP BY f.nombre
ORDER BY f.nombre;

-- 3. Cobertura temporal por fuente y metrica.
SELECT
    f.nombre AS fuente,
    o.metrica_principal,
    COUNT(*) AS observaciones,
    MIN(o.timestamp_observacion) AS primera_observacion,
    MAX(o.timestamp_observacion) AS ultima_observacion
FROM fact_observaciones AS o
JOIN dim_fuente AS f ON f.id_fuente = o.id_fuente
GROUP BY f.nombre, o.metrica_principal
ORDER BY f.nombre, o.metrica_principal;

-- 4. Nulos en campos obligatorios.
SELECT COUNT(*) AS filas_con_nulos_obligatorios
FROM fact_observaciones
WHERE id_ciudad IS NULL
   OR id_fuente IS NULL
   OR id_segmento IS NULL
   OR timestamp_observacion IS NULL
   OR metrica_principal IS NULL
   OR valor_principal IS NULL
   OR calidad_registro IS NULL;

-- 5. Relaciones huerfanas.
SELECT COUNT(*) AS hechos_sin_ciudad
FROM fact_observaciones AS o
LEFT JOIN dim_ciudad AS c ON c.id_ciudad = o.id_ciudad
WHERE c.id_ciudad IS NULL;

SELECT COUNT(*) AS hechos_sin_fuente
FROM fact_observaciones AS o
LEFT JOIN dim_fuente AS f ON f.id_fuente = o.id_fuente
WHERE f.id_fuente IS NULL;

SELECT COUNT(*) AS hechos_sin_segmento
FROM fact_observaciones AS o
LEFT JOIN dim_segmento AS s ON s.id_segmento = o.id_segmento
WHERE s.id_segmento IS NULL;

-- 6. Rangos fisicos.
SELECT COUNT(*) AS ocupacion_fuera_de_rango
FROM fact_observaciones
WHERE ocupacion_pct IS NOT NULL AND (ocupacion_pct < 0 OR ocupacion_pct > 100);

SELECT COUNT(*) AS valores_negativos
FROM fact_observaciones
WHERE velocidad_kmh < 0
   OR flujo_veh_h < 0
   OR densidad_veh_km < 0
   OR tiempo_viaje_seg < 0
   OR congestion_longitud_m < 0;

-- 7. Trazabilidad de cargas. Este resultado suma el historial, no el estado actual.
SELECT
    estado,
    SUM(registros_leidos) AS filas_leidas,
    SUM(registros_insertados) AS filas_insertadas,
    SUM(registros_rechazados) AS filas_rechazadas
FROM log_cargas
GROUP BY estado
ORDER BY estado;
