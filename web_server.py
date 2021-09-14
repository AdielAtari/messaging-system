from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, get_jwt_identity, create_access_token, jwt_required

from datetime import datetime
import uuid
from http import HTTPStatus
import werkzeug.exceptions as werkzeug_exceptions

from db_handler import DBHandler

# Initiate db_handler
db_instance = DBHandler(database='messaging-system', users_collection='users', messages_collection='messages')


app = Flask(__name__)
app.url_map.strict_slashes = False


# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


# endpoint foe heartbeat of the app
@app.route('/heartbeat')
def is_alive():
    return 'app alive!'


@app.route("/logging", methods=["POST"])
def logging():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


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
    try:
        is_username_exit = db_instance.get_item(collection=db_instance.users_collection, query={"username": username})
    except Exception as ex:
        return werkzeug_exceptions.InternalServerError(f'Failed to get user from DB, exception: {str(ex)}')
    if is_username_exit:
        return werkzeug_exceptions.Unauthorized(f'Username already exist, choose another one')

    # create token for new user
    access_token = create_access_token(identity=username, expires_delta=False)

    # Add new user to DB
    if not db_instance.add_item(collection=db_instance.users_collection, new_document=login_data):
        return werkzeug_exceptions.InternalServerError(f'Failed to add user: {username} to DB')
    return jsonify(access_token=access_token), HTTPStatus.OK


@app.route('/message', methods=['POST'])
def write_message():
    # Get data from user to login
    new_message = request.get_json(silent=True)
    if not new_message:
        return werkzeug_exceptions.BadRequest(f'Not a valid message provided as json to login, '
                                              f'login_data: {new_message}')
    # Get Sender, Receiver, Message, Subject
    sender = new_message.get("Sender", None)
    receiver = new_message.get("Receiver", None)
    message = new_message.get("Message", None)
    subject = new_message.get("Subject", None)
    # In case one of Sender, Receiver, Message, Subject does not exit in request not a valid request
    if not sender or not receiver or not message or not subject:
        return werkzeug_exceptions.BadRequest(f'One of Sender, Receiver, Message, Subject was not provided in json, '
                                              f'new_message: {new_message}')

    # Add field 'message_id' and 'creation_date' to the new message
    message_id = str(uuid.uuid4())
    creation_date = datetime.utcnow()
    new_message.update({"message_id": message_id, "creation_date": creation_date, "unread": True})

    # Add new message to DB
    if not db_instance.add_item(collection=db_instance.messages_collection, new_document=new_message):
        return werkzeug_exceptions.InternalServerError(f'Failed to add new message to DB: {new_message}')
    del new_message['_id']
    return jsonify(new_message=new_message), HTTPStatus.CREATED


@app.route('/messages', methods=['GET'])
@jwt_required()
def get_all_messages():
    # Get the identity of the current user
    current_user = get_jwt_identity()

    # Filter only messages that the current user is the 'Receiver'
    current_user_messages = db_instance.get_all_items(collection=db_instance.messages_collection,
                                                      query={"Receiver": current_user})
    return jsonify(messages=current_user_messages), HTTPStatus.OK


@app.route('/unread_messages', methods=['GET'])
@jwt_required()
def get_all_unread_messages():
    # Get the identity of the current user
    current_user = get_jwt_identity()

    # Filter only unread messages that the current user is the 'Receiver' a
    current_user_unread_messages = db_instance.get_all_items(collection=db_instance.messages_collection,
                                                             query={"Receiver": current_user, "unread": True})
    return jsonify(messages=current_user_unread_messages), HTTPStatus.OK


@app.route('/message/<message_id>', methods=['GET'])
@jwt_required()
def get_one_message(message_id):
    # Get the identity of the current user
    current_user = get_jwt_identity()

    # Filter message for the current user is the 'Receiver' and message_id
    query = {"Receiver": current_user, "message_id": message_id}
    current_user_unread_messages = db_instance.get_item(collection=db_instance.messages_collection, query=query,
                                                        field_obj={"unread": 0})

    if not current_user_unread_messages:
        return werkzeug_exceptions.NotFound(f'Not found the requested message_id: {message_id}')
    # Update the message as read message
    update_data = {"$set": {"unread": False}}
    db_instance.update_item(collection=db_instance.messages_collection, query=query, update_data=update_data)

    return jsonify(message=current_user_unread_messages), HTTPStatus.OK


@app.route('/message/<message_id>', methods=['DELETE'])
def delete_one_message(message_id):
    # Delete message from DB
    res = db_instance.delete_item(collection=db_instance.messages_collection, query={"message_id": message_id})

    # Failed to delete message from DB
    if not isinstance(res, int) or res == 0:
        return werkzeug_exceptions.InternalServerError(f'Failed to delete message_id : {message_id}')

    return jsonify(deleted_message=res), HTTPStatus.OK
