from base import BaseClass
import hashlib
from common.mongo_db_connect import connect_to_database

db = connect_to_database()

class EmployeeDatabaseManager(BaseClass):
    def __init__(self):
        super().__init__()
        self.DB_NAME = 'employee'

    def check_employee_exist(self, email, password):
        respond = db[self.DB_NAME].find_one({'email': email})
        hashed_password = hashlib.sha256(str(password).encode('utf-8')).hexdigest()
        try:
            if respond['password'] == hashed_password:
                return respond
        except BaseException as e:
            self.log.info(e)
            return None

    def get_employee_info(self, phone):
        try:
            respond = db[self.DB_NAME].find_one({'phone_number': str(phone)})
            del respond['_id']
            del respond['started_working']
            del respond['password']
            del respond['Address']
            return respond

        except BaseException as e:
            self.log.info(f'No employee found for phone: {phone}, error: {e}')
            return False


