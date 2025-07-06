#!/usr/bin/env python3
"""
One-Click Workspace Integration Script

This script automates the integration of the metadata validator into any workspace.
Run this script from your workspace root to set up the metadata validator for agent use.

Usage: python setup_integration.py

Author: ViewtifulSlayer
Version: 1.0.0
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def print_step(step_num, title, description=""):
    """Print a formatted step header."""
    print(f"\n{'='*60}")
    print(f"🔧 STEP {step_num}: {title}")
    print(f"{'='*60}")
    if description:
        print(f"📝 {description}")

def print_success(message):
    """Print a success message."""
    print(f"✅ {message}")

def print_error(message):
    """Print an error message."""
    print(f"❌ {message}")

def print_info(message):
    """Print an info message."""
    print(f"ℹ️  {message}")

def check_python_version():
    """Check if Python version is compatible."""
    print_step(1, "Checking Python Version")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print_error(f"Python 3.7+ required. Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print_success(f"Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def setup_metadata_validator():
    """Set up the metadata validator in the current workspace."""
    print_step(2, "Setting Up Metadata Validator")
    
    # Get current directory (workspace root)
    workspace_root = Path.cwd()
    metadata_dir = workspace_root / "metadata_validator"
    
    # Check if metadata_validator already exists
    if metadata_dir.exists():
        print_info("Metadata validator directory already exists")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print_info("Skipping metadata validator setup")
            return metadata_dir
    
    # Copy the metadata validator to workspace
    try:
        # Get the directory where this script is located
        script_dir = Path(__file__).parent
        source_dir = script_dir
        
        # Copy the entire metadata_validator package
        if metadata_dir.exists():
            shutil.rmtree(metadata_dir)
        
        shutil.copytree(source_dir, metadata_dir)
        print_success(f"Metadata validator copied to {metadata_dir}")
        
        return metadata_dir
    except Exception as e:
        print_error(f"Failed to copy metadata validator: {e}")
        return None

def create_agent_helper():
    """Create the agent helper script."""
    print_step(3, "Creating Agent Helper Script")
    
    helper_content = '''#!/usr/bin/env python3
"""
Agent Metadata Helper

This script provides easy integration functions for agents to use the metadata validator.
Import this in your agent code to access metadata validation functionality.

