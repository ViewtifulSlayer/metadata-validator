"""
Configuration loader for metadata validator.

This module provides robust configuration loading with fallback mechanisms
and validation, following industry best practices for configuration management.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ConfigLoader:
    """
    Robust configuration loader with fallback mechanisms and validation.
    
    This class follows the patterns found in the codebase for configuration management,
    providing a reliable way to load and validate configuration settings.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration loader.
        
        Args:
            config_path: Optional path to configuration file. If None, uses default location.
        """
        if config_path is None:
            # Default to config file in the same directory as this module
            self.config_path = Path(__file__).parent / "metadata_standards.json"
        else:
            self.config_path = Path(config_path)
        
        self._config = None
        self._load_config()
    
    def _load_config(self) -> None:
        """
        Load configuration from file with fallback to defaults.
        
        This method implements the same pattern used in other parts of the codebase:
        - Try to load from file
        - Fall back to defaults if file not found
        - Log any issues for debugging
        """
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_path}")
            else:
                logger.warning(f"Configuration file not found at {self.config_path}, using defaults")
                self._config = self._get_default_config()
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            self._config = self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self._config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration as fallback.
        
        This provides the same values that were previously hardcoded,
        ensuring backward compatibility.
        """
        return {
            "metadata": {
                "version": "1.0.0",
                "description": "Default configuration for metadata validation standards",
                "last_updated": "2025-07-05",
                "author": "proto_sphinx-0.2.0"
            },
            "required_fields": [
                "Document Title",
                "Author",
                "Created",
                "Last Updated",
                "Version",
                "Description"
            ],
            "date_format": {
                "pattern": "\\d{4}-\\d{2}-\\d{2}",
                "iso_format": "YYYY-MM-DD",
                "current_date": "2025-07-05",
                "description": "ISO 8601 date format for all date fields"
            },
            "defaults": {
                "Document Title": "Unknown",
                "Author": "Unknown",
                "Created": None,
                "Last Updated": None,
                "Version": "0.1.0",
                "Description": "No description provided."
            },
            "date_patterns": {
                "description": "Patterns for date format normalization",
                "patterns": [
                    {
                        "name": "MM/DD/YYYY",
                        "regex": "(\\d{1,2})/(\\d{1,2})/(\\d{4})",
                        "formatter": "YYYY-MM-DD",
                        "description": "US date format with slashes"
                    },
                    {
                        "name": "MM/DD/YY",
                        "regex": "(\\d{1,2})/(\\d{1,2})/(\\d{2})",
                        "formatter": "20YY-MM-DD",
                        "description": "US date format with 2-digit year"
                    },
                    {
                        "name": "DD/MM/YYYY",
                        "regex": "(\\d{1,2})/(\\d{1,2})/(\\d{4})",
                        "formatter": "YYYY-DD-MM",
                        "description": "European date format with slashes"
                    },
                    {
                        "name": "DD/MM/YY",
                        "regex": "(\\d{1,2})/(\\d{1,2})/(\\d{2})",
                        "formatter": "20YY-DD-MM",
                        "description": "European date format with 2-digit year"
                    },
                    {
                        "name": "MM-DD-YYYY",
                        "regex": "(\\d{1,2})-(\\d{1,2})-(\\d{4})",
                        "formatter": "YYYY-MM-DD",
                        "description": "US date format with dashes"
                    },
                    {
                        "name": "DD-MM-YYYY",
                        "regex": "(\\d{1,2})-(\\d{1,2})-(\\d{4})",
                        "formatter": "YYYY-DD-MM",
                        "description": "European date format with dashes"
                    },
                    {
                        "name": "YYYY/MM/DD",
                        "regex": "(\\d{4})/(\\d{1,2})/(\\d{1,2})",
                        "formatter": "YYYY-MM-DD",
                        "description": "ISO-like format with slashes"
                    },
                    {
                        "name": "YYYY.MM.DD",
                        "regex": "(\\d{4})\\.(\\d{1,2})\\.(\\d{1,2})",
                        "formatter": "YYYY-MM-DD",
                        "description": "ISO-like format with dots"
                    },
                    {
                        "name": "YYYYMMDD",
                        "regex": "(\\d{4})(\\d{2})(\\d{2})",
                        "formatter": "YYYY-MM-DD",
                        "description": "Compact format without separators"
                    },
                    {
                        "name": "Month Name YYYY",
                        "regex": "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\s+(\\d{1,2}),?\\s+(\\d{4})",
                        "formatter": "YYYY-MM-DD",
                        "description": "US format with abbreviated month names"
                    },
                    {
                        "name": "Full Month YYYY",
                        "regex": "(January|February|March|April|May|June|July|August|September|October|November|December)\\s+(\\d{1,2}),?\\s+(\\d{4})",
                        "formatter": "YYYY-MM-DD",
                        "description": "US format with full month names"
                    }
                ]
            },
            "timeout_config": {
                "description": "Timeout settings for user interaction",
                "initial_timeout": None,
                "gentle_prompt_delay": None,
                "final_timeout": None,
                "note": "Set to null to disable timeouts"
            },
            "validation": {
                "description": "Validation behavior settings",
                "auto_update_last_updated": True,
                "confirm_ambiguous_dates": True,
                "strict_mode": False,
                "allow_empty_values": False
            },
            "user_experience": {
                "description": "User experience and accessibility settings",
                "interactive_mode": True,
                "auto_mode": False,
                "gentle_prompts": True,
                "clear_error_messages": True,
                "color_output": True
            },
            "extensibility": {
                "description": "Settings for future extensibility",
                "custom_field_validators": {},
                "custom_date_patterns": [],
                "plugin_support": False
            }
        }
    
    def get_required_fields(self) -> List[str]:
        """Get list of required metadata fields."""
        if self._config is None:
            return []
        return self._config.get("required_fields", [])
    
    def get_date_pattern(self) -> str:
        """Get the ISO date pattern for validation."""
        if self._config is None:
            return "\\d{4}-\\d{2}-\\d{2}"
        return self._config.get("date_format", {}).get("pattern", "\\d{4}-\\d{2}-\\d{2}")
    
    def get_defaults(self) -> Dict[str, Any]:
        """Get default values for metadata fields."""
        if self._config is None:
            return {}
        return self._config.get("defaults", {})
    
    def get_date_patterns(self) -> List[Dict[str, str]]:
        """Get date format patterns for normalization."""
        if self._config is None:
            return []
        return self._config.get("date_patterns", {}).get("patterns", [])
    
    def get_timeout_config(self) -> Dict[str, Any]:
        """Get timeout configuration settings."""
        if self._config is None:
            return {}
        return self._config.get("timeout_config", {})
    
    def get_validation_config(self) -> Dict[str, Any]:
        """Get validation behavior settings."""
        if self._config is None:
            return {}
        return self._config.get("validation", {})
    
    def get_user_experience_config(self) -> Dict[str, Any]:
        """Get user experience settings."""
        if self._config is None:
            return {}
        return self._config.get("user_experience", {})
    
    def get_config(self) -> Dict[str, Any]:
        """Get the complete configuration dictionary."""
        if self._config is None:
            return {}
        return self._config.copy()
    
    def reload_config(self) -> None:
        """Reload configuration from file."""
        self._load_config()
    
    def validate_config(self) -> List[str]:
        """
        Validate configuration structure and return any issues.
        
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        if self._config is None:
            errors.append("Configuration is not loaded")
            return errors
        
        # Check required sections
        required_sections = ["required_fields", "date_format", "defaults"]
        for section in required_sections:
            if section not in self._config:
                errors.append(f"Missing required configuration section: {section}")
        
        # Check required fields is a list
        if "required_fields" in self._config and not isinstance(self._config["required_fields"], list):
            errors.append("required_fields must be a list")
        
        # Check date format has pattern
        date_format = self._config.get("date_format", {})
        if "pattern" not in date_format:
            errors.append("date_format must contain a pattern")
        
        return errors


# Global configuration instance for easy access
_config_loader = None


def get_config_loader() -> ConfigLoader:
    """
    Get the global configuration loader instance.
    
    This follows the singleton pattern used in other parts of the codebase
    for shared resources.
    """
    global _config_loader
    if _config_loader is None:
        _config_loader = ConfigLoader()
    return _config_loader


def reload_config() -> None:
    """Reload the global configuration."""
    global _config_loader
    if _config_loader is not None:
        _config_loader.reload_config()


# Convenience functions for backward compatibility
def get_required_fields() -> List[str]:
    """Get list of required metadata fields."""
    return get_config_loader().get_required_fields()


def get_date_pattern() -> str:
    """Get the ISO date pattern for validation."""
    return get_config_loader().get_date_pattern()


def get_defaults() -> Dict[str, Any]:
    """Get default values for metadata fields."""
    return get_config_loader().get_defaults()


def get_date_patterns() -> List[Dict[str, str]]:
    """Get date format patterns for normalization."""
    return get_config_loader().get_date_patterns()


def get_timeout_config() -> Dict[str, Any]:
    """Get timeout configuration settings."""
    return get_config_loader().get_timeout_config()


def get_validation_config() -> Dict[str, Any]:
    """Get validation behavior settings."""
    return get_config_loader().get_validation_config()


def get_user_experience_config() -> Dict[str, Any]:
    """Get user experience settings."""
    return get_config_loader().get_user_experience_config() 