"""
Metadata Validator Package

A comprehensive metadata validation and testing framework for markdown documentation files.
Includes Phoenix (adversarial testing) and Sphinx (cognitive pattern analysis) approaches.

Version: 1.1.0
Author: ViewtifulSlayer
"""

__version__ = "1.1.0"
__author__ = "ViewtifulSlayer"

# Import all public functions for easy access
from .metadata_validator import (
    # Core validation functions
    validate_metadata,
    normalize_date_format,
    extract_metadata_block,
    
    # Changelog functions
    find_changelog_file,
    extract_changelog_section_from_file,
    determine_changelog_preference,
    extract_latest_version_from_changelog,
    check_changelog_consistency,
    suggest_changelog_entry,
    suggest_changelog_placement,
    normalize_changelog_dates,
    validate_changelog_date_format,
    
    # Utility functions
    display_metadata,
    prettify_filename,
    
    # Main function
    main
)

__all__ = [
    'validate_metadata',
    'normalize_date_format', 
    'extract_metadata_block',
    'find_changelog_file',
    'extract_changelog_section_from_file',
    'determine_changelog_preference',
    'extract_latest_version_from_changelog',
    'check_changelog_consistency',
    'suggest_changelog_entry',
    'suggest_changelog_placement',
    'normalize_changelog_dates',
    'validate_changelog_date_format',
    'display_metadata',
    'prettify_filename',
    'main'
] 