from base import BaseClass
from common.mongo_db_connect import connect_to_database
import datetime
db = connect_to_database()

class CustomerDatabaseManager(BaseClass):
    def __init__(self):
        super().__init__()
        self.DB_NAME = 'customer'

    def query(self, query):
        try:
            return db[self.DB_NAME].find(query)
        except BaseException as e:
            self.log.error(e)
            return False

    def check_customer_exist(self, phone):
        res = db[self.DB_NAME].find_one({'Phone number': str(phone)})
        if res:
            return True
        return False

    def get_customer_info(self, phone):
        try:
            respond = db[self.DB_NAME].find_one({'Phone number': str(phone)})
            self.log.info("Customer info:", respond)
            del respond['signed_date']
            del respond['_id']
            return respond
        except BaseException as e:
            self.log.info(f'No customer found for phone: {phone}, error: {e}')
            return False

    def register_customers(self, name, phone, address):
        if self.check_customer_exist(phone):
            return 'Customer existed'
        try:
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