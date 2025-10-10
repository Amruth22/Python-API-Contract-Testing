"""
Response Schemas
JSON schemas for API responses
"""


# User response schemas
USER_RESPONSE_SCHEMA = {
    'type': 'object',
    'required': ['id', 'username', 'email'],
    'properties': {
        'id': {'type': 'integer'},
        'username': {'type': 'string'},
        'email': {'type': 'string'},
        'age': {'type': 'integer'},
        'city': {'type': 'string'}
    }
}


USER_LIST_RESPONSE_SCHEMA = {
    'type': 'object',
    'required': ['users', 'count'],
    'properties': {
        'users': {
            'type': 'array',
            'items': USER_RESPONSE_SCHEMA
        },
        'count': {'type': 'integer'}
    }
}


CREATE_USER_RESPONSE_SCHEMA = {
    'type': 'object',
    'required': ['id', 'username', 'email'],
    'properties': {
        'id': {'type': 'integer'},
        'username': {'type': 'string'},
        'email': {'type': 'string'},
        'message': {'type': 'string'}
    }
}


# Order response schemas
ORDER_RESPONSE_SCHEMA = {
    'type': 'object',
    'required': ['id', 'user_id', 'product', 'quantity', 'price', 'status'],
    'properties': {
        'id': {'type': 'integer'},
        'user_id': {'type': 'integer'},
        'product': {'type': 'string'},
        'quantity': {'type': 'integer'},
        'price': {'type': 'number'},
        'status': {'type': 'string'}
    }
}


ORDER_LIST_RESPONSE_SCHEMA = {
    'type': 'object',
    'required': ['orders', 'count'],
    'properties': {
        'orders': {
            'type': 'array',
            'items': ORDER_RESPONSE_SCHEMA
        },
        'count': {'type': 'integer'}
    }
}


# Error response schema
ERROR_RESPONSE_SCHEMA = {
    'type': 'object',
    'required': ['error', 'message'],
    'properties': {
        'error': {'type': 'string'},
        'message': {'type': 'string'},
        'details': {'type': 'object'}
    }
}


# Success response schema
SUCCESS_RESPONSE_SCHEMA = {
    'type': 'object',
    'required': ['status', 'message'],
    'properties': {
        'status': {'type': 'string'},
        'message': {'type': 'string'},
        'data': {'type': 'object'}
    }
}


def get_response_schema(schema_name):
    """
    Get response schema by name
    
    Args:
        schema_name: Name of schema
        
    Returns:
        JSON schema or None
    """
    schemas = {
        'user': USER_RESPONSE_SCHEMA,
        'user_list': USER_LIST_RESPONSE_SCHEMA,
        'create_user': CREATE_USER_RESPONSE_SCHEMA,
        'order': ORDER_RESPONSE_SCHEMA,
        'order_list': ORDER_LIST_RESPONSE_SCHEMA,
        'error': ERROR_RESPONSE_SCHEMA,
        'success': SUCCESS_RESPONSE_SCHEMA
    }
    
    return schemas.get(schema_name)
