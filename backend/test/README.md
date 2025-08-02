# Mental Health Platform Repository Test Suite

## Overview

This test suite provides comprehensive testing for the mental health wellness platform repository system. It includes unit tests, integration tests, and clinical workflow validation to ensure data integrity, healthcare compliance, and robust error handling.

## Test Structure

```
backend/test/
├── conftest.py                          # Test configuration and fixtures
├── test_base_repository.py              # Base repository functionality tests
├── test_integration_workflows.py        # Clinical workflow integration tests
└── README.md                           # This file
```

## Test Categories

### 1. Unit Tests

**Base Repository Tests (`test_base_repository.py`)**
- CRUD operations (Create, Read, Update, Delete)
- Query functionality with filters and pagination
- Transaction management
- Error handling and validation
- Entity existence checking and counting

### 2. Integration Tests

**Clinical Workflow Tests (`test_integration_workflows.py`)**
- Patient intake and treatment planning workflows
- Crisis detection and emergency response workflows
- Treatment progress tracking across multiple sessions
- Medication adherence monitoring workflows
- Care coordination and referral management workflows

## Test Fixtures

The `conftest.py` file provides comprehensive test fixtures:

### Core Fixtures
- `mock_db_manager`: Mock database manager for isolated testing
- `mock_logger`: Mock logger for testing log operations
- `sample_patient_id`, `sample_therapist_id`, `sample_provider_id`: Standard IDs for consistent testing

### Clinical Entity Fixtures
- `sample_therapeutic_relationship`: Mock therapeutic relationship
- `sample_treatment_plan`: Mock treatment plan with CBT focus
- `sample_therapy_session`: Mock individual therapy session
- `sample_mood_entry`: Mock patient mood tracking entry
- `sample_journal_entry`: Mock therapeutic journal entry
- `sample_crisis_detection`: Mock crisis detection with high severity
- `sample_safety_plan`: Mock comprehensive safety plan

### Utility Functions
- `create_mock_query_result()`: Creates standardized query results
- `mock_db_response()`: Configures mock database responses

## Running Tests

### Prerequisites

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock pytest-asyncio
```

### Execute Tests

```bash
# Run all tests
pytest backend/test/ -v

# Run with coverage report
pytest backend/test/ --cov=backend/happypath/repository --cov-report=html

# Run specific test files
pytest backend/test/test_base_repository.py -v
pytest backend/test/test_integration_workflows.py -v

# Run tests with markers (if implemented)
pytest backend/test/ -m "unit" -v        # Unit tests only
pytest backend/test/ -m "integration" -v # Integration tests only
pytest backend/test/ -m "clinical" -v    # Clinical workflow tests
```

### Test Output

```bash
# Example successful test run
========================= test session starts =========================
platform darwin -- Python 3.9.7, pytest-7.2.0, pluggy-1.0.0
rootdir: /Users/leiliu/projects/happy_path
collected 15 items

backend/test/test_base_repository.py::TestBaseRepository::test_create_entity_success PASSED
backend/test/test_base_repository.py::TestBaseRepository::test_get_by_id_found PASSED
backend/test/test_base_repository.py::TestBaseRepository::test_update_entity_success PASSED
backend/test/test_base_repository.py::TestBaseRepository::test_delete_entity_success PASSED
backend/test/test_integration_workflows.py::TestClinicalWorkflows::test_complete_patient_intake_workflow PASSED
backend/test/test_integration_workflows.py::TestClinicalWorkflows::test_crisis_detection_and_response_workflow PASSED

========================= 15 passed in 2.34s =========================
```

## Test Design Principles

### 1. Isolation
- Each test is independent and can run in any order
- Mock dependencies to avoid external system calls
- Use fixtures for consistent test data setup

### 2. Clinical Realism
- Test scenarios reflect real healthcare workflows
- Include edge cases specific to mental health treatment
- Validate healthcare compliance requirements

### 3. Comprehensive Coverage
- Test both happy path and error conditions
- Include boundary value testing
- Cover all repository methods and workflows

### 4. Performance Consideration
- Mock database operations for fast test execution
- Use async fixtures where appropriate
- Minimize test setup and teardown time

## Healthcare-Specific Testing

### HIPAA Compliance Testing
- Verify audit logging for all data access
- Test data encryption and privacy controls
- Validate user authorization and access controls

### Clinical Safety Testing
- Crisis detection accuracy and response times
- Safety plan accessibility and completeness
- Emergency escalation procedures

### Treatment Workflow Testing
- Multi-step clinical processes
- Data consistency across related entities
- Progress tracking and outcome measurement

## Adding New Tests

### 1. Unit Tests for New Repositories

```python
# Example: test_new_repository.py
import pytest
from backend.happypath.repository import NewRepository

