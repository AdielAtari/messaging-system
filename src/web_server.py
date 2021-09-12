from flask import Flask, request, jsonify, send_file
from flask_jwt import JWT
import uuid
import os
from http import HTTPStatus
import werkzeug.exceptions

from db_handler import DBHandler
from auth import Auth
db_instance = DBHandler(database='messaging-system', users_collection='users', messages_collection='messages')
auth_instance = Auth(db_instance)

app = Flask(__name__)
app.secret_key = 'my secret key'

jwt = JWT(app=app, authentication_handler=Auth.authentication_handler, identity_handler=Auth.identity_handler)


@app.route('/heartbeat')
def is_alive():
    return 'app alive!'


@app.route('/message', methods=['POST'])
def write_message():
    pass


@app.route('/messages', methods=['GET'])
def get_all_messages():
    pass


@app.route('/unread_messages', methods=['GET'])
def get_all_unread_messages():
    pass


@app.route('/message', methods=['GET'])
def get_one_message():
    pass


@app.route('/message', methods=['DELETE'])
def delete_one_message():
    pass
