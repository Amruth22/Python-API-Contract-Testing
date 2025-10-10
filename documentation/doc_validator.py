"""
Documentation Validator
Validates that API matches its documentation
"""

import logging
import requests
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)


class DocumentationValidator:
    """
    Validates API implementation against documentation
    """
    
    def __init__(self):
        self.validation_results = []
        logger.info("Documentation Validator initialized")
    
    def validate_endpoint(self, spec, base_url, path, method):
        """
        Validate endpoint matches specification
        
        Args:
            spec: APISpecification instance
            base_url: Base URL of API
            path: Endpoint path
            method: HTTP method
            
        Returns:
            Validation result
        """
        endpoint_spec = spec.get_endpoint_spec(path, method)
        
        if not endpoint_spec:
            return {
                'passed': False,
                'error': f'No specification found for {method} {path}'
            }
        
        result = {
            'endpoint': f"{method} {path}",
            'passed': True,
            'errors': []
        }
        
        try:
            # Make request
            url = f"{base_url}{path}"
            
            if method == 'GET':
                response = requests.get(url)
            elif method == 'POST':
                # Generate sample data from request schema
                sample_data = self._generate_sample_from_schema(endpoint_spec.get('request_schema'))
                response = requests.post(url, json=sample_data)
            else:
                response = requests.request(method, url)
            
            # Validate status code
            expected_status = endpoint_spec.get('status_code', 200)
            if response.status_code != expected_status:
                result['passed'] = False
                result['errors'].append(
                    f"Status code mismatch: expected {expected_status}, got {response.status_code}"
                )
            
            # Validate response schema
            response_schema = endpoint_spec.get('response_schema')
            if response_schema and response.status_code < 400:
                try:
                    response_data = response.json()
                    validate(instance=response_data, schema=response_schema)
                except ValidationError as e:
                    result['passed'] = False
                    result['errors'].append(f"Response doesn't match schema: {e.message}")
                except Exception as e:
                    result['passed'] = False
                    result['errors'].append(f"Response validation error: {str(e)}")
        
        except Exception as e:
            result['passed'] = False
            result['errors'].append(f"Request failed: {str(e)}")
        
        self.validation_results.append(result)
        return result
    
    def validate_all_endpoints(self, spec, base_url):
        """
        Validate all endpoints in specification
        
        Args:
            spec: APISpecification instance
            base_url: Base URL of API
            
        Returns:
            Validation summary
        """
        results = []
        
        for path, methods in spec.get_all_endpoints().items():
            for method in methods.keys():
                result = self.validate_endpoint(spec, base_url, path, method)
                results.append(result)
        
        passed = sum(1 for r in results if r['passed'])
        failed = len(results) - passed
        
        return {
            'total_endpoints': len(results),
            'passed': passed,
            'failed': failed,
            'success_rate': f"{(passed / len(results) * 100) if results else 0:.2f}%",
            'results': results
        }
    
    def _generate_sample_from_schema(self, schema):
        """Generate sample data from schema"""
        if not schema or 'properties' not in schema:
            return {}
        
        sample = {}
        for prop, prop_schema in schema['properties'].items():
            if prop_schema['type'] == 'string':
                sample[prop] = 'test_value'
            elif prop_schema['type'] == 'integer':
                sample[prop] = 1
            elif prop_schema['type'] == 'number':
                sample[prop] = 1.0
        
        return sample
