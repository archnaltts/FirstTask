import json
import jwt
from flask import Flask
from bson.json_util import dumps
from flask import  jsonify, request, make_response
from models import User
from validate import validate_user

app = Flask(__name__)

SECRET_KEY = '\x9f\xb0\xb5\x1c\x81(V\x9f\x00\xc0\xba\x1b\x16Y\xc5\x16\xc8;\xe5\xe8\xca\xaeJk'
app.config['SECRET_KEY'] = SECRET_KEY

JWT_SECRET = SECRET_KEY
JWT_ALGORITHM = "HS256"

@app.route('/')
def hello_app():
    return 'Hello'

@app.route("/api/v1/addusers/", methods=["POST"])
def add_user():
    try:
        user = request.json
        if not user:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        is_validated = validate_user(**user)
        if is_validated is not True:
            return dict(message='Invalid data', data=None, error=is_validated), 400
        user = User().create(**user)
        if not user:
            return {
                "message": "User already exists",
                "error": "Conflict",
                "data": None
            }, 409
        payload = {
            'user_id': user["_id"]}
        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        return {
            "message": "Successfully created new user and fetched auth token for current user",
            "user": json.loads(dumps(user)),
            "token" : jwt_token.decode('utf-8')
                }, 201
    except Exception as e:
        return {
               "message": "Something went wrong!",
               "error": str(e),
               "data": None
               }, 500

@app.route('/api/v1/users')
def users():
    users = User().get_all()
    response = dumps(users)
    return jsonify({
        "message": "successfully retrieved all users profile",
        "data": response
    })

@app.route('/api/v1/user/<id>')
def users_by_id(id):
    user = User().get_by_id(id)
    response = dumps(user)
    return jsonify({
        "message": "successfully retrieved user profile",
        "data": response
    })


@app.route('/api/v1/usertoken/<token>')
def users_by_token(token):
    id_from_token = jwt.decode(token,verify=False)
    user = User().get_by_id(id_from_token['user_id'])
    response = dumps(user)
    return jsonify({
        "message": "successfully retrieved user profile",
        "data": response
    })

@app.route('/api/v1/delete/<id>')
def user_delete(id):
    user = User().get_by_id(id)
    if user:
        User().delete(id)
        return jsonify({
            "message": "User Deleted Successfully",
        })
    else:
        return jsonify({
            "message": "User Not Exist or May be deleted",
        })

@app.route('/api/v1/update/<id>', methods=['PUT'])
def update_user(id):
    try:
        user = request.json

        is_validated = validate_user(**user)
        if is_validated is not True:
            return dict(message='Invalid data', data=None, error=is_validated), 400

        if user.get("name") and user.get("email") and user.get("age") and user.get("dob") and user.get("phone") :
            user = User().update(id, user["name"], user["email"], user["age"], user["dob"], user["phone"])
            return jsonify({
                "message": "successfully updated account",
                "data": user
            }), 201
        return {
            "message": "Invalid data",
            "data": None,
            "error": "Bad Request"
        }, 400
    except Exception as e:
        return jsonify({
            "message": "failed to update account",
            "error": str(e),
            "data": None
        }), 400

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
	app.run(debug=True, host='0.0.0.0')