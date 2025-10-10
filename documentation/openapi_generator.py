"""
OpenAPI Generator
Generates OpenAPI specification from API
"""

import logging
import json

logger = logging.getLogger(__name__)


class OpenAPIGenerator:
    """
    Generates OpenAPI 3.0 specification
    """
    
    def __init__(self, title, version, description=""):
        """
        Initialize OpenAPI generator
        
        Args:
            title: API title
            version: API version
            description: API description
        """
        self.spec = {
            'openapi': '3.0.0',
            'info': {
                'title': title,
                'version': version,
                'description': description
            },
            'paths': {}
        }
        
        logger.info(f"OpenAPI Generator initialized: {title} v{version}")
    
    def add_path(self, path, method, summary, request_schema=None, response_schema=None, status_code=200):
        """
        Add path to OpenAPI spec
        
        Args:
            path: Endpoint path
            method: HTTP method
            summary: Endpoint summary
            request_schema: Request schema
            response_schema: Response schema
            status_code: Response status code
        """
        if path not in self.spec['paths']:
            self.spec['paths'][path] = {}
        
        operation = {
            'summary': summary,
            'responses': {
                str(status_code): {
                    'description': 'Successful response'
                }
            }
        }
        
        # Add request body if schema provided
        if request_schema:
            operation['requestBody'] = {
                'required': True,
                'content': {
                    'application/json': {
                        'schema': request_schema
                    }
                }
            }
        
        # Add response schema if provided
        if response_schema:
            operation['responses'][str(status_code)]['content'] = {
                'application/json': {
                    'schema': response_schema
                }
            }
        
        self.spec['paths'][path][method.lower()] = operation
        logger.info(f"Path added to OpenAPI: {method} {path}")
    
    def generate(self):
        """
        Generate OpenAPI specification
        
        Returns:
            OpenAPI spec dictionary
        """
        return self.spec
    
    def to_json(self, indent=2):
        """
        Convert specification to JSON string
        
        Args:
            indent: JSON indentation
            
        Returns:
            JSON string
        """
        return json.dumps(self.spec, indent=indent)
    
    def save_to_file(self, filename='openapi.json'):
        """
        Save specification to file
        
        Args:
            filename: Output filename
        """
        with open(filename, 'w') as f:
            f.write(self.to_json())
        
        logger.info(f"OpenAPI spec saved to {filename}")
