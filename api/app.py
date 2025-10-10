"""
Flask API (Provider)
API that implements contracts
"""

from flask import Flask, request, jsonify
import logging
from schema.schema_validator import SchemaValidator
from schema.request_schemas import get_request_schema
from schema.response_schemas import get_response_schema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize validator
validator = SchemaValidator()

# In-memory storage
users_db = {}
orders_db = {}
user_counter = 1
order_counter = 1


@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'API Contract Testing - Provider API',
        'version': '1.0.0',
        'endpoints': {
            'users': '/api/users',
            'orders': '/api/orders',
            'contracts': '/api/contracts'
        }
    })


@app.route('/health')
def health():
    """Health check"""
    return jsonify({'status': 'healthy'})


@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    users_list = list(users_db.values())
    
    response_data = {
        'users': users_list,
        'count': len(users_list)
    }
    
    # Validate response
    schema = get_response_schema('user_list')
    if schema:
        validation = validator.validate_response(response_data, schema)
        if not validation['valid']:
            logger.error(f"Response validation failed: {validation['errors']}")
    
    return jsonify(response_data)


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    if user_id not in users_db:
        return jsonify({
            'error': 'Not Found',
            'message': f'User {user_id} not found'
        }), 404
    
    user = users_db[user_id]
    
    # Validate response
    schema = get_response_schema('user')
    if schema:
        validation = validator.validate_response(user, schema)
        if not validation['valid']:
            logger.error(f"Response validation failed: {validation['errors']}")
    
    return jsonify(user)


@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Request body required'
        }), 400
    
    # Validate request
    schema = get_request_schema('create_user')
    if schema:
        validation = validator.validate_request(data, schema)
        if not validation['valid']:
            return jsonify({
                'error': 'Validation Error',
                'message': 'Request validation failed',
                'errors': validation['errors']
            }), 400
    
    # Create user
    global user_counter
    user_id = user_counter
    user = {
        'id': user_id,
        'username': data['username'],
        'email': data['email'],
        'age': data.get('age'),
        'city': data.get('city')
    }
    users_db[user_id] = user
    user_counter += 1
    
    # Validate response
    response_schema = get_response_schema('create_user')
    if response_schema:
        validation = validator.validate_response(user, response_schema)
        if not validation['valid']:
            logger.error(f"Response validation failed: {validation['errors']}")
    
    return jsonify(user), 201


@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    user_id = request.args.get('user_id', type=int)
    
    if user_id:
        orders_list = [o for o in orders_db.values() if o['user_id'] == user_id]
    else:
        orders_list = list(orders_db.values())
    
    return jsonify({
        'orders': orders_list,
        'count': len(orders_list)
    })


@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Request body required'
        }), 400
    
    # Validate request
    schema = get_request_schema('create_order')
    if schema:
        validation = validator.validate_request(data, schema)
        if not validation['valid']:
            return jsonify({
                'error': 'Validation Error',
                'errors': validation['errors']
            }), 400
    
    # Create order
    global order_counter
    order_id = order_counter
    order = {
        'id': order_id,
        'user_id': data['user_id'],
        'product': data['product'],
        'quantity': data['quantity'],
        'price': data.get('price', 0.0),
        'status': 'pending'
    }
    orders_db[order_id] = order
    order_counter += 1
    
    return jsonify(order), 201


@app.route('/api/contracts', methods=['GET'])
def get_contracts():
    """Get available contracts"""
    from contracts.contract_definition import get_user_contract, create_user_contract, list_users_contract
    
    contracts = [
        get_user_contract().to_dict(),
        create_user_contract().to_dict(),
        list_users_contract().to_dict()
    ]
    
    return jsonify({
        'contracts': contracts,
        'count': len(contracts)
    })


if __name__ == '__main__':
    import os
    
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print("=" * 60)
    print("API Contract Testing - Provider API")
    print("=" * 60)
    print(f"Starting on port {port}")
    print("Features:")
    print("  - Contract validation")
    print("  - Schema validation")
    print("  - Request/Response validation")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
