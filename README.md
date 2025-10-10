# API Contract Testing

Educational Python application demonstrating **API contract testing**, **mock services**, **consumer-driven contracts**, **schema validation testing**, and **automated API documentation testing**.

## Features

### 📝 API Contract Testing
- **Contract Definitions** - Define expected API behavior
- **Contract Validation** - Verify API matches contract
- **Request/Response Validation** - Check data format
- **Status Code Validation** - Verify correct HTTP codes
- **Contract Registry** - Manage all contracts

### 🎭 Mock Services
- **Mock Server** - Simulate API responses
- **Predefined Responses** - Test data for mocking
- **Request Matching** - Match requests to responses
- **Mock Manager** - Manage multiple mocks
- **Mock Scenarios** - Define testing scenarios

### 👥 Consumer-Driven Contracts
- **Consumer Expectations** - What consumers expect
- **Provider Verification** - Provider meets expectations
- **Interaction Definitions** - Define request/response pairs
- **Contract Registry** - Store consumer contracts
- **Multi-Consumer Support** - Multiple consumers per provider

### ✅ Schema Validation
- **JSON Schema** - Validate data structure
- **Request Validation** - Validate incoming requests
- **Response Validation** - Validate outgoing responses
- **Schema Registry** - Store all schemas
- **Detailed Error Messages** - Clear validation errors

### 📚 Automated Documentation Testing
- **API Specification** - Define API documentation
- **Documentation Validator** - Test docs match reality
- **OpenAPI Generation** - Generate OpenAPI 3.0 specs
- **Endpoint Verification** - Verify all endpoints documented
- **Spec Export** - Save specifications to files

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Amruth22/Python-API-Contract-Testing.git
cd Python-API-Contract-Testing
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Demonstrations
```bash
python main.py
```

### 5. Run Flask API
```bash
python api/app.py
```

### 6. Run Tests
```bash
python tests.py
```

## Project Structure

```
Python-API-Contract-Testing/
│
├── contracts/
│   ├── contract_definition.py   # Contract definitions
│   ├── contract_validator.py    # Contract validation
│   └── consumer_contracts.py    # Consumer contracts
│
├── mocks/
│   ├── mock_server.py           # Mock service
│   ├── mock_responses.py        # Mock data
│   └── mock_manager.py          # Mock management
│
├── schema/
│   ├── schema_validator.py      # Schema validation
│   ├── request_schemas.py       # Request schemas
│   └── response_schemas.py      # Response schemas
│
├── documentation/
│   ├── api_spec.py              # API specification
│   ├── doc_validator.py         # Doc validator
│   └── openapi_generator.py     # OpenAPI generator
│
├── testing/
│   ├── contract_tests.py        # Contract test runner
│   └── test_helpers.py          # Test utilities
│
├── api/
│   └── app.py                   # Flask API (provider)
│
├── main.py                      # Demonstration
├── tests.py                     # 10 unit tests
└── README.md                    # This file
```

## Usage Examples

### Define a Contract

```python
from contracts.contract_definition import APIContract

# Create contract
contract = APIContract(
    name="GetUser",
    method="GET",
    path="/api/users/1"
).with_response_schema({
    'type': 'object',
    'required': ['id', 'username', 'email'],
    'properties': {
        'id': {'type': 'integer'},
        'username': {'type': 'string'},
        'email': {'type': 'string'}
    }
}).with_status(200)
```

### Validate Contract

```python
from contracts.contract_validator import ContractValidator

validator = ContractValidator()

# Validate API against contract
result = validator.validate_contract(contract, "http://localhost:5000")

if result['passed']:
    print("Contract validation passed!")
else:
    print(f"Errors: {result['errors']}")
```

### Create Mock Server

```python
from mocks.mock_server import MockServer

# Create mock
mock = MockServer("UserMock")

# Add mock response
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

# Run mock server
mock.run(port=5001)
```

### Validate Schema

