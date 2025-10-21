"""
Comprehensive Unit Tests for API Contract Testing
Tests contracts, mocks, schemas, and documentation validation
"""

import unittest
from contracts.contract_definition import APIContract, ContractRegistry
from contracts.contract_validator import ContractValidator
from contracts.consumer_contracts import ConsumerContract, mobile_app_user_contract
from mocks.mock_server import MockServer
from mocks.mock_responses import get_mock_response
from schema.schema_validator import SchemaValidator
from schema.request_schemas import CREATE_USER_REQUEST_SCHEMA
from schema.response_schemas import USER_RESPONSE_SCHEMA, USER_LIST_RESPONSE_SCHEMA
from documentation.api_spec import create_sample_api_spec
from documentation.openapi_generator import OpenAPIGenerator
from testing.test_helpers import generate_test_data


class APIContractTestingTestCase(unittest.TestCase):
    """Unit tests for API Contract Testing"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test configuration"""
        print("\n" + "=" * 60)
        print("API Contract Testing - Unit Test Suite")
        print("=" * 60)
        print("Testing: Contracts, Mocks, Schemas, Documentation")
        print("=" * 60 + "\n")
    
    # Test 1: Contract Definition
    def test_01_contract_definition(self):
        """Test creating and defining contracts"""
        print("\n1. Testing contract definition...")
        
        contract = APIContract(
            name="TestContract",
            method="GET",
            path="/api/test"
        ).with_status(200)
        
        self.assertEqual(contract.name, "TestContract")
        self.assertEqual(contract.method, "GET")
        self.assertEqual(contract.path, "/api/test")
        self.assertEqual(contract.expected_status, 200)
        
        print(f"   [EMOJI] Contract created: {contract.name}")
        print(f"   [EMOJI] Method: {contract.method}, Path: {contract.path}")
    
    # Test 2: Contract Registry
    def test_02_contract_registry(self):
        """Test contract registry"""
        print("\n2. Testing contract registry...")
        
        registry = ContractRegistry()
        
        contract = APIContract("Test", "GET", "/api/test")
        registry.register(contract)
        
        retrieved = registry.get_contract("GET", "/api/test")
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Test")
        
        print(f"   [EMOJI] Contract registered and retrieved")
        
        all_contracts = registry.get_all_contracts()
        self.assertEqual(len(all_contracts), 1)
        print(f"   [EMOJI] Total contracts: {len(all_contracts)}")
    
    # Test 3: Schema Validation
    def test_03_schema_validation(self):
        """Test JSON schema validation"""
        print("\n3. Testing schema validation...")
        
        validator = SchemaValidator()
        
        # Valid data
        valid_data = {
            'username': 'john_doe',
            'email': 'john@example.com'
        }
        
        result = validator.validate(valid_data, CREATE_USER_REQUEST_SCHEMA)
        self.assertTrue(result['valid'])
        print("   [EMOJI] Valid data passed validation")
        
        # Invalid data
        invalid_data = {
            'username': 'ab',  # Too short
            'email': 'invalid'
        }
        
        result = validator.validate(invalid_data, CREATE_USER_REQUEST_SCHEMA)
        self.assertFalse(result['valid'])
        print("   [EMOJI] Invalid data rejected")
    
    # Test 4: Mock Server
    def test_04_mock_server(self):
        """Test mock server functionality"""
        print("\n4. Testing mock server...")
        
        mock = MockServer("TestMock")
        
        # Add mock response
        mock.add_mock(
            method='GET',
            path='api/test',
            response_data={'message': 'test'},
            status_code=200
        )
        
        self.assertIn('GET:api/test', mock.mocks)
        print("   [EMOJI] Mock response added")
        
        # Check mock data
        mock_data = mock.mocks['GET:api/test']
        self.assertEqual(mock_data['status_code'], 200)
        print(f"   [EMOJI] Mock configured: status {mock_data['status_code']}")
    
    # Test 5: Consumer Contract
    def test_05_consumer_contract(self):
        """Test consumer-driven contracts"""
        print("\n5. Testing consumer-driven contracts...")
        
        contract = ConsumerContract("TestConsumer", "TestProvider")
        
        contract.add_interaction(
            description="Get data",
            request={'method': 'GET', 'path': '/api/data'},
            response={'status': 200, 'body': {'data': 'value'}}
        )
        
        self.assertEqual(contract.consumer_name, "TestConsumer")
        self.assertEqual(contract.provider_name, "TestProvider")
        self.assertEqual(len(contract.interactions), 1)
        
        print(f"   [EMOJI] Consumer contract created")
        print(f"   [EMOJI] Interactions: {len(contract.interactions)}")
    
    # Test 6: Request Schema Validation
    def test_06_request_schema_validation(self):
        """Test request schema validation"""
        print("\n6. Testing request schema validation...")
        
        validator = SchemaValidator()
        
        # Valid request
        valid_request = {
            'username': 'test_user',
            'email': 'test@example.com',
            'age': 25
        }
        
        result = validator.validate_request(valid_request, CREATE_USER_REQUEST_SCHEMA)
        self.assertTrue(result['valid'])
        print("   [EMOJI] Valid request passed")
        
        # Invalid request (missing required field)
        invalid_request = {
            'username': 'test_user'
            # Missing email
        }
        
        result = validator.validate_request(invalid_request, CREATE_USER_REQUEST_SCHEMA)
        self.assertFalse(result['valid'])
        print("   [EMOJI] Invalid request rejected")
    
    # Test 7: Response Schema Validation
    def test_07_response_schema_validation(self):
        """Test response schema validation"""
        print("\n7. Testing response schema validation...")
        
        validator = SchemaValidator()
        
        # Valid response
        valid_response = {
            'id': 1,
            'username': 'john_doe',
            'email': 'john@example.com'
        }
        
        result = validator.validate_response(valid_response, USER_RESPONSE_SCHEMA)
        self.assertTrue(result['valid'])
        print("   [EMOJI] Valid response passed")
        
        # Invalid response (missing required field)
        invalid_response = {
            'id': 1,
            'username': 'john_doe'
            # Missing email
        }
        
        result = validator.validate_response(invalid_response, USER_RESPONSE_SCHEMA)
        self.assertFalse(result['valid'])
        print("   [EMOJI] Invalid response rejected")
    
    # Test 8: API Specification
    def test_08_api_specification(self):
        """Test API specification"""
        print("\n8. Testing API specification...")
        
        spec = create_sample_api_spec()
        
        self.assertEqual(spec.title, "User Management API")
        self.assertEqual(spec.version, "1.0.0")
        
        # Check endpoints
        endpoints = spec.get_all_endpoints()
        self.assertGreater(len(endpoints), 0)
        
        print(f"   [EMOJI] API spec created: {spec.title}")
        print(f"   [EMOJI] Endpoints documented: {len(endpoints)}")
    
    # Test 9: OpenAPI Generation
    def test_09_openapi_generation(self):
        """Test OpenAPI specification generation"""
        print("\n9. Testing OpenAPI generation...")
        
        generator = OpenAPIGenerator(
            title="Test API",
            version="1.0.0",
            description="Test API"
        )
        
        generator.add_path(
            path='/api/test',
            method='GET',
            summary='Test endpoint'
        )
        
        spec = generator.generate()
        
        self.assertEqual(spec['openapi'], '3.0.0')
        self.assertIn('/api/test', spec['paths'])
        
        print(f"   [EMOJI] OpenAPI spec generated")
        print(f"   [EMOJI] OpenAPI version: {spec['openapi']}")
    
    # Test 10: Test Helpers
    def test_10_test_helpers(self):
        """Test helper utilities"""
        print("\n10. Testing helper utilities...")
        
        # Test data generation
        schema = {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'age': {'type': 'integer'},
                'active': {'type': 'boolean'}
            }
        }
        
        test_data = generate_test_data(schema)
        
        self.assertIn('name', test_data)
        self.assertIn('age', test_data)
        self.assertIn('active', test_data)
        
        print(f"   [EMOJI] Test data generated: {test_data}")


def run_tests():
    """Run all unit tests"""
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(APIContractTestingTestCase)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
        print(f"Success rate: {success_rate:.1f}%")
    
    if result.failures:
        print("\n[EMOJI] FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\n[EMOJI] ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    if not result.failures and not result.errors:
        print("\n[EMOJI] ALL TESTS PASSED! [EMOJI]")
    
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("API Contract Testing - Unit Test Suite")
    print("=" * 60)
    
    try:
        success = run_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[EMOJI]️  Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n[EMOJI] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
