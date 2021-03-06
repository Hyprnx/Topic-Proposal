import pymongo.errors
from pymongo.results import InsertOneResult
from bc import *
from base import BaseClass
from common.exceptions.Validation import ValidationException
from common.mongo_db_connect import connect_to_database

db = connect_to_database()


class DataManager(BaseClass):
    DB_NAME = None

    def __init__(self):
        super().__init__()

    def check_status(self):
        database = db[self.DB_NAME]
        return database

    def insert_data(self, data=None):
        raise NotImplementedError('NOT IMPLEMENTED, CALL METHOD IN SUBCLASS')

    def query_data(self, data=None):
        raise NotImplementedError('NOT IMPLEMENTED, CALL METHOD IN SUBCLASS')



class BlockChainManager(DataManager):
    DB_NAME = None

    def __init__(self):
        super().__init__()

    def insert_block(self, data=None, signer=None):
        self.log.info('Trying to insert data')
        try:
            prev_hash, prev_index = self._get_last_hash()
            element = Node(prev_hash=prev_hash, data=data, signer=signer, index=str(int(prev_index) + 1))
            respond = db[self.DB_NAME].insert_one(element.get_block_info())
        except IndexError:
            element = Node(prev_hash='0', data={'message': 'The first blockchain node'}, signer='To Duc Anh', index='0',
                           _block_hash='0')
            respond = db[self.DB_NAME].insert_one(element.get_block_info())

        self.log.info(respond)

        if not self.validate():
            raise ValidationException('Blockchain is corrupted')

        if not isinstance(respond, InsertOneResult):
            self.log.info('Failed inserting data')
            raise pymongo.errors.OperationFailure('Failed inserting data')

        self.log.info('Successfully inserted data')
        return True

    def query_block(self, query=None):
        if not isinstance(query, dict):
            raise ValueError('Query must be a dictionary')
        yield db[self.DB_NAME].find(query)

    def get_last_block(self):
        return db[self.DB_NAME].find()

    def get_first_block(self):
        return db[self.DB_NAME].find().sort('timestamp', -1)[0]

    def _get_last_hash(self):
        last_node = db[self.DB_NAME].find().sort('timestamp', -1)[0]
        return last_node['blockhash'], last_node['index']

    def validate(self):
        self.log.info('Validating Blockchain...')
        prev_hash = '0'
        for i, data in enumerate(db[self.DB_NAME].find()):
            if i == 0 or i == 1:
                continue
            self.log.info(data.keys())
            blockhash = data['blockhash']
            del data['blockhash']
            del data["_id"]
            encoded_block = json.dumps(data, sort_keys=True).encode()
            hashed = hashlib.sha256(encoded_block).hexdigest()
            if hashed != blockhash:
                self.log.critical('Blockchain interrupted, this blockchain is no longer valid')
                return False

        self.log.info('Blockchain is safe')
        return True

class DemoBlockChainManager(BlockChainManager):
    DB_NAME = 'demo'

    def __init__(self):
        super().__init__()

class TransactionBlockChainManager(BlockChainManager):
    DB_NAME = 'transactions'

    def __init__(self):
        super().__init__()

def main():
    mng = DemoBlockChainManager()
    blockchain_first_block = {
        'data': 'Hello, this is the first block in the blockchain',
    }
    mng.validate()

if __name__ == '__main__':
    main()
