"""
Mock Responses
Predefined mock response data
"""


# User mock responses
USER_MOCK_RESPONSES = {
    'get_user': {
        'id': 1,
        'username': 'john_doe',
        'email': 'john@example.com',
        'age': 30,
        'city': 'New York'
    },
    'list_users': {
        'users': [
            {'id': 1, 'username': 'john_doe', 'email': 'john@example.com'},
            {'id': 2, 'username': 'jane_doe', 'email': 'jane@example.com'},
            {'id': 3, 'username': 'bob_smith', 'email': 'bob@example.com'}
        ],
        'count': 3
    },
    'create_user': {
        'id': 4,
        'username': 'new_user',
        'email': 'new@example.com',
        'message': 'User created successfully'
    },
    'user_not_found': {
        'error': 'Not Found',
        'message': 'User not found'
    }
}


# Order mock responses
ORDER_MOCK_RESPONSES = {
    'get_order': {
        'id': 1,
        'user_id': 1,
        'product': 'Laptop',
        'quantity': 1,
        'price': 999.99,
        'status': 'confirmed'
    },
    'list_orders': {
        'orders': [
            {'id': 1, 'user_id': 1, 'product': 'Laptop', 'price': 999.99},
            {'id': 2, 'user_id': 1, 'product': 'Mouse', 'price': 29.99}
        ],
        'count': 2
    },
    'create_order': {
        'id': 3,
        'user_id': 1,
        'product': 'Keyboard',
        'quantity': 1,
        'price': 79.99,
        'status': 'pending',
        'message': 'Order created successfully'
    }
}


# Error mock responses
ERROR_MOCK_RESPONSES = {
    'bad_request': {
        'error': 'Bad Request',
        'message': 'Invalid request data'
    },
    'unauthorized': {
        'error': 'Unauthorized',
        'message': 'Authentication required'
    },
    'forbidden': {
        'error': 'Forbidden',
        'message': 'Access denied'
    },
    'not_found': {
        'error': 'Not Found',
        'message': 'Resource not found'
    },
    'internal_error': {
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }
}


def get_mock_response(category, response_type):
    """
    Get a mock response
    
    Args:
        category: Response category (user, order, error)
        response_type: Specific response type
        
    Returns:
        Mock response data
    """
    responses = {
        'user': USER_MOCK_RESPONSES,
        'order': ORDER_MOCK_RESPONSES,
        'error': ERROR_MOCK_RESPONSES
    }
    
    return responses.get(category, {}).get(response_type, {})
