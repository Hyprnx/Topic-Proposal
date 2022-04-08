SCHEMA_TIME = {
  # "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "datetime": {
      "type": "string",
      "format": "date-time"
    }
  }
}

SCHEMA_ADDRESS = {
    "type": "object",
    "properties": {
        "country_name": {
            "type": "string"
        },
        "district": {
            "type": "string"
        },

    },
    "required": [
        "country_name"
    ],
    'additionalProperties': False
}

SCHEMA_EMPLOYEE = {
    "type": "object",
    "properties": {
        'id': {
            "type": "string"
        },
        'name': {
            "type": "string"
        },
        'phone_number': {
            'type': 'string',
            "pattern": "^[0-9]{10}$"
        },
        'address': SCHEMA_ADDRESS
    },
    "required": [
        "name",
        "phone_number"
    ],
    'additionalProperties': False
}


SCHEMA_CUSTOMER = {
    "type": "object",
    "properties": {
        'id': {
            "type": "string"
        },
        'name': {
            "type": "string"
        },
        'phone_number': {
            'type': 'string',
            "pattern": "[0-9]{10}$"
        },
        'address': SCHEMA_ADDRESS
    },
    "required": [
        "name",
        "phone_number",
        'id',
    ],
    'additionalProperties': False
}

SCHEMA_GOODS_IMPORT = {
    "type": "object",
    "properties": {
        'name': {
            "type": "string"
        },
        'brand': {
            "type": "string"
        },
        'price': {
            "type": "number"
        },
        'quantity': {
            "type": "number"
        },
        'who_sell': SCHEMA_EMPLOYEE,
        "time": SCHEMA_TIME
    },
    "required": [
        "name",
        "brand",
        'price',
        'quantity',
        'who_sell',
        'time'
    ],
    'additionalProperties': False
}


SCHEMA_GOODS_SELL = {
    "type": "object",
    "properties": {
        'name': {
            "type": "string"
        },
        'brand': {
            "type": "string"
        },
        'price': {
            "type": "number"
        },
        'quantity': {
            "type": "number"
        },
        'who_sell': SCHEMA_EMPLOYEE,
        'who_buy': SCHEMA_CUSTOMER,
        "time": SCHEMA_TIME
    },
    "required": [
        "name",
        "brand",
        'price',
        'quantity',
        'who_sell',
        'who_buy',
        # 'time'
    ],
    'additionalProperties': False
}

