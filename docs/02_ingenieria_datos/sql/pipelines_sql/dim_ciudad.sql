USE tsi_db;

CREATE TABLE IF NOT EXISTS dim_ciudad (
    id_ciudad INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    pais VARCHAR(100) NOT NULL,
    zona_horaria VARCHAR(50) NOT NULL,
    es_ciudad_objetivo BOOLEAN NOT NULL DEFAULT FALSE,
    latitud DECIMAL(9,6) NULL,
    longitud DECIMAL(9,6) NULL,

    CONSTRAINT chk_ciudad_latitud
        CHECK (latitud BETWEEN -90 AND 90),

    CONSTRAINT chk_ciudad_longitud
        CHECK (longitud BETWEEN -180 AND 180),

    CONSTRAINT uq_ciudad
        UNIQUE (nombre, pais)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;