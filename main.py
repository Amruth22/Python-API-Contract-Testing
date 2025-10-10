"""
API Contract Testing - Main Demonstration
Shows examples of all contract testing features
"""

from contracts.contract_definition import APIContract, get_user_contract, create_user_contract, list_users_contract
from contracts.contract_validator import ContractValidator
from contracts.consumer_contracts import mobile_app_user_contract, web_app_order_contract
from mocks.mock_server import create_user_mock_server
from mocks.mock_responses import get_mock_response
from schema.schema_validator import SchemaValidator
from schema.request_schemas import CREATE_USER_REQUEST_SCHEMA
from schema.response_schemas import USER_RESPONSE_SCHEMA
from documentation.api_spec import create_sample_api_spec
from documentation.doc_validator import DocumentationValidator
from documentation.openapi_generator import OpenAPIGenerator
from testing.contract_tests import ContractTestRunner


def print_section(title):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_contract_definition():
    """Demonstrate contract definition"""
    print_section("1. Contract Definition")
    
    # Create a contract
    contract = APIContract(
        name="GetUser",
        method="GET",
        path="/api/users/1",
        description="Get user by ID"
    ).with_response_schema({
        'type': 'object',
        'required': ['id', 'username', 'email'],
        'properties': {
            'id': {'type': 'integer'},
            'username': {'type': 'string'},
            'email': {'type': 'string'}
        }
    }).with_status(200)
    
    print("\n📝 Contract Created:")
    print(f"   Name: {contract.name}")
    print(f"   Method: {contract.method}")
    print(f"   Path: {contract.path}")
    print(f"   Expected Status: {contract.expected_status}")
    print(f"   Has Response Schema: {contract.response_schema is not None}")


def demo_schema_validation():
    """Demonstrate schema validation"""
    print_section("2. Schema Validation")
    
    validator = SchemaValidator()
    
    # Valid data
    print("\n✅ Testing valid data:")
    valid_data = {
        'username': 'john_doe',
        'email': 'john@example.com',
        'age': 30
    }
    
    result = validator.validate(valid_data, CREATE_USER_REQUEST_SCHEMA)
    print(f"   Valid: {result['valid']}")
    
    # Invalid data
    print("\n❌ Testing invalid data:")
    invalid_data = {
        'username': 'ab',  # Too short
        'email': 'invalid-email'  # Invalid format
    }
    
    result = validator.validate(invalid_data, CREATE_USER_REQUEST_SCHEMA)
    print(f"   Valid: {result['valid']}")
    if not result['valid']:
        print(f"   Errors: {len(result['errors'])} validation errors")


def demo_mock_server():
    """Demonstrate mock server"""
    print_section("3. Mock Server")
    
    # Create mock server
    mock = create_user_mock_server()
    
    print("\n🎭 Mock Server Created:")
    print(f"   Mocks registered: {len(mock.mocks)}")
    
    # Show registered mocks
    print("\n📋 Registered Mocks:")
    for key in mock.mocks.keys():
        print(f"   - {key}")


def demo_consumer_contracts():
    """Demonstrate consumer-driven contracts"""
    print_section("4. Consumer-Driven Contracts")
    
    # Create consumer contract
    contract = mobile_app_user_contract()
    
    print(f"\n📱 Consumer Contract:")
    print(f"   Consumer: {contract.consumer_name}")
    print(f"   Provider: {contract.provider_name}")
    print(f"   Interactions: {len(contract.interactions)}")
    
    # Show interactions
    print("\n📋 Interactions:")
    for i, interaction in enumerate(contract.interactions, 1):
        print(f"   {i}. {interaction['description']}")
        print(f"      Request: {interaction['request']['method']} {interaction['request']['path']}")
        print(f"      Expected Status: {interaction['response']['status']}")


def demo_api_specification():
    """Demonstrate API specification"""
    print_section("5. API Specification")
    
    # Create API spec
    spec = create_sample_api_spec()
    
    print(f"\n📚 API Specification:")
    print(f"   Title: {spec.title}")
    print(f"   Version: {spec.version}")
    print(f"   Base URL: {spec.base_url}")
    print(f"   Endpoints: {len(spec.endpoints)}")
    
    # Show endpoints
    print("\n📋 Documented Endpoints:")
    for path, methods in spec.endpoints.items():
        for method in methods.keys():
            print(f"   - {method} {path}")


def demo_openapi_generation():
    """Demonstrate OpenAPI generation"""
    print_section("6. OpenAPI Generation")
    
    # Create OpenAPI generator
    generator = OpenAPIGenerator(
        title="User Management API",
        version="1.0.0",
        description="API for managing users"
    )
    
    # Add paths
    generator.add_path(
        path='/api/users',
        method='GET',
        summary='Get all users',
        response_schema=USER_RESPONSE_SCHEMA
    )
    
    generator.add_path(
        path='/api/users',
        method='POST',
        summary='Create user',
        request_schema=CREATE_USER_REQUEST_SCHEMA,
        response_schema=USER_RESPONSE_SCHEMA,
        status_code=201
    )
    
    # Generate spec
    openapi_spec = generator.generate()
    
    print("\n📄 OpenAPI Specification Generated:")
    print(f"   OpenAPI Version: {openapi_spec['openapi']}")
    print(f"   API Title: {openapi_spec['info']['title']}")
    print(f"   API Version: {openapi_spec['info']['version']}")
    print(f"   Paths: {len(openapi_spec['paths'])}")


def demo_mock_responses():
    """Demonstrate mock responses"""
    print_section("7. Mock Responses")
    
    # Get mock responses
    user_response = get_mock_response('user', 'get_user')
    list_response = get_mock_response('user', 'list_users')
    error_response = get_mock_response('error', 'not_found')
    
    print("\n🎭 Mock Response Examples:")
    print(f"\n   User Response:")
    print(f"   {user_response}")
    
    print(f"\n   List Response:")
    print(f"   Users: {len(list_response['users'])}")
    print(f"   Count: {list_response['count']}")
    
    print(f"\n   Error Response:")
    print(f"   {error_response}")


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 70)
    print("  API Contract Testing - Demonstration")
    print("=" * 70)
    
    try:
        demo_contract_definition()
        demo_schema_validation()
        demo_mock_server()
        demo_consumer_contracts()
        demo_api_specification()
        demo_openapi_generation()
        demo_mock_responses()
        
        print("\n" + "=" * 70)
        print("  All Demonstrations Completed!")
        print("=" * 70)
        print("\nKey Concepts Demonstrated:")
        print("  1. Contract Definition - Define API contracts")
        print("  2. Schema Validation - Validate JSON schemas")
        print("  3. Mock Server - Simulate API responses")
        print("  4. Consumer-Driven Contracts - Consumer expectations")
        print("  5. API Specification - Document APIs")
        print("  6. OpenAPI Generation - Generate OpenAPI specs")
        print("  7. Mock Responses - Predefined test data")
        print("\nTo run Flask API:")
        print("  python api/app.py")
        print("\nTo run tests:")
        print("  python tests.py")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
