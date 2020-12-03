# CHAT-API:

El proyecto consiste en crear una api, y colocarla en una base de datos; en nuestro caso será Mongodb.

Para introducir los datos en la API usaremos la aplicación POSTMAN: https://www.postman.com/

Iremos paso a paso:

Primero escribimos una función para crear un usuario, usando el metodo 'POST':
- Para ellos pedimos un nombre de usuario, un email y una contraseña; la contraseña la encriptaremos con el metodo "generate_passwor_hash".
- Una vez elegido los datos del usuario, la función generará un ID automáticamente.
```python
@app.route('/chats', methods=['POST'])
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
Con la función anterior creamos tantos usuarios como queramos, y para poder consultar los usuarios de nuestra aplicaciones tenemos dos opciones, usando la el metodo 'GET'.
Uno para ver todos los usuraios y otro para filtrar por el ID:
```python
@app.route('/chats',methods=['GET'])

@app.route('/chats/<id>', methods=['GET'])

## La función completa se encuentra en el código
```
También añadimos otras funciones para modificar ['PUT'] o borrar ['DELETE'] los usuarios:
```python
@app.route('/chats/<id>', methods=['DELETE']) 

@app.route('/chats/<_id>', methods=['PUT'])

## La función completa se encuentra en el código
```
Con todos los usarios, y sus diferentes metodos, el siguiente paso es crear los chats, prácticamente siguiendo la misma estructura que con los usuarios.

- Creamos un chat y añadir los usarios:

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

Me ha quedado pendiente adjuntar mensajes al grupo, y analizarlos con NPL; lo añadiré en un futuro.