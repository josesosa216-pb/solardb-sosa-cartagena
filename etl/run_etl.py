import os
import subprocess
import sys
from pathlib import Path

import psycopg2

RAIZ = Path(__file__).resolve().parent.parent  # carpeta del proyecto


def leer_env():
    """Lee el archivo .env y guarda sus datos como variables de entorno."""
    for linea in (RAIZ / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in linea and not linea.startswith("#"):
            clave, valor = linea.split("=", 1)
            os.environ[clave.strip()] = valor.strip()


def main():
    leer_env()

    # 1. Generar las lecturas con el simulador
    subprocess.run([sys.executable, str(RAIZ / "etl" / "simulador.py")], check=True, cwd=RAIZ)

    # 2. Conectar a PostgreSQL
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )
    cur = conn.cursor()

    # 3. Abrir la bitácora: una fila nueva con estado EN_CURSO
    cur.execute(
        "INSERT INTO etl_log (proceso, estado) "
        "VALUES ('carga_lecturas_demo', 'EN_CURSO') RETURNING id"
    )
    log_id = cur.fetchone()[0]
    conn.commit()

    try:
        # 4. Vaciar la bandeja y cargar cada línea del archivo
        cur.execute("TRUNCATE stg_lectura_raw")
        with open(RAIZ / "data" / "lecturas.jsonl", encoding="utf-8") as f:
            lineas = [l.strip() for l in f if l.strip()]
        for linea in lineas:
            cur.execute("INSERT INTO stg_lectura_raw (payload) VALUES (%s)", (linea,))
        leidas = len(lineas)

        # 5. Transformar y cargar a lectura_demo (usa tu archivo 02_carga.sql)
        cur.execute((RAIZ / "sql" / "02_carga.sql").read_text(encoding="utf-8"))
        cargadas = cur.rowcount
        rechazadas = leidas - cargadas

        # 6. Cerrar la bitácora con el resultado
        cur.execute(
            "UPDATE etl_log SET fin = now(), filas_leidas = %s, "
            "filas_cargadas = %s, filas_rechazadas = %s, estado = 'OK' WHERE id = %s",
            (leidas, cargadas, rechazadas, log_id),
        )
        conn.commit()
        print(f"ETL OK | leidas: {leidas} | cargadas: {cargadas} | rechazadas: {rechazadas}")

    except Exception as error:
        conn.rollback()  # deshace lo que quedó a medias
        cur.execute(
            "UPDATE etl_log SET fin = now(), estado = 'ERROR', error = %s WHERE id = %s",
            (str(error), log_id),
        )
        conn.commit()
        print("ETL con ERROR:", error)

    finally:
        conn.close()


if __name__ == "__main__":
    main()