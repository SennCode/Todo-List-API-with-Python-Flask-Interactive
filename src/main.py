"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Tarea
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# USER 

@app.route('/user', methods=['POST'])
def crear_usuario():
    body = request.get_json()
    if body is None:
        return "Error"
    
    email = body.get('email')
    password = body.get('password')
    if email is None or password is None:
        return "Valores incorrectos!"

    user = User(
        email = email, 
        password = password,
        is_active = True
    )

    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize())


@app.route('/user/list', methods=['GET'])
def listar_usuario():
    usuarios = User.query.all()
    print(usuarios)

    res = []
    for usuario in usuarios:
        res.append(usuario.serialize())

    return jsonify(res)


#TAREAS
@app.route('/todos', methods=['GET'])
def lista_tareas():
    tareas = Tarea.query.all()
    res = []
    for tarea in tareas:
        tarea.append(tarea.serialize())

    return jsonify(res)

@app.route('/todos', methods=['POST'])
def tarea_nueva():
    body = request.get_json()
    #validar body is not None

    tarea = Tarea(
        tittle = body["title"], #validar
        user_id = body["user_id"],#validar
    )

    db.session.add(tarea)
    db.session.commit()

    return jsonify(tarea)

@app.route('/todos/<int:position>', methods=['DELETE'])
def eliminar_tarea(position):
    resultado = None
    for tarea in TAREAS:
        resultado = tarea
        break
    # if resultado != None:
    #     TAREAS.remove(resultado)
    return "jsonify(TAREAS)"

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
