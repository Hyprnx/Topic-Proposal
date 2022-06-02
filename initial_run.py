from pymongo import MongoClient
import datetime
import json
from pprint import pprint
from datetime import datetime
import random
import time
import unicodedata

from mongo_db_connect import connect_to_database
db = connect_to_database()

employee = db.employee
customer = db.customer

# from unicode import unicode

def random_date():
    # random.seed(seed)
    d = random.randint(1577811600, int(time.time()))
    return datetime.fromtimestamp(d).strftime('%Y-%m-%d %H:%M:%S')


def normalize_name(name):
    text = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8")
    return str(text)

def random_email(name):
    return '_'.join(i for i in normalize_name(name).lower().split()) + '@bc.com'


def get_employee(name):
    respond = employee.find_one({'Name': name})
    return respond['email'], respond['phone_number']

def get_customer(name):
    respond = customer.find_one({'Name': name})
    return respond['Phone number']

path = 'C:\git\Topic-Proposal\sample_data\Transactions.json'

with open(path, 'r', encoding='utf8') as f:
    data = json.loads(f.read())

for i in data:
    i['employee_email'], i['employee_phone'] = get_employee(i['employee_name'])
    i['customer_phone'] = get_customer(i['customer_name'])



write_path = 'C:\git\Topic-Proposal\sample_data\Transactions2.json'

with open(write_path, 'w', encoding='utf8') as f_out:
    f_out.write(json.dumps(data, ensure_ascii=False, indent=4))

# pprint(data[0][''])

