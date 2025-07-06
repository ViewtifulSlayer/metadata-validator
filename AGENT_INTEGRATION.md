# 🚀 Metadata Validator - Agent Integration Guide

## **Get Started in 2 Minutes**

### **1. Copy & Run (1 minute)**
```bash
# Copy the setup script to your workspace
cp /path/to/metadata_validator/setup_integration.py ./

# Run automated setup
python setup_integration.py
```

### **2. Use in Your Code (1 minute)**
```python
# In your agent/script
from agent_metadata_helper import setup_metadata_validator, validate_file_metadata

# Setup (run once)
setup_metadata_validator()

# Validate any markdown file
success, output, error = validate_file_metadata("document.md")
```

---

## **🎯 What You Get**

- ✅ **Zero dependencies** (Python standard library only)
- ✅ **36 date formats** supported (MM/DD/YYYY, DD/MM/YYYY, YYYY.MM.DD, etc.)
- ✅ **100% test success rate** (Phoenix adversarial tested)
- ✅ **Agent-ready** integration functions
- ✅ **VS Code integration** (tasks & settings)
- ✅ **Usage examples** included

---

## **📋 Quick Examples**

### **Validate a File**
```python
success, output, error = validate_file_metadata("document.md")
if success:
    print("✅ Metadata is valid")
else:
    print(f"❌ Issues: {error}")
```

### **Normalize Dates**
```python
from agent_metadata_helper import normalize_date

dates = ["7/5/25", "2025.07.05", "Jul 5, 2025"]
for date in dates:
    normalized, changed, format_type = normalize_date(date)
    print(f"{date} → {normalized}")
```

### **Batch Process**
```python
import glob
files = glob.glob("**/*.md", recursive=True)
for file in files:
    success, output, error = validate_file_metadata(file)
    if not success:
        print(f"❌ {file}: {error}")
```

---

## **🧪 Quick Test**

```bash
# Test the integration
python metadata_validator/metadata_validator.py test_document.md --manual

# Test agent helper
python agent_metadata_helper.py
```

---

## **🔧 What `setup_integration.py` Does Automatically**

The setup script performs these steps automatically:

### **Step 1: Environment Check**
- ✅ Verifies Python version (3.7+ required)
- ✅ Checks workspace permissions
- ✅ Validates system compatibility

### **Step 2: Package Setup**
- ✅ Copies metadata validator to your workspace
- ✅ Creates `metadata_validator/` directory
- ✅ Handles existing installations (with overwrite option)

### **Step 3: Agent Helper Creation**
- ✅ Generates `agent_metadata_helper.py` with integration functions
- ✅ Includes all necessary import statements
- ✅ Provides ready-to-use validation functions

### **Step 4: VS Code Integration**
- ✅ Creates `.vscode/settings.json` with metadata validator settings
- ✅ Configures automatic validation on save
- ✅ Sets up task configurations

### **Step 5: Test Files**
- ✅ Creates sample markdown files for testing
- ✅ Generates validation examples
- ✅ Provides verification scripts

### **Step 6: Verification**
- ✅ Runs automated tests to ensure everything works
- ✅ Validates date normalization functions
- ✅ Tests file validation capabilities

---

## **📋 Troubleshooting**

### **Common Issues:**

**"Python 3.7+ required"**
```bash
# Check your Python version
python --version

# If using Python 3.6 or earlier, upgrade Python
```

**"Permission denied"**
```bash
# Run with administrator privileges (Windows)
# Or use sudo (Linux/Mac)
sudo python setup_integration.py
```

**"Metadata validator not found"**
```bash
# Ensure you're in the correct workspace directory
# Check that setup_integration.py copied successfully
ls -la metadata_validator/
```

### **Manual Setup (if automation fails):**
```bash
# 1. Copy the package manually
cp -r /path/to/metadata_validator ./

# 2. Create agent helper manually
python metadata_validator/setup_integration.py --manual

# 3. Test manually
python agent_metadata_helper.py
```

---

## **📚 Full Documentation**

- 📖 `README.md` - Complete package documentation and features
- 📖 `QUICKSTART.md` - End-user quick start guide
- 📖 `docs/testing_plan.md` - Comprehensive testing framework
- 📖 `docs/phoenix_report.md` - Adversarial testing results
- 📖 `docs/sphinx_report.md` - Cognitive pattern analysis
- 📖 `CHANGELOG.md` - Version history and changes

### **Advanced Integration:**
- 📖 `docs/workspace_integration_guide.md` - Detailed integration guide
- 📖 `docs/date_format_support.md` - Date format documentation
- 📖 `config/metadata_standards.json` - Configurable validation rules

---

**That's it! Your agents can now validate metadata with minimal setup.** 🎉 