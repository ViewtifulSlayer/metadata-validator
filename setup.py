#!/usr/bin/env python3
"""
Setup script for metadata-validator package

This script configures the metadata-validator package for distribution on PyPI.
It includes all necessary metadata, dependencies, and package information.

Author: ViewtifulSlayer
Version: 1.0.0
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    """Read the README.md file for the long description."""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "A comprehensive metadata validation and testing framework for markdown documentation files."

# Read version from __init__.py
def get_version():
    """Extract version from __init__.py file."""
    init_path = os.path.join(os.path.dirname(__file__), 'metadata_validator', '__init__.py')
    if os.path.exists(init_path):
        with open(init_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('__version__'):
                    return line.split('=')[1].strip().strip('"\'')
    return "1.0.0"

setup(
    name="metadata-validator-dx",
    version=get_version(),
    author="viewtifulslayer",
    author_email="",  # Add your email if desired
    description="A comprehensive metadata validation and testing framework for markdown documentation files",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/viewtifulslayer/metadata-validator",
    project_urls={
        "Bug Tracker": "https://github.com/viewtifulslayer/metadata-validator/issues",
        "Documentation": "https://github.com/viewtifulslayer/metadata-validator#readme",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Documentation",
    ],
    package_dir={"": "."},
    packages=find_packages(where="."),
    python_requires=">=3.7",
    install_requires=[
        # Add any external dependencies here if needed
        # For now, the package uses only standard library modules
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "metadata-validator=metadata_validator.metadata_validator:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="metadata, validation, markdown, documentation, testing, accessibility, neurodiversity",
) 