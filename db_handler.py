from pymongo import MongoClient, DESCENDING
from pymongo.collection import Collection
from typing import Union


class DBHandler:
    def __init__(self, database, users_collection, messages_collection, mongo_address):
        self._client = MongoClient(host=mongo_address, serverSelectionTimeoutMS=10)
        self._db = self._client[database]
        self.users_collection = self._db[users_collection]
        self.messages_collection = self._db[messages_collection]
        # self.create_indexes()

    @staticmethod
    def get_item(collection: Collection, query: dict, field_obj: dict = None) -> Union[dict, None]:
        """
        :param collection: In which collection to find one document
        :param query: In order to find document
        :param field_obj: Optional parameter, can return or emmit only specified keys
        :return: One document if found otherwise None
        """
        projection = {'_id': 0}
        if field_obj:
            projection.update(field_obj)
        return collection.find_one(query, projection)

    @staticmethod
    def add_item(collection: Collection, new_document: dict) -> bool:
        """
        :param collection: In which collection to add the new document
        :param new_document: Document to add to specific collection
        :return: In case of success return True otherwise return False
        """
        result_inserted_id = collection.insert_one(new_document).inserted_id
        if result_inserted_id is None:
            return False
        return True

    @staticmethod
    def get_all_items(collection: Collection, query: dict = {}) -> list:
        """
        :param collection: In which collection to find documents
        :param query: In order to filter results
        :return: List of all matched document
        """
        data = list(collection.find(query, {"_id": 0, "unread": 0}).sort('_id', DESCENDING))
        return data

    @staticmethod
    def delete_item(collection: Collection, query: dict):
        """
        :param collection: In which collection to delete document
        :param query: In order to find document to delete
        :return: Instance of deleted document
        """
        res = collection.delete_one(query)
        return res.deleted_count

    @staticmethod
    def update_item(collection: Collection, query: dict, update_data: Union[dict, set, list]) -> bool:
        """
        :param collection: In which collection to update document
        :param query: In order to find document to update
        :param update_data: Data to update document
        :return: Bool depend on matched count
        """
        res = collection.update_one(query, update_data)
        return res.matched_count > 0
