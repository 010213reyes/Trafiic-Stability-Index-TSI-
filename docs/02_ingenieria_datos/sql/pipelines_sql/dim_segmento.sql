USE tsi_db;

CREATE TABLE IF NOT EXISTS dim_segmento (
    id_segmento INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_ciudad INT UNSIGNED NOT NULL,
    id_fuente INT UNSIGNED NOT NULL,
    identificador_origen VARCHAR(150) NOT NULL,
    tipo_entidad VARCHAR(30) NOT NULL,
    tipo_via VARCHAR(100) NULL,
    descripcion VARCHAR(255) NULL,
    latitud DECIMAL(9,6) NULL,
    longitud DECIMAL(9,6) NULL,

    CONSTRAINT fk_segmento_ciudad
        FOREIGN KEY (id_ciudad)
        REFERENCES dim_ciudad(id_ciudad),

    CONSTRAINT fk_segmento_fuente
        FOREIGN KEY (id_fuente)
        REFERENCES dim_fuente(id_fuente),

    CONSTRAINT chk_segmento_latitud
        CHECK (latitud BETWEEN -90 AND 90),

    CONSTRAINT chk_segmento_longitud
        CHECK (longitud BETWEEN -180 AND 180),

    CONSTRAINT uq_segmento_origen
        UNIQUE (id_fuente, identificador_origen)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;