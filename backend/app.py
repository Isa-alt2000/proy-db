from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Configuración de PostgreSQL (ajusta con tu password real)
DB_CONFIG = {
    "host": "localhost",
    "database": "proyecto_db",
    "user": "isa_admin",
    "password": "tu_password_seguro",  # ¡Cambia esto!
    "port": 5432
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Ruta para agregar usuarios desde el formulario HTML
@app.route('/api/usuarios', methods=['POST'])
def agregar_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')

    if not nombre or not correo:
        return jsonify({"error": "Nombre y correo son obligatorios"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            sql.SQL("INSERT INTO usuarios (nombre, correo) VALUES (%s, %s) RETURNING id, nombre, correo"),
            [nombre, correo]
        )
        nuevo_usuario = cursor.fetchone()
        conn.commit()
        return jsonify({
            "id": nuevo_usuario[0],
            "nombre": nuevo_usuario[1],
            "correo": nuevo_usuario[2]
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Ruta para obtener todos los usuarios (mostrar en cuadros DIV)
@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY id DESC")  # Ordenados por los más recientes primero
        usuarios = cursor.fetchall()
        return jsonify([
            {"id": u[0], "nombre": u[1], "correo": u[2]} for u in usuarios
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)