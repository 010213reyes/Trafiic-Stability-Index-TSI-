-- Manual SQL de resumen analitico para tsi_db.
-- Ejecutar despues de la validacion basica de 06_validacion_sql.
-- Estas consultas son de solo lectura.

USE tsi_db;

-- 1. Distribucion de observaciones por ciudad, fuente y metrica.
SELECT
    c.nombre AS ciudad,
    f.nombre AS fuente,
    o.metrica_principal,
    COUNT(*) AS observaciones
FROM fact_observaciones AS o
JOIN dim_ciudad AS c ON c.id_ciudad = o.id_ciudad
JOIN dim_fuente AS f ON f.id_fuente = o.id_fuente
GROUP BY c.nombre, f.nombre, o.metrica_principal
ORDER BY c.nombre, f.nombre, o.metrica_principal;

-- 2. Estadisticos de la metrica principal por fuente.
SELECT
    f.nombre AS fuente,
    o.metrica_principal,
    COUNT(*) AS observaciones,
    MIN(o.valor_principal) AS minimo,
    AVG(o.valor_principal) AS media,
    MAX(o.valor_principal) AS maximo
FROM fact_observaciones AS o
JOIN dim_fuente AS f ON f.id_fuente = o.id_fuente
GROUP BY f.nombre, o.metrica_principal
ORDER BY f.nombre, o.metrica_principal;

-- 3. Cobertura por dia y fuente.
SELECT
    f.nombre AS fuente,
    DATE(o.timestamp_observacion) AS fecha,
    COUNT(*) AS observaciones,
    AVG(o.valor_principal) AS media_diaria
FROM fact_observaciones AS o
JOIN dim_fuente AS f ON f.id_fuente = o.id_fuente
GROUP BY f.nombre, DATE(o.timestamp_observacion)
ORDER BY f.nombre, fecha;

-- 4. Calidad de registro por fuente.
SELECT
    f.nombre AS fuente,
    o.calidad_registro,
    COUNT(*) AS observaciones
FROM fact_observaciones AS o
JOIN dim_fuente AS f ON f.id_fuente = o.id_fuente
GROUP BY f.nombre, o.calidad_registro
ORDER BY f.nombre, o.calidad_registro;

-- 5. Segmentos con mayor volumen dentro de cada fuente.
SELECT
    f.nombre AS fuente,
    o.id_segmento,
    COUNT(*) AS observaciones
FROM fact_observaciones AS o
JOIN dim_fuente AS f ON f.id_fuente = o.id_fuente
GROUP BY f.nombre, o.id_segmento
ORDER BY f.nombre, observaciones DESC;
