from base import BaseClass
import json
import hashlib
from mongo_db_connect import connect_to_database
import datetime
db = connect_to_database()

class CustomerDatabaseManager(BaseClass):
    def __init__(self):
        super().__init__()
        self.DB_NAME = 'customer'

    def check_customer_exist(self, email):
        res = db[self.DB_NAME].find_one({'email': email})
        if res:
            return True
        return False

    def register_customers(self, name, email, password):
        if self.check_customer_exist(email):
            return 'Customer existed'
        try:
            hashed_password = hashlib.sha256(str(password).encode('utf-8')).hexdigest()
            customer_info = {
                'username': name,
                'email': email,
                'password': hashed_password,
                'timestamp': str(datetime.datetime.now()),
            }
            self.log.info(f'Inserting customer: {customer_info} to database...')
            db[self.DB_NAME].insert_one(customer_info)
            self.log.info(f'Successfully inserting customer to database')
            return True
        except BaseException as e:
            raise e