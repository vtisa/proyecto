from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
import psycopg2
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = 'una_clave_secreta_muy_segura'  # Necesario para usar flash y CSRF
csrf = CSRFProtect(app)

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

def eliminar_persona(dni):
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM personas WHERE dni = %s", (dni,))
            affected_rows = cursor.rowcount
            conn.commit()
            return affected_rows > 0
        except psycopg2.Error as e:
            print("Error al eliminar persona:", e)
            conn.rollback()
            return False
        finally:
            conn.close()
    return False

@app.route('/eliminar', methods=['POST'])
@csrf.exempt
def eliminar_registro():
    dni = request.form.get('dni')
    if dni and eliminar_persona(dni):
        flash('Registro eliminado con éxito', 'success')
    else:
        flash('Error al eliminar el registro', 'error')
    return redirect(url_for('administrar'))

@app.route('/administrar')
def administrar():
    registros = obtener_registros()
    return render_template('administrar.html', registros=registros)

# ... (resto del código permanece igual)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))    
    app.run(host='0.0.0.0', port=port, debug=True)