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

#Ruta guardar jugador nuevo
@app.route('/jugador', methods=['POST'])
def guardarJugador():
    #Obtener valores introducidos
    nombre = request.form['nombre']
    puntos = request.form['puntos']
    exacto = request.form['exacto']
    dobles = request.form['dobles']
    #Añadir jugador
    jugadores.inserta_jugador(nombre,puntos,exacto, dobles, "Insular")
    #Sacar los datos
    return redirect(url_for('home'))

#Lanzar la app
if __name__ == '__main__':
    app.run(debug=True, port=4000)