import logging

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from data_structure.schema.schemas import *

from base import BaseClass

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.ERROR)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Validator(BaseClass):
    SCHEMA = None

    def __init__(self):
        super().__init__()

    def validate(self, entry):
        try:
            self.log.info('Validating %s' %entry)
            validate(instance=entry, schema=self.SCHEMA)
            self.log.info('Entry validated: passed')
            return True, "OK"
        except ValidationError as e:
            return False, e.message


class ValidateImportGoods(Validator):
    SCHEMA = SCHEMA_GOODS_IMPORT

    def __init__(self):
        super().__init__()


class ValidateSellingGoods(Validator):
    SCHEMA = SCHEMA_GOODS_SELL

    def __init__(self):
        super().__init__()


def main():
    from datetime import datetime

    today = datetime.now()

    seller_address = {
        "country_name": 'Vietnam',
        "district": 'Hai Ba Trung'
    }
    seller = {
        'id': '123456',
        'name': 'To Duc Anh',
        'phone_number': '0123456789',
        'address': seller_address
    }

    customer_address = {
        "country_name": 'Vietnam',
        "district": 'Hai Ba Trung'
    }

    customer = {
        'id': '456789',
        'name': 'Nam',
        'phone_number': '0332460789',
        'address': customer_address
    }

    selling_info = {
        "name": "toyota vios 1 5g 2010",
        "brand": 'toyota',
        "price": 1100000000,
        "quantity": 2,
        "who_sell": seller,
        "who_buy": customer,
        # "time": today
    }

    validator = ValidateSellingGoods()
    print('Validate used car result:', validator.validate(selling_info))


if __name__ == '__main__':
    main()
