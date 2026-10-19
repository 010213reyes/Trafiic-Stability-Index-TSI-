USE tsi_db;

CREATE TABLE IF NOT EXISTS fact_agregado (
    id_agregado BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    id_ciudad INT UNSIGNED NOT NULL,
    id_fuente INT UNSIGNED NOT NULL,
    id_segmento INT UNSIGNED NULL,

    fecha_inicio DATETIME NOT NULL,
    fecha_fin DATETIME NOT NULL,

    nivel_agregacion VARCHAR(50) NOT NULL,
    metrica VARCHAR(100) NOT NULL,
    valor_agregado DECIMAL(18,6) NOT NULL,

    cantidad_observaciones INT UNSIGNED NOT NULL,

    CONSTRAINT fk_agregado_ciudad
        FOREIGN KEY (id_ciudad)
        REFERENCES dim_ciudad(id_ciudad),

    CONSTRAINT fk_agregado_fuente
        FOREIGN KEY (id_fuente)
        REFERENCES dim_fuente(id_fuente),

    CONSTRAINT fk_agregado_segmento
        FOREIGN KEY (id_segmento)
        REFERENCES dim_segmento(id_segmento),

    CONSTRAINT chk_agregado_fecha
        CHECK (fecha_fin >= fecha_inicio)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;