from flask import Flask, request, jsonify, send_file
# from flask_jwt import JWT
from flask_jwt_extended import JWTManager, get_jwt_identity, create_access_token, jwt_required


import uuid
import os
from http import HTTPStatus
import werkzeug.exceptions as werkzeug_exceptions

from db_handler import DBHandler
from auth import Auth
db_instance = DBHandler(database='messaging-system', users_collection='users', messages_collection='messages')
auth_instance = Auth(db_instance)

app = Flask(__name__)
app.url_map.strict_slashes = False
# app.secret_key = 'my secret key'

# jwt = JWT(app=app, authentication_handler=Auth.authentication_handler, identity_handler=Auth.identity_handler)


# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    # Get data from user to login
    login_data = request.get_json(silent=True)
    if not login_data:
        return werkzeug_exceptions.BadRequest(f'No username and password provided as json to login, '
                                              f'login_data: {login_data}')
    # Get username and password
    username = login_data.get("username", None)
    password = login_data.get("password", None)
    # In case one of password or username does not exit in request not a valid request
    if not username or not password:
        return werkzeug_exceptions.BadRequest(f'One of username or password was not provided in json to login, '
                                              f'login_data: {login_data}')

    # In case username already taken, not a valid request
    is_username_exit = db_instance.get_item(collection=db_instance.users_collection, query={"username": username})
    if is_username_exit:
        return werkzeug_exceptions.Unauthorized(f'Username already exist, choose another one')

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/heartbeat')
def is_alive():
    return 'app alive!'


@app.route('/message', methods=['POST'])
def write_message():
    pass


@app.route('/messages', methods=['GET'])
@jwt_required()
def get_all_messages():
    pass


@app.route('/unread_messages', methods=['GET'])
@jwt_required()
def get_all_unread_messages():
    pass


@app.route('/message', methods=['GET'])
def get_one_message():
    pass


@app.route('/message', methods=['DELETE'])
def delete_one_message():
    pass
