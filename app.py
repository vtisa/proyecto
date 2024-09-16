from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify
import psycopg2
import os

app = Flask(__name__, template_folder='templates')

# Configuración de la base de datos
DB_HOST = 'dpg-crk8f408fa8c7396nchg-a.oregon-postgres.render.com'
DB_NAME = 'nube1'
DB_USER = 'nube1_user'
DB_PASSWORD = 'Zgskprq80K2LLNcmc9c5Urx4FJR7ZX16'

def conectar_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        return conn
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

def crear_persona(dni, nombre, apellido, direccion, telefono):
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO personas (dni, nombre, apellido, direccion, telefono) VALUES (%s, %s, %s, %s, %s)",
                           (dni, nombre, apellido, direccion, telefono))
            conn.commit()
        except psycopg2.Error as e:
            print("Error al crear persona:", e)
            conn.rollback()
        finally:
            conn.close()

def obtener_registros():
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM personas ORDER BY apellido")
            registros = cursor.fetchall()
            return registros
        except psycopg2.Error as e:
            print("Error al obtener registros:", e)
            return []
        finally:
            conn.close()
    return []

def eliminar_persona(dni):
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM personas WHERE dni = %s", (dni,))
            conn.commit()
            return True
        except psycopg2.Error as e:
            print("Error al eliminar persona:", e)
            conn.rollback()
            return False
        finally:
            conn.close()
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    dni = request.form['dni']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    crear_persona(dni, nombre, apellido, direccion, telefono)
    return redirect(url_for('administrar'))

@app.route('/administrar')
def administrar():
    registros = obtener_registros()
    return render_template('administrar.html', registros=registros)

@app.route('/eliminar/<dni>', methods=['POST'])
def eliminar_registro(dni):
    if eliminar_persona(dni):
        return redirect(url_for('administrar'))
    else:
        return "Error al eliminar el registro", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))    
    app.run(host='0.0.0.0', port=port, debug=True)