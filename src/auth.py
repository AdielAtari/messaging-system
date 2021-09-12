
class Auth:
    def __init__(self, db):
        self._db = db

    def get_all_users(self):
        users = self._db.get_all_items(collection=self._db.users_collection)
        print(users)
        return users

    def add_user(self, user_data):
        if len(user_data) == 2 and 'username' in user_data and 'password' in user_data:
            inserted_id = self._db.add_item(collection=self._db.users_collection, new_document=user_data)
            return inserted_id

    def authentication_handler(self, username, password):
        users = self.get_all_users()
        for user in users:
            if username == user['username'] and password == user['password']:
                return user

    @staticmethod
    def identity_handler(payload):
        user_id = payload['identity']
        pass