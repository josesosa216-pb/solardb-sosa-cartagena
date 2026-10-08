INSERT INTO lectura_demo (dispositivo_id, ts, p_ac, irradiancia, temp_modulo, payload)
SELECT
    (payload ->> 'device_id')::int,
    (payload ->> 'ts')::timestamptz,
    (payload ->> 'p_ac')::numeric,
    (payload ->> 'irradiancia')::numeric,
    (payload ->> 'temp_modulo')::numeric,
    payload
FROM stg_lectura_raw
ON CONFLICT (dispositivo_id, ts) DO NOTHING;