```python
from schema.schema_validator import SchemaValidator

validator = SchemaValidator()

# Validate data
data = {
    'username': 'john_doe',
    'email': 'john@example.com'
}

result = validator.validate(data, CREATE_USER_REQUEST_SCHEMA)

if result['valid']:
    print("Schema validation passed!")
else:
    print(f"Errors: {result['errors']}")
```

### Consumer-Driven Contract

```python
from contracts.consumer_contracts import ConsumerContract

# Consumer defines what they expect
contract = ConsumerContract("MobileApp", "UserAPI")

contract.add_interaction(
    description="Get user profile",
    request={
        'method': 'GET',
        'path': '/api/users/1'
    },
    response={
        'status': 200,
        'body': {
            'id': 1,
            'username': 'string',
            'email': 'string'
        }
    }
)

# Provider must satisfy this contract
```

### Generate OpenAPI Spec

```python
from documentation.openapi_generator import OpenAPIGenerator

generator = OpenAPIGenerator(
    title="User API",
    version="1.0.0",
    description="User management API"
)

generator.add_path(
    path='/api/users',
    method='GET',
    summary='Get all users',
    response_schema=USER_LIST_RESPONSE_SCHEMA
)

# Generate spec
openapi_spec = generator.generate()

# Save to file
generator.save_to_file('openapi.json')
```

## Contract Testing Flow

```
1. Define Contract
   ↓
2. Consumer specifies expectations
   ↓
3. Provider implements API
   ↓
4. Validate contract
   - Check status code
   - Validate request schema
   - Validate response schema
   ↓
5. Test passes/fails
   ↓
6. Generate documentation
```

## Testing

Run the comprehensive test suite:

```bash
python tests.py
```

### Test Coverage (10 Tests)

1. ✅ **Contract Definition** - Test contract creation
2. ✅ **Contract Registry** - Test contract storage
3. ✅ **Schema Validation** - Test JSON schema validation
4. ✅ **Mock Server** - Test mock responses
5. ✅ **Consumer Contract** - Test consumer-driven contracts
6. ✅ **Request Validation** - Test request schema
7. ✅ **Response Validation** - Test response schema
8. ✅ **API Specification** - Test API docs
9. ✅ **OpenAPI Generation** - Test OpenAPI spec
10. ✅ **Test Helpers** - Test utility functions

## Educational Notes

### 1. What is Contract Testing?

**Contract testing** verifies that an API provider meets the expectations (contract) defined by its consumers.

**Benefits:**
- Catch breaking changes early
- Ensure API compatibility
- Enable independent development
- Provide clear API expectations

### 2. Consumer-Driven Contracts

**Concept:** Consumers define what they need from the API, and providers must satisfy those contracts.

**Workflow:**
1. Consumer defines contract
2. Provider implements to satisfy contract
3. Automated tests verify contract
4. Both sides can evolve safely

### 3. Schema Validation

**Purpose:** Ensure data structure matches expected format

**JSON Schema:**
- Define data types
- Required fields
- Validation rules
- Format constraints

### 4. Mock Services

**Why Mock?**
- Test without real API
- Simulate error scenarios
- Fast and reliable tests
- No external dependencies

### 5. API Documentation Testing

**Problem:** Documentation often becomes outdated

**Solution:** Automated tests verify docs match reality

## Production Considerations

For production use:

1. **Contract Testing Tools:**
   - Use Pact for consumer-driven contracts
   - Implement contract versioning
   - Set up contract broker

2. **Schema Management:**
   - Version schemas
   - Implement schema evolution
   - Use schema registry

3. **Documentation:**
   - Auto-generate from code
   - Keep docs in sync
   - Use OpenAPI/Swagger

4. **Testing:**
   - Run contract tests in CI/CD
   - Test against staging
   - Monitor contract compliance

## Dependencies

- **Flask 3.0.0** - Web framework
- **jsonschema 4.20.0** - JSON schema validation
- **python-dotenv 1.0.0** - Environment variables
- **pytest 7.4.3** - Testing framework
- **requests 2.31.0** - HTTP client

## License

This project is for educational purposes. Feel free to use and modify as needed.

---

**Happy Testing! 🚀**
