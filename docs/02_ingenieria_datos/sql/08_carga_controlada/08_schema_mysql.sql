CREATE DATABASE IF NOT EXISTS tsi_international
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE tsi_international;

CREATE TABLE IF NOT EXISTS dim_ciudad (
    ciudad_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    pais VARCHAR(100) NOT NULL,
    region VARCHAR(100) NULL,
    zona_horaria VARCHAR(64) NOT NULL,
    es_ciudad_objetivo BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (ciudad_id),
    UNIQUE KEY uk_ciudad_nombre_pais (nombre, pais)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS dim_fuente (
    fuente_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    ciudad_id INT UNSIGNED NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    tipo_fuente VARCHAR(50) NOT NULL,
    origen_url TEXT NULL,
    licencia VARCHAR(255) NULL,
    rol_dato VARCHAR(40) NOT NULL,
    es_real BOOLEAN NOT NULL,
    fecha_inicio DATE NULL,
    fecha_fin DATE NULL,
    frecuencia_documentada VARCHAR(100) NULL,
    PRIMARY KEY (fuente_id),
    UNIQUE KEY uk_fuente_ciudad_nombre (ciudad_id, nombre),
    CONSTRAINT fk_fuente_ciudad FOREIGN KEY (ciudad_id) REFERENCES dim_ciudad (ciudad_id)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS dim_segmento (
    segmento_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    ciudad_id INT UNSIGNED NOT NULL,
    fuente_id INT UNSIGNED NOT NULL,
    codigo_segmento VARCHAR(150) NOT NULL,
    nombre_segmento VARCHAR(255) NULL,
    tipo_via VARCHAR(50) NOT NULL,
    latitud DOUBLE NULL,
    longitud DOUBLE NULL,
    PRIMARY KEY (segmento_id),
    UNIQUE KEY uk_segmento_fuente_codigo (fuente_id, codigo_segmento),
    KEY ix_segmento_ciudad (ciudad_id),
    CONSTRAINT chk_segmento_latitud CHECK (latitud IS NULL OR latitud BETWEEN -90 AND 90),
    CONSTRAINT chk_segmento_longitud CHECK (longitud IS NULL OR longitud BETWEEN -180 AND 180),
    CONSTRAINT fk_segmento_ciudad FOREIGN KEY (ciudad_id) REFERENCES dim_ciudad (ciudad_id),
    CONSTRAINT fk_segmento_fuente FOREIGN KEY (fuente_id) REFERENCES dim_fuente (fuente_id)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS fact_observaciones (
    observacion_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `timestamp` DATETIME(6) NOT NULL,
    ciudad_id INT UNSIGNED NOT NULL,
    fuente_id INT UNSIGNED NOT NULL,
    segmento_id BIGINT UNSIGNED NOT NULL,
    metrica_principal VARCHAR(50) NOT NULL,
    valor_principal DOUBLE NOT NULL,
    velocidad_kmh DOUBLE NULL,
    flujo_veh_h DOUBLE NULL,
    ocupacion_pct DOUBLE NULL,
    densidad_veh_km DOUBLE NULL,
    tiempo_viaje_seg DOUBLE NULL,
    congestion_longitud_m DOUBLE NULL,
    indice_congestion DOUBLE NULL,
    intensidad_fuente DOUBLE NULL,
    carga_fuente DOUBLE NULL,
    vmed_fuente DOUBLE NULL,
    calidad_registro VARCHAR(20) NOT NULL,
    PRIMARY KEY (observacion_id),
    KEY ix_fact_timestamp (`timestamp`),
    KEY ix_fact_ciudad_timestamp (ciudad_id, `timestamp`),
    KEY ix_fact_fuente_timestamp (fuente_id, `timestamp`),
    KEY ix_fact_segmento_timestamp (segmento_id, `timestamp`),
    KEY ix_fact_metrica_timestamp (metrica_principal, `timestamp`),
    CONSTRAINT chk_fact_ocupacion CHECK (ocupacion_pct IS NULL OR ocupacion_pct BETWEEN 0 AND 100),
    CONSTRAINT chk_fact_tiempo_viaje CHECK (tiempo_viaje_seg IS NULL OR tiempo_viaje_seg >= 0),
    CONSTRAINT chk_fact_congestion CHECK (congestion_longitud_m IS NULL OR congestion_longitud_m >= 0),
    CONSTRAINT fk_fact_ciudad FOREIGN KEY (ciudad_id) REFERENCES dim_ciudad (ciudad_id),
    CONSTRAINT fk_fact_fuente FOREIGN KEY (fuente_id) REFERENCES dim_fuente (fuente_id),
    CONSTRAINT fk_fact_segmento FOREIGN KEY (segmento_id) REFERENCES dim_segmento (segmento_id)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS calidad_observacion (
    calidad_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    observacion_id BIGINT UNSIGNED NOT NULL,
    tipo_problema VARCHAR(50) NOT NULL,
    descripcion TEXT NOT NULL,
    severidad VARCHAR(20) NOT NULL,
    fecha_revision DATETIME(6) NOT NULL,
    PRIMARY KEY (calidad_id),
    KEY ix_calidad_observacion (observacion_id),
    CONSTRAINT fk_calidad_observacion FOREIGN KEY (observacion_id) REFERENCES fact_observaciones (observacion_id)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS fact_agregado (
    agregado_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    ciudad_id INT UNSIGNED NOT NULL,
    fuente_id INT UNSIGNED NOT NULL,
    segmento_id BIGINT UNSIGNED NULL,
    periodo_inicio DATETIME(6) NOT NULL,
    periodo_fin DATETIME(6) NOT NULL,
    metrica VARCHAR(50) NOT NULL,
    valor_agregado DOUBLE NOT NULL,
    cantidad_observaciones INT UNSIGNED NOT NULL,
    PRIMARY KEY (agregado_id),
    KEY ix_agregado_ciudad_periodo (ciudad_id, periodo_inicio),
    KEY ix_agregado_fuente_periodo (fuente_id, periodo_inicio),
    KEY ix_agregado_segmento_periodo (segmento_id, periodo_inicio),
    CONSTRAINT fk_agregado_ciudad FOREIGN KEY (ciudad_id) REFERENCES dim_ciudad (ciudad_id),
    CONSTRAINT fk_agregado_fuente FOREIGN KEY (fuente_id) REFERENCES dim_fuente (fuente_id),
    CONSTRAINT fk_agregado_segmento FOREIGN KEY (segmento_id) REFERENCES dim_segmento (segmento_id)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS log_cargas (
    carga_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    fuente_id INT UNSIGNED NULL,
    archivo_origen VARCHAR(500) NOT NULL,
    fecha_inicio DATETIME(6) NOT NULL,
    fecha_fin DATETIME(6) NULL,
    filas_leidas BIGINT UNSIGNED NOT NULL DEFAULT 0,
    filas_insertadas BIGINT UNSIGNED NOT NULL DEFAULT 0,
    filas_rechazadas BIGINT UNSIGNED NOT NULL DEFAULT 0,
    estado VARCHAR(20) NOT NULL,
    mensaje TEXT NULL,
    PRIMARY KEY (carga_id),
    KEY ix_log_cargas_fuente (fuente_id),
    CONSTRAINT fk_log_cargas_fuente FOREIGN KEY (fuente_id) REFERENCES dim_fuente (fuente_id)
) ENGINE = InnoDB;