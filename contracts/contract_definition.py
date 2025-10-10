"""
Contract Definition
Defines API contracts for testing
"""

import logging

logger = logging.getLogger(__name__)


class APIContract:
    """
    API contract definition
    Defines expected behavior of an API endpoint
    """
    
    def __init__(self, name, method, path, description=""):
        """
        Initialize API contract
        
        Args:
            name: Contract name
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            description: Contract description
        """
        self.name = name
        self.method = method
        self.path = path
        self.description = description
        
        self.request_schema = None
        self.response_schema = None
        self.expected_status = 200
        self.headers = {}
        
        logger.info(f"Contract created: {name} ({method} {path})")
    
    def with_request_schema(self, schema):
        """
        Set request schema
        
        Args:
            schema: JSON schema for request
        """
        self.request_schema = schema
        return self
    
    def with_response_schema(self, schema):
        """
        Set response schema
        
        Args:
            schema: JSON schema for response
        """
        self.response_schema = schema
        return self
    
    def with_status(self, status_code):
        """
        Set expected status code
        
        Args:
            status_code: Expected HTTP status code
        """
        self.expected_status = status_code
        return self
    
    def with_headers(self, headers):
        """
        Set expected headers
        
        Args:
            headers: Dictionary of expected headers
        """
        self.headers = headers
        return self
    
    def to_dict(self):
        """Convert contract to dictionary"""
        return {
            'name': self.name,
            'method': self.method,
            'path': self.path,
            'description': self.description,
            'request_schema': self.request_schema,
            'response_schema': self.response_schema,
            'expected_status': self.expected_status,
            'headers': self.headers
        }


class ContractRegistry:
    """
    Registry for storing and managing contracts
    """
    
    def __init__(self):
        self.contracts = {}
        logger.info("Contract Registry initialized")
    
    def register(self, contract):
        """
        Register a contract
        
        Args:
            contract: APIContract instance
        """
        key = f"{contract.method}:{contract.path}"
        self.contracts[key] = contract
        logger.info(f"Contract registered: {key}")
    
    def get_contract(self, method, path):
        """
        Get contract by method and path
        
        Args:
            method: HTTP method
            path: Endpoint path
            
        Returns:
            APIContract or None
        """
        key = f"{method}:{path}"
        return self.contracts.get(key)
    
    def get_all_contracts(self):
        """Get all registered contracts"""
        return list(self.contracts.values())
    
    def get_contracts_by_path(self, path):
        """Get all contracts for a path"""
        return [c for c in self.contracts.values() if c.path == path]


# Predefined contracts for common endpoints
def get_user_contract():
    """Contract for GET /api/users/{id}"""
    return APIContract(
        name="GetUser",
        method="GET",
        path="/api/users/{id}",
        description="Get user by ID"
    ).with_response_schema({
        'type': 'object',
        'required': ['id', 'username', 'email'],
        'properties': {
            'id': {'type': 'integer'},
            'username': {'type': 'string'},
            'email': {'type': 'string', 'format': 'email'}
        }
    }).with_status(200)


def create_user_contract():
    """Contract for POST /api/users"""
    return APIContract(
        name="CreateUser",
        method="POST",
        path="/api/users",
        description="Create a new user"
    ).with_request_schema({
        'type': 'object',
        'required': ['username', 'email'],
        'properties': {
            'username': {'type': 'string', 'minLength': 3},
            'email': {'type': 'string', 'format': 'email'},
            'age': {'type': 'integer', 'minimum': 0}
        }
    }).with_response_schema({
        'type': 'object',
        'required': ['id', 'username', 'email'],
        'properties': {
            'id': {'type': 'integer'},
            'username': {'type': 'string'},
            'email': {'type': 'string'}
        }
    }).with_status(201)


def list_users_contract():
    """Contract for GET /api/users"""
    return APIContract(
        name="ListUsers",
        method="GET",
        path="/api/users",
        description="List all users"
    ).with_response_schema({
        'type': 'object',
        'required': ['users', 'count'],
        'properties': {
            'users': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'username': {'type': 'string'},
                        'email': {'type': 'string'}
                    }
                }
            },
            'count': {'type': 'integer'}
        }
    }).with_status(200)
