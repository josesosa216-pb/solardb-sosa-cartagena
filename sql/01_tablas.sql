CREATE TABLE stg_lectura_raw (
    id BIGSERIAL PRIMARY KEY,
    payload JSONB NOT NULL,
    cargado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE lectura_demo (
    dispositivo_id INT NOT NULL,
    ts TIMESTAMPTZ NOT NULL,
    p_ac NUMERIC(10,3) CHECK (p_ac >= 0),
    irradiancia NUMERIC(8,1) CHECK (irradiancia BETWEEN 0 AND 1500),
    temp_modulo NUMERIC(5,1),
    payload JSONB,
    PRIMARY KEY (dispositivo_id, ts)
);

CREATE TABLE etl_log (
    id BIGSERIAL PRIMARY KEY,
    proceso TEXT NOT NULL,
    inicio TIMESTAMPTZ NOT NULL DEFAULT now(),
    fin TIMESTAMPTZ,
    filas_leidas INT,
    filas_cargadas INT,
    filas_rechazadas INT,
    estado TEXT NOT NULL CHECK (estado IN ('EN_CURSO', 'OK', 'ERROR')),
    error TEXT
);