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
    app.run(host='0.0.0.0', port=5000)