import os
import socket

import psycopg
from flask import Flask

app = Flask(__name__)

def leer_password():
    ruta = os.environ.get('DB_PASS_FILE')     # 1. ¿existe la variable?
    if ruta:                                  # 2. si existe...
        return open(ruta).read().strip()                           #    ...leé el archivo de esa ruta
    return os.environ.get('DB_PASS')          # 3. si no, fallback: como antes

def conectar():
    return psycopg.connect(
        host=os.environ.get('DB_HOST'),
        port=int(os.environ.get('DB_PORT')),
        user=os.environ.get('DB_USER'),
        dbname=os.environ.get('DB_NAME'),
        password = leer_password(),
    )




def init_db():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visitas (id INTEGER PRIMARY KEY, total INTEGER NOT NULL)")
    cur.execute("INSERT INTO visitas (id, total) VALUES (1, 0) ON CONFLICT (id) DO NOTHING")
    conn.commit()
    cur.close()
    conn.close()


@app.route('/')
def index():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("UPDATE visitas SET total = total + 1 WHERE id = 1 RETURNING total")
    total = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"visitas": total, "servidor": socket.gethostname()}


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)