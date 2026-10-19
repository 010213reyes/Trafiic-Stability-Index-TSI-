USE tsi_db;

CREATE TABLE IF NOT EXISTS dim_fuente (
    id_fuente INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  id_ciudad INT UNSIGNED NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    tipo_fuente VARCHAR(50) NOT NULL,
    descripcion TEXT NULL,
    rol_proyecto VARCHAR(50) NULL,
    unidad_original VARCHAR(50) NULL,
    origen_url TEXT NULL,
    frecuencia_documentada VARCHAR(100) NULL,

    CONSTRAINT fk_fuente_ciudad
      FOREIGN KEY (id_ciudad)
      REFERENCES dim_ciudad(id_ciudad),

    CONSTRAINT uq_fuente
        UNIQUE (id_ciudad, nombre)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;