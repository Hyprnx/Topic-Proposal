from pymongo import MongoClient
import datetime

host = 'localhost'
port = 27017

client = MongoClient(host, port)

blockchain_first_block = {
            'index': 0,
            'signer': 'To Duc Anh',
            'timestamp': str(datetime.datetime.now()),
            'data': 'Hello, this is the first block in the blockchain',
            'previous_hash': '0'}

