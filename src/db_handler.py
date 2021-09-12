import pymongo


class DBHandler:
    def __init__(self, database, users_collection, messages_collection):
        self._client = pymongo.MongoClient("mongodb://localhost:27017/")
        self._db = self._client[database]
        self.users_collection = self._db[users_collection]
        self.messages_collection = self._db[messages_collection]

    def get_item(self, collection, query):
        pass

    @staticmethod
    def add_item(collection, new_document):
        result = collection.insert_one(new_document)
        return result.inserted_id

    @staticmethod
    def get_all_items(collection, query={}):
        data = []
        cursor = collection.find(query, {"id": 0})
        for item in cursor:
            data.append(item)
        return data

    def delete_item(self, collection, query):
        pass
