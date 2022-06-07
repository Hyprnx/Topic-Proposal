from base import BaseClass
from common.mongo_db_connect import connect_to_database
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

    def sell_product(self, product_id, current_amount, amount_sell):
        try:
            new_amount = int(current_amount) - int(amount_sell)
            myquery = {"product_id": int(product_id)}
            newvalues = {"$set": {"stock": new_amount}}
            db[self.DB_NAME].update_one(myquery, newvalues)
            return True
        except BaseException as e:
            self.log.error(e)
            return False

    def import_product(self, new_product: bool, **product_data):
        if new_product:
            try:
                new_prod = {'product_id': int(product_data['product_id']),
                            'product_name': product_data['product_name'],
                            'price': float(product_data['price']),
                            'stock': int(product_data['new_stock'])}
                db[self.DB_NAME].insert_one(new_prod)
                return True
            except BaseException as e:
                self.log.error(e)
                return False
        else:
            try:
                new_amount = int(product_data['old_amount']) + int(product_data['new_amount'])
                myquery = {"product_id": int(product_data['product_id'])}
                newvalues = {"$set": {"stock": new_amount}}
                db[self.DB_NAME].update_one(myquery, newvalues)
                return True
            except BaseException as e:
                self.log.error(e)
                return False