"""
Test Helpers
Utility functions for contract testing
"""

import logging

logger = logging.getLogger(__name__)


def assert_status_code(response, expected_status):
    """
    Assert response status code
    
    Args:
        response: HTTP response
        expected_status: Expected status code
        
    Returns:
        True if matches, False otherwise
    """
    if response.status_code != expected_status:
        logger.error(f"Status code mismatch: expected {expected_status}, got {response.status_code}")
        return False
    return True


def assert_response_schema(response_data, schema, validator):
    """
    Assert response matches schema
    
    Args:
        response_data: Response data
        schema: JSON schema
        validator: SchemaValidator instance
        
    Returns:
        True if valid, False otherwise
    """
    result = validator.validate(response_data, schema)
    return result['valid']


def assert_header_present(response, header_name):
    """
    Assert header is present in response
    
    Args:
        response: HTTP response
        header_name: Header name
        
    Returns:
        True if present, False otherwise
    """
    if header_name not in response.headers:
        logger.error(f"Header missing: {header_name}")
        return False
    return True


def assert_response_time(response_time, max_time):
    """
    Assert response time is within limit
    
    Args:
        response_time: Actual response time
        max_time: Maximum allowed time
        
    Returns:
        True if within limit, False otherwise
    """
    if response_time > max_time:
        logger.warning(f"Response time exceeded: {response_time}s > {max_time}s")
        return False
    return True


def compare_contracts(contract1, contract2):
    """
    Compare two contracts for compatibility
    
    Args:
        contract1: First contract
        contract2: Second contract
        
    Returns:
        Comparison result
    """
    differences = []
    
    # Compare methods
    if contract1.method != contract2.method:
        differences.append(f"Method mismatch: {contract1.method} vs {contract2.method}")
    
    # Compare paths
    if contract1.path != contract2.path:
        differences.append(f"Path mismatch: {contract1.path} vs {contract2.path}")
    
    # Compare status codes
    if contract1.expected_status != contract2.expected_status:
        differences.append(f"Status mismatch: {contract1.expected_status} vs {contract2.expected_status}")
    
    return {
        'compatible': len(differences) == 0,
        'differences': differences
    }


def generate_test_data(schema):
    """
    Generate test data from schema
    
    Args:
        schema: JSON schema
        
    Returns:
        Test data
    """
    if not schema or 'properties' not in schema:
        return {}
    
    data = {}
    
    for prop, prop_schema in schema['properties'].items():
        prop_type = prop_schema.get('type')
        
        if prop_type == 'string':
            if prop_schema.get('format') == 'email':
                data[prop] = 'test@example.com'
            else:
                data[prop] = 'test_string'
        elif prop_type == 'integer':
            data[prop] = prop_schema.get('minimum', 1)
        elif prop_type == 'number':
            data[prop] = prop_schema.get('minimum', 1.0)
        elif prop_type == 'boolean':
            data[prop] = True
        elif prop_type == 'array':
            data[prop] = []
        elif prop_type == 'object':
            data[prop] = {}
    
    return data
