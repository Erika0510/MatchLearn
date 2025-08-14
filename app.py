from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS 
 #flask framework para construir aplicaciones web en Python.

 #request: accede a los datos que llegan en una petición 
 # (por ejemplo, el JSON con nombre, correo y contraseña).

#jsonify: convierte respuestas de Python a JSON.

#sqlite3: se usa para manejar la base de datos usuarios.db



app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir peticiones desde otras fuentes 
#CORS(app): permite que el frontend (en otro dominio o puerto) pueda hacer peticiones al backend.

# Función para inicializar la base de datos
def init_db():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Ruta para registrar un nuevo usuario
@app.route('/registrarse', methods=['POST'])
def registrar():
    data = request.get_json()

    # Validación básica de campos
    nombre = data.get('nombre', '').strip()
    correo = data.get('correo', '').strip()
    contrasena = data.get('contrasena', '').strip()

    if not nombre or not correo or not contrasena:
        return jsonify({"success": False, "message": "Todos los campos son obligatorios."}), 400

    try:
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, correo, contrasena) VALUES (?, ?, ?)",
                       (nombre, correo, contrasena))
        conn.commit()
        return jsonify({"success": True})
    
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "El correo ya está registrado."}), 409
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        conn.close()


@app.route('/iniciarsesion', methods=['POST'])
def iniciar_sesion():
    data = request.get_json()
    correo = data.get('correo')
    contrasena = data.get('contrasena')

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE correo = ? AND contrasena = ?", (correo, contrasena))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        return jsonify({"success": True, "nombre": usuario[1]}) 
    else:
        return jsonify({"success": False, "message": "Correo o contraseña incorrectos."})

# Punto de entrada principal
if __name__ == '__main__':
    init_db()  
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__== '_main_':
    print("Iniciando servidor Flask...")
    init_db()
    app.run(debug=True)
