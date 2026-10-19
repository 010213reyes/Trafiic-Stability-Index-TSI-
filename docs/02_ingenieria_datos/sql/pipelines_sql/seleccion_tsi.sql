USE tsi_db;

SELECT DATABASE();

SELECT
	c.nombre AS ciudad,
	f.nombre AS fuente,
	o.metrica_principal,
	COUNT(*) AS observaciones,
	MIN(o.timestamp_observacion) AS primera_observacion,
	MAX(o.timestamp_observacion) AS ultima_observacion
FROM fact_observaciones AS o
JOIN dim_ciudad AS c ON c.id_ciudad = o.id_ciudad
JOIN dim_fuente AS f ON f.id_fuente = o.id_fuente
GROUP BY c.nombre, f.nombre, o.metrica_principal
ORDER BY c.nombre, f.nombre, o.metrica_principal;