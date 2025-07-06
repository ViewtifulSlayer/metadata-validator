"""
Test suite for changelog validation functionality.
Tests version extraction, consistency checking, and suggestion generation.
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch, mock_open
from datetime import datetime

# Add the parent directory to the path to import metadata_validator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metadata_validator import (
    find_changelog_file,
    extract_changelog_section_from_file,
    determine_changelog_preference,
    extract_latest_version_from_changelog,
    check_changelog_consistency,
    suggest_changelog_entry,
    suggest_changelog_placement
)


class TestChangelogValidation(unittest.TestCase):
    """Test cases for changelog validation functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.today = "2025-07-05"

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_find_changelog_file_exact_match(self):
        """Test finding CHANGELOG.md file."""
        changelog_path = os.path.join(self.temp_dir, "CHANGELOG.md")
        with open(changelog_path, 'w') as f:
            f.write("# Changelog\n")
        
        found_path = find_changelog_file(self.temp_dir)
        self.assertEqual(found_path, changelog_path)

    def test_find_changelog_file_case_variations(self):
        """Test finding changelog files with different case variations."""
        # Create a fresh temp directory for this test to avoid interference
        test_dir = tempfile.mkdtemp()
        try:
            # Test that CHANGELOG.md takes precedence over changelog.md
            changelog_lower_path = os.path.join(test_dir, "changelog.md")
            changelog_upper_path = os.path.join(test_dir, "CHANGELOG.md")
            
            # Create both files
            with open(changelog_lower_path, 'w') as f:
                f.write("# Changelog Lower\n")
            with open(changelog_upper_path, 'w') as f:
                f.write("# Changelog Upper\n")
            
            # The function should find CHANGELOG.md first (it's first in the search list)
            found_path = find_changelog_file(test_dir)
            self.assertEqual(found_path, changelog_upper_path)
        finally:
            import shutil
            shutil.rmtree(test_dir)

    def test_find_changelog_file_not_found(self):
        """Test when no changelog file exists."""
        found_path = find_changelog_file(self.temp_dir)
        self.assertIsNone(found_path)

    def test_extract_latest_version_standard_format(self):
        """Test extracting version from standard Keep a Changelog format."""
        changelog_content = """# Changelog

## [1.0.0] - 2025-07-05

### Added
- Initial release

## [0.9.0] - 2025-07-01

### Added
- Beta features
"""
        
        with patch('builtins.open', mock_open(read_data=changelog_content)):
            version = extract_latest_version_from_changelog("fake_path.md")
            self.assertEqual(version, "1.0.0")

    def test_extract_latest_version_bracket_format(self):
        """Test extracting version from bracket format."""
        changelog_content = """# Changelog

[1.0.0] - 2025-07-05

### Added
- Initial release

[0.9.0] - 2025-07-01

### Added
- Beta features
"""
        
        with patch('builtins.open', mock_open(read_data=changelog_content)):
            version = extract_latest_version_from_changelog("fake_path.md")
            self.assertEqual(version, "1.0.0")

    def test_extract_latest_version_no_brackets(self):
        """Test extracting version from format without brackets."""
        changelog_content = """# Changelog

## 1.0.0 - 2025-07-05

### Added
- Initial release

## 0.9.0 - 2025-07-01

### Added
- Beta features
"""
        
        with patch('builtins.open', mock_open(read_data=changelog_content)):
            version = extract_latest_version_from_changelog("fake_path.md")
            self.assertEqual(version, "1.0.0")

    def test_extract_latest_version_no_versions(self):
        """Test when no versions are found in changelog."""
        changelog_content = """# Changelog

This is a changelog without version numbers.

### Added
- Some features
"""
        
        with patch('builtins.open', mock_open(read_data=changelog_content)):
            version = extract_latest_version_from_changelog("fake_path.md")
            self.assertIsNone(version)

    def test_extract_changelog_section_from_file(self):
        """Test extracting changelog section from markdown file."""
        file_content = """# My Document

Some content here.

## Changelog

## [1.0.0] - 2025-07-05

### Added
- Initial release

## [0.9.0] - 2025-07-01

### Added
- Beta features

## Another Section

More content.
"""
        
        with patch('builtins.open', mock_open(read_data=file_content)):
            changelog_section = extract_changelog_section_from_file("fake_file.md")
            self.assertIsNotNone(changelog_section)
            if changelog_section:
                self.assertIn("## [1.0.0] - 2025-07-05", changelog_section)
                self.assertIn("## [0.9.0] - 2025-07-01", changelog_section)

    def test_determine_changelog_preference_package_file(self):
        """Test preference determination for package files."""
        with patch('metadata_validator.find_changelog_file', return_value=None):
            with patch('metadata_validator.extract_changelog_section_from_file', return_value=None):
                preference = determine_changelog_preference("__init__.py", self.temp_dir)
                self.assertEqual(preference, "separate")

    def test_determine_changelog_preference_readme_with_separate(self):
        """Test preference determination for README with separate changelog."""
        # Mock the functions to return the expected values
        with patch('metadata_validator.metadata_validator.find_changelog_file', return_value="/fake/CHANGELOG.md"):
            with patch('metadata_validator.metadata_validator.extract_changelog_section_from_file', return_value=None):
                preference = determine_changelog_preference("README.md", self.temp_dir)
                self.assertEqual(preference, "separate")

    def test_determine_changelog_preference_readme_with_embedded(self):
        """Test preference determination for README with embedded changelog."""
        # Mock the functions to return the expected values
        with patch('metadata_validator.metadata_validator.find_changelog_file', return_value=None):
            with patch('metadata_validator.metadata_validator.extract_changelog_section_from_file', return_value="## [1.0.0]"):
                preference = determine_changelog_preference("README.md", self.temp_dir)
                self.assertEqual(preference, "embedded")

    def test_check_changelog_consistency_separate_match(self):
        """Test when metadata version matches separate changelog version."""
        changelog_content = """# Changelog

## [1.0.0] - 2025-07-05

### Added
- Initial release
"""
        
        with patch('builtins.open', mock_open(read_data=changelog_content)):
            changelog_path = os.path.join(self.temp_dir, "CHANGELOG.md")
            with patch('metadata_validator.find_changelog_file', return_value=changelog_path):
                with patch('metadata_validator.extract_latest_version_from_changelog', return_value="1.0.0"):
                    with patch('metadata_validator.determine_changelog_preference', return_value="separate"):
                        with patch('metadata_validator.extract_changelog_section_from_file', return_value=None):
                            result = check_changelog_consistency("1.0.0", "fake_file.md", self.temp_dir)
                            self.assertTrue(result)

    def test_check_changelog_consistency_embedded_match(self):
        """Test when metadata version matches embedded changelog version."""
        changelog_content = """## [1.0.0] - 2025-07-05

### Added
- Initial release
"""
        
        with patch('metadata_validator.find_changelog_file', return_value=None):
            with patch('metadata_validator.extract_changelog_section_from_file', return_value=changelog_content):
                with patch('metadata_validator.determine_changelog_preference', return_value="embedded"):
                    with patch('metadata_validator.extract_latest_version_from_changelog', return_value="1.0.0"):
                        result = check_changelog_consistency("1.0.0", "fake_file.md", self.temp_dir)
                        self.assertTrue(result)

    def test_check_changelog_consistency_no_changelog(self):
        """Test when no changelog exists."""
        with patch('metadata_validator.find_changelog_file', return_value=None):
            with patch('metadata_validator.extract_changelog_section_from_file', return_value=None):
                with patch('metadata_validator.determine_changelog_preference', return_value="both"):
                    result = check_changelog_consistency("1.0.0", "fake_file.md", self.temp_dir)
                    self.assertTrue(result)

    @patch('metadata_validator.metadata_validator.datetime')
    def test_suggest_changelog_entry_patch(self, mock_datetime):
        """Test generating patch changelog entry."""
        mock_datetime.now.return_value.strftime.return_value = self.today
        entry = suggest_changelog_entry("1.0.1", "patch")
        self.assertIn("## [1.0.1] - 2025-07-05", entry)

    @patch('metadata_validator.metadata_validator.datetime')
    def test_suggest_changelog_entry_minor(self, mock_datetime):
        """Test generating minor changelog entry."""
        mock_datetime.now.return_value.strftime.return_value = self.today
        entry = suggest_changelog_entry("1.1.0", "minor")
        self.assertIn("## [1.1.0] - 2025-07-05", entry)

    @patch('metadata_validator.metadata_validator.datetime')
    def test_suggest_changelog_entry_major(self, mock_datetime):
        """Test generating major changelog entry."""
        mock_datetime.now.return_value.strftime.return_value = self.today
        entry = suggest_changelog_entry("2.0.0", "major")
        self.assertIn("## [2.0.0] - 2025-07-05", entry)

    @patch('metadata_validator.metadata_validator.datetime')
    def test_suggest_changelog_entry_default(self, mock_datetime):
        """Test generating default (patch) changelog entry."""
        mock_datetime.now.return_value.strftime.return_value = self.today
        entry = suggest_changelog_entry("1.0.1")
        self.assertIn("## [1.0.1] - 2025-07-05", entry)

    def test_suggest_changelog_placement_readme(self):
        """Test changelog placement suggestion for README files."""
        placement = suggest_changelog_placement("README.md", "readme")
        self.assertIn("position", placement)
        self.assertIn("heading_level", placement)
        self.assertIn("example", placement)

    def test_suggest_changelog_placement_documentation(self):
        """Test changelog placement suggestion for documentation files."""
        placement = suggest_changelog_placement("docs/api.md", "documentation")
        self.assertIn("position", placement)
        self.assertIn("heading_level", placement)
        self.assertIn("example", placement)

    def test_suggest_changelog_placement_configuration(self):
        """Test changelog placement suggestion for configuration files."""
        placement = suggest_changelog_placement("config.md", "configuration")
        self.assertIn("position", placement)
        self.assertIn("heading_level", placement)
        self.assertIn("example", placement)

    def test_extract_changelog_section_alternative_headings(self):
        """Test extracting changelog section with alternative headings."""
        file_content = """# My Document

Some content here.

## History

## [1.0.0] - 2025-07-05

### Added
- Initial release

## Another Section

More content.
"""
        
        with patch('builtins.open', mock_open(read_data=file_content)):
            changelog_section = extract_changelog_section_from_file("fake_file.md")
            self.assertIsNotNone(changelog_section)
            if changelog_section:
                self.assertIn("## [1.0.0] - 2025-07-05", changelog_section)


if __name__ == '__main__':
    unittest.main() 