class TestNewRepository:
    @pytest.fixture
    def new_repo(self, mock_db_manager, mock_logger):
        return NewRepository(mock_db_manager, mock_logger)
    
    def test_create_new_entity(self, new_repo, mock_db_manager):
        # Arrange
        entity_data = {"field": "value"}
        mock_db_manager.execute_query.return_value = [{"id": 1, "field": "value"}]
        
        # Act
        result = new_repo.create(entity_data)
        
        # Assert
        assert result.field == "value"
        mock_db_manager.execute_query.assert_called_once()
```

### 2. Integration Tests for New Workflows

```python
# Add to test_integration_workflows.py
def test_new_clinical_workflow(self, repositories, mock_db_manager):
    """Test new clinical workflow integration."""
    # Arrange - Setup mock responses
    # Act - Execute workflow steps
    # Assert - Verify expected outcomes and method calls
```

### 3. Test Fixtures for New Entities

```python
# Add to conftest.py
@pytest.fixture
def sample_new_entity(sample_patient_id):
    """Sample new entity for testing."""
    return NewEntity(
        patient_id=sample_patient_id,
        # ... other fields
    )
```

## Continuous Integration

### GitHub Actions Configuration

```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10]
    
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-mock
      
      - name: Run tests
        run: |
          pytest backend/test/ --cov=backend/happypath/repository --cov-report=xml
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
```

## Coverage Goals

### Minimum Coverage Targets
- **Overall**: 90% code coverage
- **Critical Paths**: 95% coverage for crisis management and safety features
- **Business Logic**: 100% coverage for clinical workflow logic
- **Error Handling**: 100% coverage for exception paths

### Coverage Reports

```bash
# Generate HTML coverage report
pytest backend/test/ --cov=backend/happypath/repository --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
```

## Performance Testing

### Load Testing Considerations

```python
@pytest.mark.performance
def test_high_volume_mood_entries(self, mood_repo, mock_db_manager):
    """Test repository performance with high volume data."""
    # Simulate 1000 mood entries
    entries = [create_sample_mood_entry() for _ in range(1000)]
    
    start_time = time.time()
    for entry in entries:
        mood_repo.create(entry)
    execution_time = time.time() - start_time
    
    # Assert reasonable performance
    assert execution_time < 5.0  # Should complete in under 5 seconds
```

## Debugging Failed Tests

### Common Issues and Solutions

1. **Import Errors**
   ```bash
   # Ensure proper Python path
   export PYTHONPATH="${PYTHONPATH}:/path/to/project"
   ```

2. **Mock Configuration Issues**
   ```python
   # Verify mock return values match expected data structure
   mock_db.execute_query.return_value = [{"expected": "format"}]
   ```

3. **Fixture Dependencies**
   ```python
   # Check fixture dependency order in conftest.py
   @pytest.fixture
   def dependent_fixture(base_fixture):  # base_fixture must be defined first
   ```

4. **Test Isolation Problems**
   ```python
   # Reset mocks between tests
   mock_db.reset_mock()
   ```

## Best Practices

### 1. Test Naming
- Use descriptive test method names: `test_create_user_with_valid_data_succeeds`
- Include expected outcome in name: `test_get_nonexistent_user_returns_none`

### 2. Test Structure (AAA Pattern)
```python
def test_example(self, repository, mock_db):
    # Arrange - Set up test data and mocks
    test_data = {"field": "value"}
    mock_db.execute_query.return_value = [expected_result]
    
    # Act - Execute the operation being tested
    result = repository.method(test_data)
    
    # Assert - Verify the expected outcomes
    assert result.field == "value"
    mock_db.execute_query.assert_called_once()
```

### 3. Error Testing
```python
def test_invalid_input_raises_validation_error(self, repository):
    # Test both the exception type and message
    with pytest.raises(ValidationError, match="Expected error message"):
        repository.create(invalid_data)
```

### 4. Async Testing
```python
@pytest.mark.asyncio
async def test_async_operation(self, async_repository, mock_db):
    # Use async fixtures and await async operations
    result = await async_repository.async_method()
    assert result is not None
```

This comprehensive test suite ensures the mental health platform repository system meets the highest standards for healthcare software quality, safety, and reliability.
