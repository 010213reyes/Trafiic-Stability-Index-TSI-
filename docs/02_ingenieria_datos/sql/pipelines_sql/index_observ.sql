USE tsi_db;

CREATE INDEX idx_obs_timestamp
ON fact_observaciones(timestamp_observacion);

CREATE INDEX idx_obs_ciudad_fecha
ON fact_observaciones(id_ciudad, timestamp_observacion);

CREATE INDEX idx_obs_fuente_fecha
ON fact_observaciones(id_fuente, timestamp_observacion);

CREATE INDEX idx_obs_segmento_fecha
ON fact_observaciones(id_segmento, timestamp_observacion);