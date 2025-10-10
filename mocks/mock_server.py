"""
Mock Server
Simulates API responses for testing
"""

from flask import Flask, jsonify, request
import logging

logger = logging.getLogger(__name__)


class MockServer:
    """
    Mock API server for testing
    """
    
    def __init__(self, name="MockServer"):
        """
        Initialize mock server
        
        Args:
            name: Server name
        """
        self.app = Flask(name)
        self.mocks = {}
        self.request_history = []
        
        self._setup_routes()
        
        logger.info(f"Mock Server initialized: {name}")
    
    def add_mock(self, method, path, response_data, status_code=200, headers=None):
        """
        Add a mock response
        
        Args:
            method: HTTP method
            path: Endpoint path
            response_data: Response data to return
            status_code: HTTP status code
            headers: Response headers
        """
        key = f"{method}:{path}"
        self.mocks[key] = {
            'response_data': response_data,
            'status_code': status_code,
            'headers': headers or {}
        }
        
        logger.info(f"Mock added: {key}")
    
    def _setup_routes(self):
        """Setup catch-all route"""
        
        @self.app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
        def catch_all(path):
            """Catch-all route for mock responses"""
            # Record request
            self.request_history.append({
                'method': request.method,
                'path': f"/{path}",
                'data': request.get_json() if request.is_json else None
            })
            
            # Find mock
            key = f"{request.method}:/{path}"
            
            if key in self.mocks:
                mock = self.mocks[key]
                response = jsonify(mock['response_data'])
                response.status_code = mock['status_code']
                
                for header, value in mock['headers'].items():
                    response.headers[header] = value
                
                return response
            else:
                return jsonify({
                    'error': 'Mock not found',
                    'message': f'No mock defined for {request.method} /{path}'
                }), 404
    
    def get_request_history(self):
        """Get history of requests made to mock server"""
        return self.request_history
    
    def clear_history(self):
        """Clear request history"""
        self.request_history.clear()
    
    def run(self, host='127.0.0.1', port=5001, debug=False):
        """Run mock server"""
        logger.info(f"Starting mock server on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug, use_reloader=False)


def create_user_mock_server():
    """Create mock server for user API"""
    mock = MockServer("UserMockServer")
    
    # Mock GET /api/users
    mock.add_mock(
        method='GET',
        path='api/users',
        response_data={
            'users': [
                {'id': 1, 'username': 'john_doe', 'email': 'john@example.com'},
                {'id': 2, 'username': 'jane_doe', 'email': 'jane@example.com'}
            ],
            'count': 2
        },
        status_code=200
    )
    
    # Mock GET /api/users/1
    mock.add_mock(
        method='GET',
        path='api/users/1',
        response_data={
            'id': 1,
            'username': 'john_doe',
            'email': 'john@example.com'
        },
        status_code=200
    )
    
    # Mock POST /api/users
    mock.add_mock(
        method='POST',
        path='api/users',
        response_data={
            'id': 3,
            'username': 'new_user',
            'email': 'new@example.com'
        },
        status_code=201
    )
    
    return mock
