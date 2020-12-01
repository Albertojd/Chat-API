from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

### Inicia la aplicación y crea la base de datos
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/chat-api'
mongo = PyMongo(app)

### Damos la bienvenida a la API
@app.route("/", methods=['POST'])
def index():
    return {"Welcome to the API_project"}


### Creamos usuario
@app.route('/users', methods=['POST'])
def create_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    if username and email and password: # Si existen estas variables guardalas en la base de datos
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert(
            {'username': username, 'email': email, 'password': hashed_password})
        response = {
            '_id': str(id),
            'username': username,
            'password': hashed_password,
            'email': email
        }
        return response
    else:
        print("error, check your data")
    return{'message': 'received'}


### Creamos las peticiones para consultar el usuario
@app.route('/users',methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    print(id)
    user = mongo.db.users.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")


### Petición para borrar usuario
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response

### Petiticón para actualizar un usuario
@app.route('/users/<_id>', methods=['PUT'])
def update_user(_id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    if username and email and password and _id:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, 
            {'$set': {'username': username, 'email': email, 'password': hashed_password}})
        response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()

############ CHAT

### Creamos el chat
@app.route('/chats', methods=['POST'])
def create_chats():
    chatname = request.json['chatname']
    subject = request.json['subject']
    members = request.json['members'] 
    if chatname and subject and members:
        id = mongo.db.chats.insert({'chatname': chatname,
        "subject":subject, 'members': members})
        response = {'_id': str(id),
        "chatname": chatname,
        "subject":subject, 
        "members": members} 
        return response
    else:
        print("error, check your data")
    return{'message': 'received'}

### Peticiones para consultar los chats
@app.route('/chats',methods=['GET'])
def get_chats():
    chats = mongo.db.chats.find()
    response = json_util.dumps(chats)
    return Response(response, mimetype='application/json')

@app.route('/chats/<id>', methods=['GET'])
def get_chat(id):
    print(id)
    chat = mongo.db.chats.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(chat)
    return Response(response, mimetype="application/json")

### Petición para borrar chat
@app.route('/chats/<id>', methods=['DELETE'])
def delete_chat(id):
    mongo.db.chats.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Chat' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response

### Petición para actualizar el chat
@app.route('/chats/<_id>', methods=['PUT'])
def update_chat(_id):
    chatname = request.json['chatname']
    subject = request.json['subject']
    members = request.json['members'] 
    if chatname and subject and members and _id:
        mongo.db.chats.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, 
            {'$set': {'chatname': chatname, 'subject': subject, 'members': members}})
        response = jsonify({'message': 'chatname' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()

### Cuando ocurra un error 404, lo manejaremos con esta función
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response
if __name__ == "__main__":
    app.run(debug=True)