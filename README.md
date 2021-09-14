# messaging-system
Backend system that is responsible for handling messages between users

# Login route to authenticate users in GET methods and return JWTs.
@app.route("/login", methods=["POST"])
In order to login, the request should contain the following json: {"username": <username>, "password": <password>} 
the response is with the access_token that is authenticated the GET method for this username: 
{"access_token": <jwt>}

# Write message
@app.route('/message', methods=['POST'])
In order to write message, the request should contain the following json: 
{"Sender": <sender>, "Receiver": <receiver>, "Message": <message>, "Subject": <subject>}

# Get all messages
@app.route('/messages', methods=['GET'])
return a valid response only for the current user that give valid access token that was in the response when the
current user login.
In the response there is also the 'message_id' value for get_one_message and delete_one_message

# Get all unread messages
@app.route('/unread_messages', methods=['GET'])
return a valid response only for the current user that give valid access token that was in the response when the
current user login
In the response there is also the 'message_id' value for get_one_message and delete_one_message

# Get one message according to specific message_id and current user
@app.route('/message/<message_id>', methods=['GET'])
return a valid response only for the current user that give valid access token that was in the response when the
current user login, also this message will mark as read

# Delete specific message according to specific message_id
@app.route('/message/<message_id>', methods=['DELETE'])
