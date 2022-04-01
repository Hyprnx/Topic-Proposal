import pymongo.errors
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.results import InsertOneResult
from bc import *
import datetime
from base import BaseClass

host = 'localhost'
port = 27017

client = MongoClient(host, port)

db = client.database

if not isinstance(db, Database):
    raise ConnectionError("Connection failed, respond is not a MongoDB Database instance")

class DatabaseManager:
    DB_NAME = None

    def check_status(self):
        database = db[self.DB_NAME]
        return database

    def insert_data(self, data=None):
        raise NotImplementedError('NOT IMPLEMENTED, CALL METHOD IN SUBCLASS')

    def query_data(self, data=None):
        raise NotImplementedError('NOT IMPLEMENTED, CALL METHOD IN SUBCLASS')

    def edit_data(self, data=None):
        raise NotImplementedError('NOT IMPLEMENTED, CALL METHOD IN SUBCLASS')


class DemoDatabaseManager(DatabaseManager):
    DB_NAME = 'demo'

    def insert_data(self, data=None, signer=None):
        try:
            prev_hash, prev_index = self._get_last_hash()
            element = Node(prev_hash=prev_hash, data=data, signer=signer, index=str(int(prev_index) + 1))
            respond = db[self.DB_NAME].insert_one(element.get_block_info())

        except IndexError:
            element = Node(prev_hash='0', data={'message': 'The first blockchain node'}, signer='To Duc Anh', index='0')
            respond = db[self.DB_NAME].insert_one(element.get_block_info())

        if not isinstance(respond, InsertOneResult):
            raise pymongo.errors.OperationFailure('Failed inserting data')

        return True

    def query_data(self, query=None):
        if not isinstance(query, dict):
            raise ValueError('Query must be a dictionary')
        yield db[self.DB_NAME].find(query)

    def find_random(self):
        return db[self.DB_NAME].find()

    def _get_last_hash(self):
        last_node = db[self.DB_NAME].find().sort('timestamp', -1)[0]
        return last_node['_id'], last_node['index']




    def __delete(self, query):
        if not isinstance(query, dict):
            raise ValueError('Query must be a dictionary')
        return db[self.DB_NAME].delete_many(query)


# class EmployeeManager(DatabaseManager):
#     DB_NAME = 'employee'


def main():
    mng = DemoDatabaseManager()
    blockchain_first_block = {
        'data': 'Hello, this is the first block in the blockchain',
        }

    # element = Node(prev_hash='0', data=blockchain_first_block, signer='To Duc Anh', index='0')
    #
    # print(element.get_block_info())

    print(mng.insert_data(data=blockchain_first_block, signer='To Duc Anh'))

    for i in mng.find_random():
        print(i)

    print(mng._get_last_hash())




if __name__ == '__main__':
    main()