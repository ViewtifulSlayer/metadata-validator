#!/usr/bin/env python3
"""
Test script to verify date normalization logic
"""
import re
from datetime import datetime

def normalize_date_format(date_str):
    """
    Convert various date formats to YYYY-MM-DD.
    Returns (normalized_date, was_changed, original_format)
    """
    if not date_str:
        return None, False, None
    
    # Already in correct format
    ISO_DATE_PATTERN = r'\d{4}-\d{2}-\d{2}'
    if re.fullmatch(ISO_DATE_PATTERN, date_str):
        return date_str, False, 'YYYY-MM-DD'
    
    # Common date format patterns
    patterns = [
        # MM/DD/YYYY
        (r'(\d{1,2})/(\d{1,2})/(\d{4})', lambda m: f"{m.group(3)}-{m.group(1).zfill(2)}-{m.group(2).zfill(2)}"),
        # MM/DD/YY (2-digit year)
        (r'(\d{1,2})/(\d{1,2})/(\d{2})', lambda m: f"20{m.group(3)}-{m.group(1).zfill(2)}-{m.group(2).zfill(2)}"),
        # DD/MM/YYYY
        (r'(\d{1,2})/(\d{1,2})/(\d{4})', lambda m: f"{m.group(3)}-{m.group(2).zfill(2)}-{m.group(1).zfill(2)}"),
        # DD/MM/YY (2-digit year)
        (r'(\d{1,2})/(\d{1,2})/(\d{2})', lambda m: f"20{m.group(3)}-{m.group(2).zfill(2)}-{m.group(1).zfill(2)}"),
        # MM-DD-YYYY
        (r'(\d{1,2})-(\d{1,2})-(\d{4})', lambda m: f"{m.group(3)}-{m.group(1).zfill(2)}-{m.group(2).zfill(2)}"),
        # MM-DD-YY (2-digit year)
        (r'(\d{1,2})-(\d{1,2})-(\d{2})', lambda m: f"20{m.group(3)}-{m.group(1).zfill(2)}-{m.group(2).zfill(2)}"),
        # DD-MM-YYYY
        (r'(\d{1,2})-(\d{1,2})-(\d{4})', lambda m: f"{m.group(3)}-{m.group(2).zfill(2)}-{m.group(1).zfill(2)}"),
        # DD-MM-YY (2-digit year)
        (r'(\d{1,2})-(\d{1,2})-(\d{2})', lambda m: f"20{m.group(3)}-{m.group(2).zfill(2)}-{m.group(1).zfill(2)}"),
        # YYYY/MM/DD
        (r'(\d{4})/(\d{1,2})/(\d{1,2})', lambda m: f"{m.group(1)}-{m.group(2).zfill(2)}-{m.group(3).zfill(2)}"),
        # MM.DD.YYYY
        (r'(\d{1,2})\.(\d{1,2})\.(\d{4})', lambda m: f"{m.group(3)}-{m.group(1).zfill(2)}-{m.group(2).zfill(2)}"),
        # MM.DD.YY (2-digit year)
        (r'(\d{1,2})\.(\d{1,2})\.(\d{2})', lambda m: f"20{m.group(3)}-{m.group(1).zfill(2)}-{m.group(2).zfill(2)}"),
        # DD.MM.YYYY
        (r'(\d{1,2})\.(\d{1,2})\.(\d{4})', lambda m: f"{m.group(3)}-{m.group(2).zfill(2)}-{m.group(1).zfill(2)}"),
        # DD.MM.YY (2-digit year)
        (r'(\d{1,2})\.(\d{1,2})\.(\d{2})', lambda m: f"20{m.group(3)}-{m.group(2).zfill(2)}-{m.group(1).zfill(2)}"),
    ]
    
    for pattern, formatter in patterns:
        match = re.fullmatch(pattern, date_str)
        if match:
            try:
                normalized = formatter(match)
                # Validate the normalized date
                datetime.strptime(normalized, '%Y-%m-%d')
                return normalized, True, pattern
            except ValueError:
                continue
    
    return date_str, False, 'unknown'

def test_date_normalization():
    """Test various date formats"""
    test_cases = [
        "7/5/25",      # Should convert to 2025-07-05
        "12/25/2024",  # Should convert to 2024-12-25
        "2025-07-05",  # Already correct format
        "invalid",     # Should not change
        "25/12/2024",  # DD/MM/YYYY format
        "07.05.2025",  # MM.DD.YYYY format
    ]
    
    print("Testing date normalization:")
    print("=" * 50)
    
    for test_date in test_cases:
        normalized, was_changed, original_format = normalize_date_format(test_date)
        status = "✅ CHANGED" if was_changed else "❌ NO CHANGE"
        print(f"Input: {test_date:12} -> {normalized:12} [{status}] (Format: {original_format})")

if __name__ == "__main__":
    test_date_normalization() 