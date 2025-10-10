"""
API Specification
Defines API documentation
"""

import logging

logger = logging.getLogger(__name__)


class APISpecification:
    """
    API specification/documentation
    """
    
    def __init__(self, title, version, base_url):
        """
        Initialize API specification
        
        Args:
            title: API title
            version: API version
            base_url: Base URL
        """
        self.title = title
        self.version = version
        self.base_url = base_url
        self.endpoints = {}
        
        logger.info(f"API Specification created: {title} v{version}")
    
    def add_endpoint(self, path, method, description, request_schema=None, response_schema=None, status_code=200):
        """
        Add endpoint to specification
        
        Args:
            path: Endpoint path
            method: HTTP method
            description: Endpoint description
            request_schema: Request schema
            response_schema: Response schema
            status_code: Expected status code
        """
        if path not in self.endpoints:
            self.endpoints[path] = {}
        
        self.endpoints[path][method] = {
            'description': description,
            'request_schema': request_schema,
            'response_schema': response_schema,
            'status_code': status_code
        }
        
        logger.info(f"Endpoint added to spec: {method} {path}")
    
    def get_endpoint_spec(self, path, method):
        """Get specification for an endpoint"""
        return self.endpoints.get(path, {}).get(method)
    
    def get_all_endpoints(self):
        """Get all endpoints"""
        return self.endpoints
    
    def to_dict(self):
        """Convert specification to dictionary"""
        return {
            'title': self.title,
            'version': self.version,
            'base_url': self.base_url,
            'endpoints': self.endpoints
        }


# Sample API specification
def create_sample_api_spec():
    """Create sample API specification"""
    spec = APISpecification(
        title="User Management API",
        version="1.0.0",
        base_url="http://localhost:5000"
    )
    
    # GET /api/users
    spec.add_endpoint(
        path='/api/users',
        method='GET',
        description='Get list of all users',
        response_schema={
            'type': 'object',
            'required': ['users', 'count'],
            'properties': {
                'users': {'type': 'array'},
                'count': {'type': 'integer'}
            }
        },
        status_code=200
    )
    
    # GET /api/users/{id}
    spec.add_endpoint(
        path='/api/users/{id}',
        method='GET',
        description='Get user by ID',
        response_schema={
            'type': 'object',
            'required': ['id', 'username', 'email'],
            'properties': {
                'id': {'type': 'integer'},
                'username': {'type': 'string'},
                'email': {'type': 'string'}
            }
        },
        status_code=200
    )
    
    # POST /api/users
    spec.add_endpoint(
        path='/api/users',
        method='POST',
        description='Create a new user',
        request_schema={
            'type': 'object',
            'required': ['username', 'email'],
            'properties': {
                'username': {'type': 'string'},
                'email': {'type': 'string'}
            }
        },
        response_schema={
            'type': 'object',
            'required': ['id', 'username', 'email'],
            'properties': {
                'id': {'type': 'integer'},
                'username': {'type': 'string'},
                'email': {'type': 'string'}
            }
        },
        status_code=201
    )
    
    return spec
