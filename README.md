# SolarDB Pascual — Consulta Bases de Datos I

> An idempotent ETL pipeline that loads simulated IoT telemetry into a governed PostgreSQL repository, versioned on GitHub.

**Integrante:** Jose Miguel Sosa Cartagena 
**Curso / Grupo:** Bases de Datos I (SD1006) · Grupo 811 · Semestre 2026-II
**Institución:** Institución Universitaria Pascual Bravo
**Docente:** Ramiro Grisales Montoya

## Descripción

Primer pipeline de ingesta del proyecto SolarDB Pascual. Un simulador genera lecturas JSON de dos inversores, el ETL las carga a una tabla de staging (`stg_lectura_raw`, columna JSONB) y de allí pasan a la tabla relacional `lectura_demo`. La carga es idempotente (`INSERT ... ON CONFLICT DO NOTHING`), deja una bitácora en `etl_log` y la base tiene un rol de solo lectura (`solar_lector`).

## Estructura

- `data/` lecturas.jsonl de muestra
- `etl/` simulador.py y run_etl.py
- `sql/` 01_tablas.sql, 02_carga.sql, 03_roles.sql
- `docs/` PDF de la consulta

## Requisitos

- PostgreSQL 15 o superior
- Python 3
- `pip install psycopg2-binary`

## Pasos para reproducir la práctica

1. Clonar el repositorio.
2. En PostgreSQL, crear la base: `CREATE DATABASE solardb;`
3. Ejecutar `sql/01_tablas.sql` sobre `solardb` para crear las tablas.
4. Crear en la carpeta principal un archivo `.env` (no se sube a GitHub) con estas variables:
```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=solardb
   DB_USER=postgres
   DB_PASSWORD=tu_contraseña
```
5. Ejecutar el flujo completo con un solo comando: `python etl/run_etl.py`
6. Ejecutarlo una segunda vez para comprobar la idempotencia: el total de `lectura_demo` sigue en 288.
7. Ejecutar `sql/03_roles.sql` para crear los roles.

## Automatización (no implementada)

- cron: `0 * * * * cd /ruta/del/proyecto && python etl/run_etl.py`
- Programador de tareas de Windows: repetir cada 1 hora, programa `python`, argumentos `etl\run_etl.py`, iniciar en la carpeta del proyecto.

## Quién hizo qué

| Integrante | Tareas |
|---|---|
| Jose Miguel Sosa Cartagena | Simulador, scripts SQL, ETL, roles, README y documento de consulta |

## Seguridad

Las contraseñas no se suben al repositorio: se leen del archivo `.env`, que está excluido en `.gitignore`.
