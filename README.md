# CHAT-API:

El proyecto consiste en crear una api, y colocarla en una base de datos; en nuestro caso será Mongodb

Los puntos que se nos pide es: 


- Crear un usuario:
```python
def create_user():
username = request.json['username']
email = request.json['email']
password = request.json['password']
if username and email and password: 
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
```

- Crear un chat y añadir los usarios:
```python
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
```

Me ha quedado pendiente adjuntar mensajes al grupo, lo añadiré en un futuro.