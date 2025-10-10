"""
Contract Validator
Validates API responses against contracts
"""

import logging
import requests
from jsonschema import validate, ValidationError as SchemaValidationError

logger = logging.getLogger(__name__)


class ContractValidator:
    """
    Validates API responses against contracts
    """
    
    def __init__(self):
        self.validation_results = []
        logger.info("Contract Validator initialized")
    
    def validate_contract(self, contract, base_url):
        """
        Validate API against contract
        
        Args:
            contract: APIContract instance
            base_url: Base URL of API
            
        Returns:
            Validation result
        """
        result = {
            'contract': contract.name,
            'method': contract.method,
            'path': contract.path,
            'passed': True,
            'errors': []
        }
        
        try:
            # Build URL
            url = f"{base_url}{contract.path}"
            
            # Make request
            if contract.method == 'GET':
                response = requests.get(url)
            elif contract.method == 'POST':
                # Use sample data if request schema exists
                sample_data = self._generate_sample_data(contract.request_schema)
                response = requests.post(url, json=sample_data)
            else:
                response = requests.request(contract.method, url)
            
            # Validate status code
            if response.status_code != contract.expected_status:
                result['passed'] = False
                result['errors'].append(
                    f"Status code mismatch: expected {contract.expected_status}, got {response.status_code}"
                )
            
            # Validate response schema
            if contract.response_schema and response.status_code < 400:
                try:
                    response_data = response.json()
                    validate(instance=response_data, schema=contract.response_schema)
                except SchemaValidationError as e:
                    result['passed'] = False
                    result['errors'].append(f"Response schema validation failed: {e.message}")
                except Exception as e:
                    result['passed'] = False
                    result['errors'].append(f"Response parsing failed: {str(e)}")
            
            # Validate headers
            for header, expected_value in contract.headers.items():
                if header not in response.headers:
                    result['passed'] = False
                    result['errors'].append(f"Missing header: {header}")
                elif response.headers[header] != expected_value:
                    result['passed'] = False
                    result['errors'].append(
                        f"Header mismatch: {header} expected {expected_value}, got {response.headers[header]}"
                    )
        
        except Exception as e:
            result['passed'] = False
            result['errors'].append(f"Request failed: {str(e)}")
        
        self.validation_results.append(result)
        
        if result['passed']:
            logger.info(f"Contract validation passed: {contract.name}")
        else:
            logger.error(f"Contract validation failed: {contract.name} - {result['errors']}")
        
        return result
    
    def validate_all_contracts(self, contracts, base_url):
        """
        Validate multiple contracts
        
        Args:
            contracts: List of APIContract instances
            base_url: Base URL of API
            
        Returns:
            Summary of validation results
        """
        results = []
        
        for contract in contracts:
            result = self.validate_contract(contract, base_url)
            results.append(result)
        
        passed = sum(1 for r in results if r['passed'])
        failed = len(results) - passed
        
        return {
            'total': len(results),
            'passed': passed,
            'failed': failed,
            'success_rate': f"{(passed / len(results) * 100) if results else 0:.2f}%",
            'results': results
        }
    
    def _generate_sample_data(self, schema):
        """
        Generate sample data from schema
        
        Args:
            schema: JSON schema
            
        Returns:
            Sample data matching schema
        """
        if not schema:
            return {}
        
        sample = {}
        
        if 'properties' in schema:
            for prop, prop_schema in schema['properties'].items():
                if prop_schema['type'] == 'string':
                    sample[prop] = 'test_value'
                elif prop_schema['type'] == 'integer':
                    sample[prop] = 1
                elif prop_schema['type'] == 'number':
                    sample[prop] = 1.0
                elif prop_schema['type'] == 'boolean':
                    sample[prop] = True
        
        return sample
    
    def get_validation_summary(self):
        """Get summary of all validations"""
        if not self.validation_results:
            return {'message': 'No validations performed'}
        
        passed = sum(1 for r in self.validation_results if r['passed'])
        failed = len(self.validation_results) - passed
        
        return {
            'total_validations': len(self.validation_results),
            'passed': passed,
            'failed': failed,
            'success_rate': f"{(passed / len(self.validation_results) * 100):.2f}%"
        }
