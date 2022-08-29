from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId #used to generate random string id

from flask import  jsonify, request

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/users'

mongo = PyMongo(app)

@app.route('/add', methods=['POST'])
def add_user():
    __json = request.json
    _name = __json['name']
    _age = __json['age']
    _gender = __json['gender']
    _email = __json['email']

    if _name and _age and _gender and _email and request.method == 'POST':
        id = mongo.db.user_data.insert({'name':_name, 'age':_age, 'gender':_gender, 'email':_email})
        responce = jsonify('User Added Successfully')
        responce.status_code = 200
        return responce

    else:
        return not_found()

@app.route('/users')
def users():
    users = mongo.db.user_data.find()
    responce = dumps(users)
    return responce

@app.route('/user/<id>')
def user_byid(id):
    user = mongo.db.user_data.find_one({'_id' : ObjectId(id)})
    responce = dumps(user)
    return responce

@app.route('/delete/<id>')
def user_delete(id):
    mongo.db.user_data.delete_one({'_id' : ObjectId(id)})
    responce = jsonify("User Deleted Successfully")
    responce.status_code = 200
    return responce


@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    _id = id
    __json = request.json
    _name = __json['name']
    _age = __json['age']
    _gender = __json['gender']
    _email = __json['email']

    if _name and _age and _gender and _email and request.method == 'PUT':
        mongo.db.user_data.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name, 'age':_age, 'gender':_gender, 'email':_email}})
        responce = jsonify('User Updated Successfully')
        responce.status_code = 200
        return responce

    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message':'Not Found' + request.url
    }
    responce = jsonify(message)
    responce.status_code = 404
    return responce


if __name__ == "__main__":
    app.run(debug=True)