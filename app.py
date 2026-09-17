from flask import Flask
import socket

app = Flask(__name__)

# Contador global, fuera de las funciones
visitas = 0

@app.route('/')
def index():
    global visitas
    visitas += 1
    return {
        "visitas": visitas,
        "servidor": socket.gethostname()
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)