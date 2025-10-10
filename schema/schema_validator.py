"""
Schema Validator
Validates JSON data against schemas
"""

import logging
from jsonschema import validate, ValidationError, Draft7Validator

logger = logging.getLogger(__name__)


class SchemaValidator:
    """
    JSON Schema validator
    """
    
    def __init__(self):
        self.validation_errors = []
        logger.info("Schema Validator initialized")
    
    def validate(self, data, schema):
        """
        Validate data against schema
        
        Args:
            data: Data to validate
            schema: JSON schema
            
        Returns:
            Validation result
        """
        result = {
            'valid': True,
            'errors': []
        }
        
        try:
            validate(instance=data, schema=schema)
            logger.debug("Schema validation passed")
        except ValidationError as e:
            result['valid'] = False
            result['errors'].append({
                'message': e.message,
                'path': list(e.path),
                'schema_path': list(e.schema_path)
            })
            
            self.validation_errors.append(result)
            logger.warning(f"Schema validation failed: {e.message}")
        
        return result
    
    def validate_request(self, request_data, schema):
        """
        Validate request data
        
        Args:
            request_data: Request data
            schema: Request schema
            
        Returns:
            Validation result
        """
        return self.validate(request_data, schema)
    
    def validate_response(self, response_data, schema):
        """
        Validate response data
        
        Args:
            response_data: Response data
            schema: Response schema
            
        Returns:
            Validation result
        """
        return self.validate(response_data, schema)
    
    def get_validation_errors(self):
        """Get all validation errors"""
        return self.validation_errors
    
    def clear_errors(self):
        """Clear validation errors"""
        self.validation_errors.clear()


class SchemaRegistry:
    """
    Registry for storing schemas
    """
    
    def __init__(self):
        self.schemas = {}
        logger.info("Schema Registry initialized")
    
    def register(self, name, schema):
        """
        Register a schema
        
        Args:
            name: Schema name
            schema: JSON schema
        """
        self.schemas[name] = schema
        logger.info(f"Schema registered: {name}")
    
    def get_schema(self, name):
        """Get schema by name"""
        return self.schemas.get(name)
    
    def get_all_schemas(self):
        """Get all schemas"""
        return self.schemas