Author: ViewtifulSlayer
Version: 1.0.0
"""

import sys
import os
import subprocess
from pathlib import Path

def setup_metadata_validator(workspace_path=None):
    """Setup metadata validator for agent use."""
    if workspace_path is None:
        workspace_path = Path.cwd()
    
    metadata_path = Path(workspace_path) / "metadata_validator"
    if str(metadata_path) not in sys.path:
        sys.path.append(str(metadata_path))
    return metadata_path

def validate_file_metadata(file_path, mode="--manual"):
    """Validate metadata for a markdown file."""
    try:
        # Get the metadata validator script path
        workspace_path = Path.cwd()
        validator_script = workspace_path / "metadata_validator" / "metadata_validator.py"
        
        if not validator_script.exists():
            return False, "", "Metadata validator not found"
        
        # Run validation
        result = subprocess.run([
            sys.executable, 
            str(validator_script), 
            str(file_path), 
            mode
        ], capture_output=True, text=True, cwd=workspace_path)
        
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def normalize_date(date_str):
    """Normalize date format to ISO 8601."""
    try:
        setup_metadata_validator()
        from metadata_validator import normalize_date_format
        return normalize_date_format(date_str)
    except Exception as e:
        return date_str, False, "error"

def validate_batch(files, mode="--manual"):
    """Validate multiple files and return results."""
    results = []
    for file_path in files:
        success, output, error = validate_file_metadata(file_path, mode)
        results.append({
            'file': file_path,
            'success': success,
            'output': output,
            'error': error
        })
    return results

def find_markdown_files(directory=".", recursive=True):
    """Find all markdown files in the given directory."""
    pattern = "**/*.md" if recursive else "*.md"
    return list(Path(directory).glob(pattern))

# Quick usage examples
if __name__ == "__main__":
    print("🧪 Testing Agent Helper Functions")
    print("=" * 40)
    
    # Test setup
    setup_metadata_validator()
    print("✅ Setup completed")
    
    # Test date normalization
    test_dates = ["7/5/25", "2025.07.05", "Jul 5, 2025"]
    for date in test_dates:
        normalized, changed, format_type = normalize_date(date)
        print(f"📅 {date} → {normalized} ({format_type})")
    
    # Test file validation (if test file exists)
    test_file = Path("test_document.md")
    if test_file.exists():
        success, output, error = validate_file_metadata(test_file)
        print(f"📄 {test_file}: {'✅ Valid' if success else '❌ Invalid'}")
    else:
        print("📄 No test file found (create test_document.md to test validation)")
'''
    
    helper_path = Path.cwd() / "agent_metadata_helper.py"
    try:
        with open(helper_path, 'w') as f:
            f.write(helper_content)
        print_success(f"Agent helper script created: {helper_path}")
        return helper_path
    except Exception as e:
        print_error(f"Failed to create agent helper: {e}")
        return None

def create_test_file():
    """Create a test markdown file for validation."""
    print_step(4, "Creating Test File")
    
    test_content = '''---
# Metadata
- **Document Title:** Test Document
- **Author:** Test User
- **Created:** 7/5/25
- **Last Updated:** 2025.07.05
- **Version:** 1.0.0
- **Description:** Test document for metadata validation
---

# Test Content

This is a test document created by the integration setup script.

## Features to Test

- Date normalization (7/5/25 → 2025-07-05)
- Date normalization (2025.07.05 → 2025-07-05)
- Required field validation
- Metadata block parsing

## Usage

Run the metadata validator on this file to test the integration:

```bash
python metadata_validator/metadata_validator.py test_document.md --manual
```

Or use the agent helper:

```python
from agent_metadata_helper import validate_file_metadata
success, output, error = validate_file_metadata("test_document.md")
```
'''
    
    test_path = Path.cwd() / "test_document.md"
    try:
        with open(test_path, 'w') as f:
            f.write(test_content)
        print_success(f"Test file created: {test_path}")
        return test_path
    except Exception as e:
        print_error(f"Failed to create test file: {e}")
        return None

def run_verification_tests():
    """Run verification tests to ensure everything works."""
    print_step(5, "Running Verification Tests")
    
    try:
        # Test 1: Check if metadata validator script exists
        validator_script = Path.cwd() / "metadata_validator" / "metadata_validator.py"
        if not validator_script.exists():
            print_error("Metadata validator script not found")
            return False
        
        print_success("Metadata validator script found")
        
        # Test 2: Run help command
        result = subprocess.run([
            sys.executable, str(validator_script), "--help"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print_success("Metadata validator help command works")
        else:
            print_error("Metadata validator help command failed")
            return False
        
        # Test 3: Run date format test
        test_script = Path.cwd() / "metadata_validator" / "tests" / "test_extended_date_formats.py"
        if test_script.exists():
            result = subprocess.run([
                sys.executable, str(test_script)
            ], capture_output=True, text=True, timeout=30)
            
            if "SUCCESS: YYYY.MM.DD format is now properly supported!" in result.stdout:
                print_success("Date format tests passed")
            else:
                print_error("Date format tests failed")
                return False
        else:
            print_info("Date format test script not found (skipping)")
        
        # Test 4: Test agent helper
        helper_script = Path.cwd() / "agent_metadata_helper.py"
        if helper_script.exists():
            result = subprocess.run([
                sys.executable, str(helper_script)
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print_success("Agent helper script works")
            else:
                print_error("Agent helper script failed")
                return False
        
        return True
        
    except subprocess.TimeoutExpired:
        print_error("Test timeout - some tests may have failed")
        return False
    except Exception as e:
        print_error(f"Verification failed: {e}")
        return False

def create_vscode_integration():
    """Create VS Code integration files."""
    print_step(6, "Setting Up VS Code Integration")
    
    vscode_dir = Path.cwd() / ".vscode"
    vscode_dir.mkdir(exist_ok=True)
    
    # Create settings.json
    settings_content = '''{
    "python.analysis.extraPaths": ["./metadata_validator"],
    "files.associations": {
        "*.md": "markdown"
    },
    "markdown.validate.enabled": true
}'''
    
    settings_path = vscode_dir / "settings.json"
    try:
        with open(settings_path, 'w') as f:
            f.write(settings_content)
        print_success("VS Code settings created")
    except Exception as e:
        print_error(f"Failed to create VS Code settings: {e}")
    
    # Create tasks.json
    tasks_content = '''{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Validate Metadata",
            "type": "shell",
            "command": "python",
            "args": ["metadata_validator/metadata_validator.py", "${file}", "--manual"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            },
            "problemMatcher": []
        }
    ]
}'''
    
    tasks_path = vscode_dir / "tasks.json"
    try:
        with open(tasks_path, 'w') as f:
            f.write(tasks_content)
        print_success("VS Code tasks created")
    except Exception as e:
        print_error(f"Failed to create VS Code tasks: {e}")

def create_usage_examples():
    """Create usage example files."""
    print_step(7, "Creating Usage Examples")
    
    examples_dir = Path.cwd() / "metadata_examples"
    examples_dir.mkdir(exist_ok=True)
    
    # Create basic usage example
    basic_example = '''#!/usr/bin/env python3
"""
Basic Usage Example

