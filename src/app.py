from flask import Flask, render_template, request, redirect, url_for, jsonify
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
    #Obtener la opción seleccionada
    seleccion = request.form.get("opciones")
    # Ordenar la clasificación según la opción seleccionada
    if seleccion == "Insular":
        jugadores.ordena_clasificacion("Puntos_Insular", "Exacto_Insular")
    elif seleccion == "Regional":
        jugadores.ordena_clasificacion("Puntos_Regional", "Exacto_Regional")
    else:
        jugadores.ordena_clasificacion("Puntos_General", "Exacto_General")

    return redirect(url_for('home'))

#Ruta botón seleccionar
@app.route("/clasificacion/<tipo>")
def seleccionarClasificacion(tipo):
    #Obtener datos de la clasificacion
    datos = jugadores.consulta_clasificacion()
    clasificacion = []
    print("ENTRA AQUI 1")
    for row in datos:
        nombre = row[0]  #La primera columna es el nombre

        # Convertir valores None a 0
        p1 = row[1] if row[1] is not None else 0
        e1 = row[2] if row[2] is not None else 0
        d1 = row[3] if row[3] is not None else 0
        p2 = row[4] if row[4] is not None else 0
        e2 = row[5] if row[5] is not None else 0
        d2 = row[6] if row[6] is not None else 0

        if tipo == "Insular":
            puntos, exacto, dobles = p1, e1, d1
        elif tipo == "Regional":
            puntos, exacto, dobles = p2, e2, d2
        else:  #General
            puntos = p1 + p2
            exacto = e1 + e2
            dobles = d1 + d2

        clasificacion.append({"nombre": nombre, "puntos": puntos, "exacto": exacto, "dobles": dobles})

    return jsonify(clasificacion)

#Lanzar la app
if __name__ == '__main__':
    app.run(debug=True, port=4000)