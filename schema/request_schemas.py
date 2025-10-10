"""
Request Schemas
JSON schemas for API requests
"""


# User request schemas
CREATE_USER_REQUEST_SCHEMA = {
    'type': 'object',
    'required': ['username', 'email'],
    'properties': {
        'username': {
            'type': 'string',
            'minLength': 3,
            'maxLength': 50
        },
        'email': {
            'type': 'string',
            'format': 'email'
        },
        'age': {
            'type': 'integer',
            'minimum': 0,
            'maximum': 150
        },
        'city': {
            'type': 'string'
        }
    },
    'additionalProperties': False
}


UPDATE_USER_REQUEST_SCHEMA = {
    'type': 'object',
    'properties': {
        'username': {
            'type': 'string',
            'minLength': 3,
            'maxLength': 50
        },
        'email': {
            'type': 'string',
            'format': 'email'
        },
        'age': {
            'type': 'integer',
            'minimum': 0,
            'maximum': 150
        },
        'city': {
            'type': 'string'
        }
    },
    'additionalProperties': False
}


# Order request schemas
CREATE_ORDER_REQUEST_SCHEMA = {
    'type': 'object',
    'required': ['user_id', 'product', 'quantity'],
    'properties': {
        'user_id': {
            'type': 'integer',
            'minimum': 1
        },
        'product': {
            'type': 'string',
            'minLength': 1
        },
        'quantity': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 100
        },
        'price': {
            'type': 'number',
            'minimum': 0
        }
    },
    'additionalProperties': False
}


# Login request schema
LOGIN_REQUEST_SCHEMA = {
    'type': 'object',
    'required': ['username', 'password'],
    'properties': {
        'username': {
            'type': 'string',
            'minLength': 3
        },
        'password': {
            'type': 'string',
            'minLength': 8
        }
    },
    'additionalProperties': False
}


def get_request_schema(schema_name):
    """
    Get request schema by name
    
    Args:
        schema_name: Name of schema
        
    Returns:
        JSON schema or None
    """
    schemas = {
        'create_user': CREATE_USER_REQUEST_SCHEMA,
        'update_user': UPDATE_USER_REQUEST_SCHEMA,
        'create_order': CREATE_ORDER_REQUEST_SCHEMA,
        'login': LOGIN_REQUEST_SCHEMA
    }
    
    return schemas.get(schema_name)