This example shows how to use the metadata validator in your agent code.
"""

from agent_metadata_helper import setup_metadata_validator, validate_file_metadata, normalize_date

# Setup the metadata validator
setup_metadata_validator()

# Example 1: Validate a single file
success, output, error = validate_file_metadata("test_document.md")
if success:
    print("✅ Metadata is valid")
else:
    print(f"❌ Metadata issues: {error}")

# Example 2: Normalize dates
dates = ["7/5/25", "2025.07.05", "Jul 5, 2025"]
for date in dates:
    normalized, changed, format_type = normalize_date(date)
    print(f"{date} → {normalized} ({format_type})")

# Example 3: Batch processing
import glob
files = glob.glob("**/*.md", recursive=True)
for file in files:
    success, output, error = validate_file_metadata(file)
    if not success:
        print(f"❌ {file}: {error}")
'''
    
    basic_path = examples_dir / "basic_usage.py"
    try:
        with open(basic_path, 'w') as f:
            f.write(basic_example)
        print_success("Basic usage example created")
    except Exception as e:
        print_error(f"Failed to create basic example: {e}")
    
    # Create advanced usage example
    advanced_example = '''#!/usr/bin/env python3
"""
Advanced Usage Example

This example shows advanced features like caching and batch processing.
"""

import glob
import json
import hashlib
from pathlib import Path
from agent_metadata_helper import setup_metadata_validator, validate_file_metadata

# Setup
setup_metadata_validator()

def get_file_hash(file_path):
    """Get MD5 hash of file content for caching."""
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def validate_with_cache(file_path, cache_file="metadata_cache.json"):
    """Validate file with caching for performance."""
    file_hash = get_file_hash(file_path)
    
    # Load cache
    try:
        with open(cache_file, 'r') as f:
            cache = json.load(f)
    except FileNotFoundError:
        cache = {}
    
    # Check cache
    if file_hash in cache:
        print(f"📋 Using cached result for {file_path}")
        return cache[file_hash]
    
    # Validate and cache
    result = validate_file_metadata(file_path)
    cache[file_hash] = result
    
    # Save cache
    with open(cache_file, 'w') as f:
        json.dump(cache, f, indent=2)
    
    return result

# Example: Batch processing with caching
files = glob.glob("**/*.md", recursive=True)
results = []

for file in files:
    success, output, error = validate_with_cache(file)
    results.append((file, success, error))

# Summary
valid_files = sum(1 for _, success, _ in results if success)
print(f"📊 Results: {valid_files}/{len(files)} files have valid metadata")

# Show issues
for file, success, error in results:
    if not success:
        print(f"❌ {file}: {error}")
'''
    
    advanced_path = examples_dir / "advanced_usage.py"
    try:
        with open(advanced_path, 'w') as f:
            f.write(advanced_example)
        print_success("Advanced usage example created")
    except Exception as e:
        print_error(f"Failed to create advanced example: {e}")

def print_final_summary():
    """Print final setup summary."""
    print_step(8, "Integration Complete!")
    
    print("🎉 Metadata Validator Integration Successful!")
    print("\n📁 Files Created:")
    print("  ✅ metadata_validator/ - Main package")
    print("  ✅ agent_metadata_helper.py - Agent integration helper")
    print("  ✅ test_document.md - Test file")
    print("  ✅ .vscode/ - VS Code integration")
    print("  ✅ metadata_examples/ - Usage examples")
    
    print("\n🚀 Quick Start:")
    print("  1. Test validation: python metadata_validator/metadata_validator.py test_document.md --manual")
    print("  2. Test agent helper: python agent_metadata_helper.py")
    print("  3. Run examples: python metadata_examples/basic_usage.py")
    
    print("\n📚 Documentation:")
    print("  📖 metadata_validator/README.md - Complete documentation")
    print("  📖 metadata_validator/docs/ - Detailed guides")
    print("  📖 metadata_examples/ - Code examples")
    
    print("\n🤖 Agent Integration:")
    print("  from agent_metadata_helper import setup_metadata_validator, validate_file_metadata")
    print("  setup_metadata_validator()")
    print("  success, output, error = validate_file_metadata('file.md')")
    
    print("\n✨ Your agents can now validate metadata with minimal setup!")

def main():
    """Main setup function."""
    print("🚀 Metadata Validator Workspace Integration")
    print("=" * 60)
    print("This script will set up the metadata validator in your workspace")
    print("and create all necessary files for agent integration.")
    print("=" * 60)
    
    # Check if user wants to proceed
    response = input("\nDo you want to proceed with the setup? (Y/n): ").strip().lower()
    if response in ['n', 'no']:
        print("Setup cancelled.")
        return
    
    # Run setup steps
    if not check_python_version():
        return
    
    metadata_dir = setup_metadata_validator()
    if not metadata_dir:
        return
    
    helper_path = create_agent_helper()
    if not helper_path:
        return
    
    test_path = create_test_file()
    if not test_path:
        return
    
    if not run_verification_tests():
        print_error("Verification tests failed. Setup may be incomplete.")
        return
    
    create_vscode_integration()
    create_usage_examples()
    print_final_summary()

if __name__ == "__main__":
    main() 