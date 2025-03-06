from flask import Flask, render_template, request, redirect, url_for
import os
from database import Clasificacion

####################################################################
#Código sacado del video https://www.youtube.com/watch?v=Zfpbnmdi-pE
####################################################################

#Definir el html
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
#Unirlo a la carpeta de proyecto
template_dir = os.path.join(template_dir, 'src', 'templates')
#Variable flask
app = Flask(__name__, template_folder = template_dir)
# Instanciar la base de datos
jugadores = Clasificacion()

#Ruta vista inicial
@app.route('/')
def home():
    #Obtener datos de la clasificacion
    clasificacion = jugadores.consulta_clasificacion()
    #Sacar los datos
    return render_template('index.html', clasificacion=clasificacion)

#Ruta botón guardar
@app.route('/guardar', methods=['POST'])
def guardarJugador():
    #Obtener valores introducidos
    accion = request.form['accion']
    nombre = request.form['nombre']
    puntos = request.form['puntos']
    exacto = request.form['exacto']
    dobles = request.form['dobles']
    # Insertar nuevo jugador
    if accion == "nuevo":     
        jugadores.inserta_jugador(nombre, puntos, exacto, dobles, "Insular")
    # Modificar jugador existente
    elif accion == "modificar":
        jugadores.modifica_jugador(nombre, puntos, exacto, dobles, "Insular")
    #Sacar los datos
    return redirect(url_for('home'))

#Ruta botón eliminar
@app.route('/eliminar/<string:nombre>', methods=['DELETE'])
def eliminarJugador(nombre):
    try:
        jugadores.elimina_jugador(nombre)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}, 500
    
#Ruta botón ordernar
@app.route('/ordenar', methods=['POST'])
def ordenarClasificacion():
    try:
        jugadores.ordena_clasificacion("Puntos_Insular", "Exacto_Insular")
        return redirect(url_for('home'))
    except Exception as e:
        return {"success": False, "error": str(e)}, 500

#Lanzar la app
if __name__ == '__main__':
    app.run(debug=True, port=4000)