from flask import Flask, render_template
import os

#Definir el html
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
#Unirlo a la carpeta de proyecto
template_dir = os.path.join(template_dir, 'src', 'templates')
#Variable flask
app = Flask(__name__, template_folder = template_dir)
#Rutas de la aplicación
@app.route('/')
def home():

    return render_template('index.html')

#Lanzar la app
if __name__ == '__main__':
    app.run(debug=True, port=4000)