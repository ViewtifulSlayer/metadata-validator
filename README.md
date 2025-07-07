# 📋 Metadata Validator DX

[![PyPI version](https://img.shields.io/pypi/v/metadata-validator-dx.svg)](https://pypi.org/project/metadata-validator-dx/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-27%2F27%20passing-brightgreen.svg)](https://github.com/ViewtifulSlayer/metadata-validator)

## 🔗 Links

- [PyPI Project](https://pypi.org/project/metadata-validator-dx/)
- [GitHub Repository](https://github.com/ViewtifulSlayer/metadata-validator)
- [Changelog](https://github.com/ViewtifulSlayer/metadata-validator/blob/main/CHANGELOG.md)

A comprehensive Python package for validating and auto-filling metadata in markdown files with smart date normalization, changelog validation, and neurodiversity-aware design.

## 📖 Table of Contents

- [Project Info](#project-info)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Development Transparency](#development-transparency)
- [Testing Framework](#testing-framework)
- [Package Structure](#package-structure)
- [Contributing](#contributing)
- [Documentation](#documentation)
- [Support](#support)
- [License](#license)

## Project Info

- **Author:** ViewtifulSlayer
- **Version:** 1.0.0
- **Status:** Active
- **Category:** Python Package, Metadata Validation
- **License:** MIT

## Features

### Core Validation
- ✅ Required field validation with intelligent suggestions
- ✅ ISO 8601 date format compliance and normalization
- ✅ Automatic date format conversion (20+ formats supported)
- ✅ Content-based title suggestions
- ✅ Graceful error handling and timeout management

### User Experience
- ✅ Three operation modes: Interactive, Auto, and Manual
- ✅ Smart auto-fill with user control
- ✅ Comprehensive help system
- ✅ Progress indicators and clear feedback

### Advanced Features
- ✅ Changelog validation and consistency checking
- ✅ Context-aware placement recommendations
- ✅ Neurodiversity-aware design principles
- ✅ Zero external dependencies (Python standard library only)

## Installation

```bash
# Install from PyPI
pip install metadata-validator-dx

# Or install from source
git clone https://github.com/ViewtifulSlayer/metadata-validator.git
cd metadata-validator
pip install -e .
```
> **Why “DX”?**
> “DX” is a nod to the Game Boy Color era’s “Deluxe” editions—this tool aims to bring that same spirit of enhancement and polish to metadata validation. It was also a simple solution to 'metadata-validator' being an existing project on PyPI.

> **Note:** After installing `metadata-validator-dx`, use the `metadata-validator` command in your terminal.

## Quick Start

```bash
# Validate a markdown file (interactive mode)
metadata-validator path/to/file.md

# Auto-fill missing fields without prompts
metadata-validator path/to/file.md --auto

# Manual mode (report only, no changes)
metadata-validator path/to/file.md --manual

# Disable auto-update of 'Last Updated' field
metadata-validator path/to/file.md --no-auto-update
```

## Usage
 
 ```bash
metadata-validator path/to/file.md
```

### Basic Validation
The metadata validator ensures your markdown files have proper metadata blocks:

```markdown
---
# Metadata
- **Document Title:** Example Document
- **Version:** 1.0.0
- **Author:** Your Name
- **Created:** 2025-01-15
- **Last Updated:** 2025-07-05
- **Status:** Active
- **Category:** Documentation
- **Description:** Brief description of the document
---
```

### Date Format Support
Automatically normalizes 20+ date formats to ISO 8601:

```bash
# These all become 2025-07-05
2025-07-05
07/05/2025
July 5, 2025
5 Jul 2025
2025-07-05T00:00:00
```

### Changelog Integration
Validates changelog consistency and provides smart suggestions:

```bash
# Checks if metadata version matches changelog version
metadata-validator README.md

# Validates both separate CHANGELOG.md and embedded sections
metadata-validator --check-changelog path/to/file.md
```

## Development Transparency

This project was developed with assistance from AI tools, following modern best practices for AI-augmented development:

### **AI Development Tools Used:**
- **Cursor IDE** - AI-powered code completion, refactoring, and development assistance
- **GitHub Copilot** - Code suggestions and documentation help
- **AI Pair Programming** - Collaborative development with AI assistance

### **Development Approach:**
The core logic, architecture decisions, and implementation details were developed collaboratively with AI assistance. This approach enabled:
- **Rapid prototyping** and iterative development
- **Comprehensive testing** with AI-generated test cases
- **Professional documentation** with AI-assisted writing
- **Best practice implementation** following industry standards

### **Quality Assurance:**
- **Human oversight** on all architectural decisions
- **Manual review** of all generated code
- **Comprehensive testing** (27/27 tests passing)
- **Professional standards** maintained throughout development

This transparency reflects our commitment to honest development practices and the evolving landscape of AI-assisted software development.

## Testing Framework

### Phoenix Adversarial Testing
Systematic robustness testing through:
- **Input Validation:** Malformed dates, special characters, whitespace issues
- **Edge Cases:** Large files, missing files, corrupted metadata
- **Performance:** Memory usage, processing time, resource consumption
- **Error Recovery:** Graceful handling of invalid inputs

### Sphinx Cognitive Pattern Testing
Accessibility testing across different cognitive patterns:
- **Linear Thinkers:** Sequential, methodical approaches
- **Non-Linear Thinkers:** Creative, associative approaches
- **Detail Focused:** Precision and exact formatting
- **Big Picture Focused:** Conceptual and approximate approaches
- **Executive Function Challenges:** Task completion and interruption handling

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test suites
python tests/test_phoenix_adversarial.py
python tests/test_sphinx_cognitive.py
python tests/test_date_normalization.py
```

## Package Structure

```
metadata_validator/
├── __init__.py                    # Package initialization
├── metadata_validator.py          # Main validation script
├── config/                        # Configuration management
│   ├── config_loader.py          # Configuration loading
│   └── metadata_standards.json   # Validation standards
├── tests/                         # Comprehensive test suite
│   ├── test_date_normalization.py # Date format testing
│   ├── test_phoenix_adversarial.py # Phoenix adversarial testing
│   ├── test_sphinx_cognitive.py   # Sphinx cognitive pattern analysis
│   └── test_files/               # Test markdown files
└── docs/                         # Documentation
    ├── testing_plan.md           # Comprehensive testing plan
    ├── phoenix_report.md         # Phoenix adversarial testing report
    └── sphinx_report.md          # Sphinx cognitive pattern report
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### For Phoenix Seat Holders
- Focus on robustness and failure mode analysis
- Create comprehensive edge case tests
- Document quality issues and improvements
- Ensure graceful error handling

### For Sphinx Seat Holders
- Analyze usability across cognitive patterns
- Identify accessibility barriers
- Propose adaptive solutions
- Ensure inclusive design principles

## Documentation

- **[Detailed README](docs/README_DETAILED.md):** Comprehensive documentation with competitive analysis
- **[Testing Plan](docs/testing_plan.md):** Comprehensive testing strategy
- **[Phoenix Report](docs/phoenix_report.md):** Adversarial testing results
- **[Sphinx Report](docs/sphinx_report.md):** Cognitive pattern analysis
- **[API Reference](docs/api_reference.md):** Complete API documentation

## Support

- **Issues:** [GitHub Issues](https://github.com/ViewtifulSlayer/metadata-validator/issues)
- **Documentation:** [Full Documentation](https://github.com/ViewtifulSlayer/metadata-validator/tree/main/docs)
- **PyPI:** [Package Page](https://pypi.org/project/metadata-validator-dx/)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Remember:** This package embodies the collaborative wisdom of both Phoenix and Sphinx seats, ensuring that the metadata validator is both robust against failure and accessible to all minds.

*"From the ashes of failure, we rise with renewed wisdom and strength."* - Phoenix Motto

*"The riddle of the Sphinx is not to be solved by one mind alone, but by the synthesis of many minds working together."* - Sphinx Motto 