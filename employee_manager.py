from base import BaseClass
import json
import hashlib
from mongo_db_connect import connect_to_database
import datetime
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

