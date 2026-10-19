USE tsi_db;

CREATE TABLE IF NOT EXISTS fact_observaciones (
    id_observacion BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    id_ciudad INT UNSIGNED NOT NULL,
    id_fuente INT UNSIGNED NOT NULL,
    id_segmento INT UNSIGNED NOT NULL,

    timestamp_observacion DATETIME(6) NOT NULL,

    es_real BOOLEAN NOT NULL,

    calidad_registro VARCHAR(30) NOT NULL,
    periodo_integracion_min DECIMAL(8,2) NULL,

    metrica_principal VARCHAR(100) NOT NULL,
    valor_principal DECIMAL(18,6) NOT NULL,

    valor_fuente DECIMAL(18,6) NULL,

    velocidad_kmh DECIMAL(10,3) NULL,
    flujo_veh_h DECIMAL(12,3) NULL,
    ocupacion_pct DECIMAL(6,3) NULL,
    densidad_veh_km DECIMAL(12,3) NULL,
    tiempo_viaje_seg DECIMAL(12,3) NULL,
    congestion_longitud_m DECIMAL(14,3) NULL,
    indice_congestion DECIMAL(12,6) NULL,
    intensidad_fuente DECIMAL(14,3) NULL,
    carga_fuente DECIMAL(14,3) NULL,
    vmed_fuente DECIMAL(10,3) NULL,

    CONSTRAINT fk_obs_ciudad
        FOREIGN KEY (id_ciudad)
        REFERENCES dim_ciudad(id_ciudad),

    CONSTRAINT fk_obs_fuente
        FOREIGN KEY (id_fuente)
        REFERENCES dim_fuente(id_fuente),

    CONSTRAINT fk_obs_segmento
        FOREIGN KEY (id_segmento)
        REFERENCES dim_segmento(id_segmento),

    CONSTRAINT chk_obs_ocupacion
        CHECK (ocupacion_pct IS NULL OR ocupacion_pct BETWEEN 0 AND 100),

    CONSTRAINT chk_obs_velocidad
        CHECK (velocidad_kmh IS NULL OR velocidad_kmh >= 0),

    CONSTRAINT chk_obs_flujo
        CHECK (flujo_veh_h IS NULL OR flujo_veh_h >= 0),

    CONSTRAINT chk_obs_densidad
        CHECK (densidad_veh_km IS NULL OR densidad_veh_km >= 0),

    CONSTRAINT chk_obs_tiempo
        CHECK (tiempo_viaje_seg IS NULL OR tiempo_viaje_seg >= 0),

    CONSTRAINT chk_obs_longitud
        CHECK (congestion_longitud_m IS NULL OR congestion_longitud_m >= 0)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;