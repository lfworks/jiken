# CLAUDE.md

This document describes the guidelines that Claude should follow when generating code for this project.

## Project Philosophy

- **Efficient library**: Provide the minimum features necessary to fulfill simple, focused responsibilities
- **Minimize dependencies**: Keep third-party library dependencies to a minimum
  - Every additional dependency degrades overall software quality

## Coding Conventions

### Naming Rules
- **Class names**: CamelCase
- **Function/method names**: snake_case
- **Private members**: Prefix with underscore (`_`)
- **Type hints**: Use wherever possible
- **Docstrings**: Google style, written concisely in English
- **Error messages**: Written in English

### Exception Handling Guidelines
- **Exception chaining**: Use the form `raise NewException(msg) from original_exception`
  - Preserves the original exception information so the root cause can be traced during debugging
  - Reference: [Python Exception Handling Docs](https://docs.python.org/3/library/exceptions.html#exception-context)
- **Avoid unnecessary variable assignments**: Write error messages inline; avoid intermediate variables like `error_msg`

### Design Principles
- **SRP (Single Responsibility Principle)**: Each class should have only one responsibility
- **Encapsulate in classes**: Default to class-based design to facilitate future extension and dependency injection
- **Testability**: Abstract external I/O so it can be easily mocked/patched
- **Favor composition over inheritance**: Keep inheritance hierarchies shallow; prefer composition
  - Use Python's `typing.Protocol` to define interfaces

## Testing Best Practices

### Test Structure and Layout
- **Unit tests**: Place under the `test/` directory
- **No external dependencies**: No DB connections or HTTP calls in tests
- **Test data**: Place under `test/test_data/`

### Using Mock/Patch
- **Mock external services**: Mock all external service calls appropriately
- **Use create_autospec**: Create mocks with `unittest.mock.create_autospec(Class, instance=True)` to enforce the actual class interface
- **Avoid sloppy setUp**: Set up only the dependencies needed for each test method
- **Do not mock Logger**: Verifying log output is not required

### Table-Driven Tests
When testing multiple parameters or scenarios, use `@parameterized.expand` to implement table-driven tests:

```python
from parameterized import parameterized

class ExampleTestCase(unittest.TestCase):
    @parameterized.expand(
        [
            # Test case 1: happy path
            (
                # input data
                {"input": "valid_data", "flag": True},
                # expected
                ("expected_output", 200),
            ),
            # Test case 2: error path
            (
                {"input": None, "flag": False},
                (None, None),
            ),
        ]
    )
    def test_example_function(self, input_data, expected):
        result = example_function(input_data)
        self.assertEqual(expected, result)
```

## Implementation Guidelines

### 1. Before Writing New Code
- Check whether similar functionality already exists
- Consider reusing common utilities
- Make appropriate use of configuration files

### 2. When Handling External Data Sources
- Account for rate limiting
- Implement proper error handling
- Implement retry mechanisms

### 3. When Processing Large Amounts of Data
- Monitor memory usage
- Implement batch processing
- Report progress appropriately

### 4. Writing Tests
- Test both happy paths and error paths
- Use mocks to eliminate external dependencies
- Consider edge cases
