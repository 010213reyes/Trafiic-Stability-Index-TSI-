CREATE DATABASE IF NOT EXISTS tsi_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE tsi_db;

SOURCE docs/02_ingenieria_datos/sql/pipelines_sql/dim_ciudad.sql;
SOURCE docs/02_ingenieria_datos/sql/pipelines_sql/dim_fuentes.sql;
SOURCE docs/02_ingenieria_datos/sql/pipelines_sql/dim_segmento.sql;
SOURCE docs/02_ingenieria_datos/sql/pipelines_sql/fact_observaciones.sql;
SOURCE docs/02_ingenieria_datos/sql/pipelines_sql/calidad_observacion.sql;
SOURCE docs/02_ingenieria_datos/sql/pipelines_sql/fact_agregado.sql;
SOURCE docs/02_ingenieria_datos/sql/pipelines_sql/logs_carga.sql;
SOURCE docs/02_ingenieria_datos/sql/pipelines_sql/index_observ.sql;

SELECT DATABASE() AS base_seleccionada;
SHOW TABLES;