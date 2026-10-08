CREATE ROLE solar_admin NOLOGIN;
CREATE ROLE solar_ingesta NOLOGIN;
CREATE ROLE solar_lector NOLOGIN;

GRANT ALL ON stg_lectura_raw, lectura_demo, etl_log TO solar_admin;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO solar_admin;

GRANT SELECT, INSERT, DELETE, TRUNCATE ON stg_lectura_raw TO solar_ingesta;
GRANT SELECT, INSERT ON lectura_demo TO solar_ingesta;
GRANT SELECT, INSERT, UPDATE ON etl_log TO solar_ingesta;
GRANT USAGE ON SEQUENCE stg_lectura_raw_id_seq, etl_log_id_seq TO solar_ingesta;

GRANT SELECT ON lectura_demo TO solar_lector;