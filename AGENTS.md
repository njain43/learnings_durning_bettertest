# AGENTS.md - Codebase Guide for AI Agents

## Project Overview

A Python learning/exploration project containing modular systems for data encoding, binary conversion, network communication, and testing frameworks. Used for studying HackerRank problems, Robot Framework automation, and building reusable codec/indexing components.

## Core Architecture

### Module Structure
- **`src/codec/`** - Binary serialization layer using Python's `struct` module
  - `ByteDecoder`: Unpacks binary data (uint_16, uint_8, char_arr, float)
  - `ByteEncoder`: Packs data into binary format
  - Uses ABC (Abstract Base Class) as interface pattern

- **`src/converter_indexer/`** - JSON↔Bytes conversion system
  - `Converter`: Orchestrates encoding/decoding via field definitions
  - `Indexer`: Reads `fields.json` and `order.json` from `samples/` to build field mapping (fn2ft2fd dict)
  - **Key pattern**: Field metadata stored in JSON, runtime conversion orchestrated through converter

- **`src/network/http/`** - HTTP client wrapper
  - `Http` class wraps `requests` library with configurable endpoints
  - Supports GET/POST with optional JSON data serialization

- **`tests/`** - Test structure separated into `unit/` and `integration/`
  - Uses `unittest.TestCase` with lifecycle methods (setUpClass, tearDownClass)
  - Some tests marked with `@skip` decorator (e.g., http tests)

## Critical Workflows

### Running Tests
```bash
# Export paths first - required for imports to resolve
export PYTHONPATH=./src:./tests

# Run all tests (unit + integration)
pytest tests/unit tests/integration

# Conda environment management
conda activate hackerrankquestions
conda env update --name hackerrankquestions --file packaging/recipe.yml
```

### Environment Setup
- **Dependency management**: `conda` (see `packaging/recipe.yml`)
- **CI/CD**: GitLab CI (`.gitlab-ci.yml`) runs pytest on build stage
- **Core dependencies**: `requests`, `pytest`
- **Python version note**: Code comments reference upgrading to Python 3.10 for match/case statements

### Local Development
- **PYTHONPATH requirement**: Must include `./src:./tests` for imports
- **Conda environment**: Named `hackerrankquestions` - activate before testing
- **IDE setup**: `.idea/` folder present (IntelliJ/PyCharm project)

## Project-Specific Patterns

### Import Structure
```python
# Always use absolute imports from src root
from src.codec.decoder import ByteDecoder
from src.converter_indexer.indexer import Indexer
from src.random_program.calculator import Calculator
```

### Field Configuration Pattern
The converter_indexer module expects two JSON files in `src/converter_indexer/samples/`:
- `fields.json`: Contains `message_definition` array with field name/type pairs
- `order.json`: Contains actual field values keyed by field name
- Runtime creates mapping: `{field_name: {f_name, f_type, f_value}}`

### Type Handling in Codec
Supported data types (hardcoded if/elif pattern, not match/case due to Python version):
- `uint_16`, `uint_8`: Integer types using `<H` and `<h` format strings
- `char_arr`: Multi-character string decoded from UTF-8
- `char`: Single character
- `float`: Double precision float

### Test Lifecycle Pattern
```python
class TestExample(TestCase):
    @classmethod
    def setUpClass(cls):  # Runs once per test class
        cls.resource = SomeClass()
    
    def setUp(self):     # Runs before each test
        pass
    
    def tearDown(self):  # Runs after each test
        pass
    
    @classmethod
    def tearDownClass(cls):  # Runs once after all tests
        pass
```

## Integration Points & Conventions

### External Dependencies
- **requests**: For HTTP operations, wrapped by `Http` class
- **pytest**: Test runner (preferred over unittest runner)
- **Robot Framework**: Integration testing framework (see `tests/robot_framework/`)
- **struct module**: Core codec dependency for binary packing/unpacking

### Cross-Component Communication
1. Converter → Indexer: Indexer provides field metadata dictionary
2. Indexer → JSON files: Reads from `samples/` directory
3. Converter → Codec: Routes through encoder/decoder based on field type
4. Http → requests: Thin wrapper for JSON serialization/response handling

### File Organization Convention
- Source code in `src/{module}/{module_file}.py`
- Matching tests in `tests/{unit|integration}/{module}/{test_file}.py`
- Shared test data in module's `samples/` subdirectory
- Documentation in `readme/` with markdown files for build, docker setup

## Key Files Reference

| File | Purpose |
|------|---------|
| `.gitlab-ci.yml` | CI pipeline - exports PYTHONPATH, runs pytest |
| `packaging/recipe.yml` | Conda environment spec (requests, pytest) |
| `src/converter_indexer/samples/fields.json` | Field schema for conversion |
| `readme/build.md` | Dev environment setup instructions |
| `tests/unit/codec/test_decoder.py` | Example test pattern with setUp |

## Common Pitfalls & Notes

1. **PYTHONPATH**: Forgetting to export before running tests causes import errors
2. **Binary format strings**: Use `<` prefix for little-endian; without breaks platform compatibility
3. **Method naming**: Note typo pattern in codebase: `unit_8` (should be `uint_8`), `substract` (should be `subtract`)
4. **Integration tests**: Some tests marked `@skip` - verify status before running full suite
5. **Encoder return**: `ByteEncoder.value()` returns list of bytes; join with `b''.join()` if needed

