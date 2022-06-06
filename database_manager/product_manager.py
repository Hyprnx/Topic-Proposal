from base import BaseClass
from common.mongo_db_connect import connect_to_database
import datetime
db = connect_to_database()

class ProductDatabaseManager(BaseClass):
    def __init__(self):
        super().__init__()
        self.DB_NAME = 'products'

    def get_product_info(self, product_id):
        try:
            respond = db[self.DB_NAME].find_one({'product_id': int(product_id)})
            self.log.info(respond)
            del respond['no']
            del respond['_id']
            return respond
        except BaseException as e:
            self.log.info(f'No product found for product_id: {product_id}, error:{e}')
            return False

    def add_product(self):
        pass