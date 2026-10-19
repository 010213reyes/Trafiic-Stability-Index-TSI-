USE tsi_db;

CREATE TABLE IF NOT EXISTS log_cargas (
    id_carga BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_archivo VARCHAR(255) NOT NULL,
    id_fuente INT UNSIGNED NULL,
    fecha_inicio DATETIME NOT NULL,
    fecha_fin DATETIME NULL,
    registros_leidos BIGINT UNSIGNED NULL,
    registros_insertados BIGINT UNSIGNED NULL,
    registros_rechazados BIGINT UNSIGNED NULL,
    estado VARCHAR(30) NOT NULL,
    mensaje TEXT NULL,

    CONSTRAINT fk_log_fuente
        FOREIGN KEY (id_fuente)
        REFERENCES dim_fuente(id_fuente)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;