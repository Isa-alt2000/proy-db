from flask import Flask, render_template, jsonify
import psycopg2

app = Flask(__name__)

# Configuración de la conexión a PostgreSQL
DB_HOST = "localhost"
DB_NAME = "proyecto_db"
DB_USER = "isa_admin"
DB_PASSWORD = "1234"
PORT = "5432"

def obtener_usuarios():
    try:
        conn = psycopg2.connect(
            host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=PORT,
        )
        cur = conn.cursor()
        cur.execute("SELECT nombre, correo FROM usuarios;")
        datos = cur.fetchall()
        cur.close()
        conn.close()
        return [{"nombre": nombre, "correo": correo} for nombre, correo in datos]
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/usuarios")
def usuarios():
    return jsonify(obtener_usuarios())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
