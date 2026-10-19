USE tsi_db;

CREATE TABLE IF NOT EXISTS calidad_observacion (
    id_calidad BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_observacion BIGINT UNSIGNED NOT NULL,

    estado VARCHAR(30) NOT NULL,
    porcentaje_completitud DECIMAL(6,3) NULL,
    tiene_valores_nulos BOOLEAN NULL,
    observaciones TEXT NULL,
    tipo_problema VARCHAR(50) NULL,
    severidad VARCHAR(20) NULL,
    fecha_revision DATETIME(6) NULL,

    CONSTRAINT fk_calidad_observacion
        FOREIGN KEY (id_observacion)
        REFERENCES fact_observaciones(id_observacion),

    CONSTRAINT chk_completitud
        CHECK (
            porcentaje_completitud IS NULL
            OR porcentaje_completitud BETWEEN 0 AND 100
        )
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;