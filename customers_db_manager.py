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

    def check_customer_exist(self, phone):
        res = db[self.DB_NAME].find_one({'Phone number': phone})
        if res:
            return True
        return False

    def register_customers(self, name, phone, address):
        if self.check_customer_exist(phone):
            return 'Customer existed'
        try:
            # hashed_password = hashlib.sha256(str(password).encode('utf-8')).hexdigest()
            customer_info = {
                'Name': name,
                'Phone number': phone,
                'Address': address,
                'signed_date': str(datetime.datetime.now()),
            }
            self.log.info(f'Inserting customer: {customer_info} to database...')
            db[self.DB_NAME].insert_one(customer_info)
            self.log.info(f'Successfully inserting customer to database')
            return True
        except BaseException as e:
            raise e