"""
Contract Tests
Contract test runner and utilities
"""

import logging
import requests
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)


class ContractTestRunner:
    """
    Runs contract tests against API
    """
    
    def __init__(self):
        self.test_results = []
        logger.info("Contract Test Runner initialized")
    
    def test_contract(self, contract, base_url):
        """
        Test a single contract
        
        Args:
            contract: APIContract instance
            base_url: Base URL of API
            
        Returns:
            Test result
        """
        result = {
            'contract': contract.name,
            'passed': True,
            'checks': []
        }
        
        try:
            # Build URL
            url = f"{base_url}{contract.path}"
            
            # Make request
            if contract.method == 'GET':
                response = requests.get(url, timeout=5)
            elif contract.method == 'POST':
                sample_data = self._generate_sample_data(contract.request_schema)
                response = requests.post(url, json=sample_data, timeout=5)
            else:
                response = requests.request(contract.method, url, timeout=5)
            
            # Check 1: Status code
            status_check = {
                'check': 'status_code',
                'passed': response.status_code == contract.expected_status,
                'expected': contract.expected_status,
                'actual': response.status_code
            }
            result['checks'].append(status_check)
            
            if not status_check['passed']:
                result['passed'] = False
            
            # Check 2: Response schema
            if contract.response_schema and response.status_code < 400:
                try:
                    response_data = response.json()
                    validate(instance=response_data, schema=contract.response_schema)
                    
                    schema_check = {
                        'check': 'response_schema',
                        'passed': True
                    }
                except ValidationError as e:
                    schema_check = {
                        'check': 'response_schema',
                        'passed': False,
                        'error': e.message
                    }
                    result['passed'] = False
                
                result['checks'].append(schema_check)
        
        except Exception as e:
            result['passed'] = False
            result['checks'].append({
                'check': 'request',
                'passed': False,
                'error': str(e)
            })
        
        self.test_results.append(result)
        return result
    
    def test_all_contracts(self, contracts, base_url):
        """
        Test all contracts
        
        Args:
            contracts: List of contracts
            base_url: Base URL
            
        Returns:
            Test summary
        """
        results = []
        
        for contract in contracts:
            result = self.test_contract(contract, base_url)
            results.append(result)
        
        passed = sum(1 for r in results if r['passed'])
        
        return {
            'total': len(results),
            'passed': passed,
            'failed': len(results) - passed,
            'results': results
        }
    
    def _generate_sample_data(self, schema):
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
