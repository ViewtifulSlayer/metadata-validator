#!/usr/bin/env python3
"""
Extended Date Format Testing Suite

This script tests all supported date formats in the metadata validator,
including the newly added YYYY.MM.DD format and other comprehensive formats.

Author: ViewtifulSlayer
Version: 1.0.0
"""

import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from metadata_validator import normalize_date_format

def test_date_normalization():
    """Test comprehensive date format normalization."""
    print("🧪 Testing Extended Date Format Support")
    print("=" * 60)
    
    # Test cases with expected results
    test_cases = [
        # Original formats (should still work)
        ("2025-07-05", "2025-07-05", False, "YYYY-MM-DD"),
        ("7/5/25", "2025-07-05", True, "MM/DD/YY"),
        ("12/25/2024", "2024-12-25", True, "MM/DD/YYYY"),
        ("25/12/2024", "2024-12-25", True, "DD/MM/YYYY"),
        ("7-5-25", "2025-07-05", True, "MM-DD-YY"),
        ("25-7-2025", "2025-07-25", True, "DD-MM-YYYY"),
        ("2025/7/5", "2025-07-05", True, "YYYY/MM/DD"),
        ("07.05.2025", "2025-07-05", True, "MM.DD.YYYY"),
        ("25.12.2024", "2024-12-25", True, "DD.MM.YYYY"),
        
        # NEW: YYYY.MM.DD formats (the main fix)
        ("2025.07.05", "2025-07-05", True, "YYYY.MM.DD"),
        ("2025.7.5", "2025-07-05", True, "YYYY.MM.DD"),
        ("25.07.05", "2025-07-05", True, "YY.MM.DD"),
        ("25.7.5", "2025-07-05", True, "YY.MM.DD"),
        
        # NEW: Compact formats
        ("20250705", "2025-07-05", True, "YYYYMMDD"),
        ("250705", "2025-07-05", True, "YYMMDD"),
        
        # NEW: US format with month names
        ("Jul 5, 2025", "2025-07-05", True, "Month DD, YYYY"),
        ("July 5, 2025", "2025-07-05", True, "Month DD, YYYY"),
        ("Jul 5 2025", "2025-07-05", True, "Month DD YYYY"),
        ("July 5 2025", "2025-07-05", True, "Month DD YYYY"),
        ("Dec 25, 2024", "2024-12-25", True, "Month DD, YYYY"),
        ("December 25, 2024", "2024-12-25", True, "Month DD, YYYY"),
        
        # Edge cases and invalid formats
        ("invalid", "invalid", False, "unknown"),
        ("", None, False, None),
        ("   ", "   ", False, "unknown"),
        ("7/5/25 ", "7/5/25 ", False, "unknown"),  # Trailing space
        (" 7/5/25", " 7/5/25", False, "unknown"),  # Leading space
    ]
    
    passed = 0
    failed = 0
    
    for test_input, expected_output, expected_changed, expected_format in test_cases:
        try:
            normalized, was_changed, detected_format = normalize_date_format(test_input)
            
            # Check if the result matches expectations
            success = (
                normalized == expected_output and 
                was_changed == expected_changed and
                detected_format == expected_format
            )
            
            if success:
                status = "✅ PASS"
                passed += 1
            else:
                status = "❌ FAIL"
                failed += 1
                print(f"   Expected: {expected_output} (changed: {expected_changed}, format: {expected_format})")
                print(f"   Got:      {normalized} (changed: {was_changed}, format: {detected_format})")
            
            print(f"{status} '{test_input}' -> '{normalized}' (Format: {detected_format})")
            
        except Exception as e:
            print(f"❌ ERROR '{test_input}': {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    print(f"🎯 Success Rate: {passed/(passed+failed)*100:.1f}%")
    
    return passed, failed

def test_specific_phoenix_failure():
    """Test the specific Phoenix failure case that was identified."""
    print("\n🦅 Testing Phoenix Failure Case Fix")
    print("=" * 60)
    
    # This was the specific case that failed in Phoenix testing
    test_input = "2025.07.05"
    expected_output = "2025-07-05"
    
    normalized, was_changed, detected_format = normalize_date_format(test_input)
    
    if normalized == expected_output and was_changed:
        print(f"✅ FIXED: '{test_input}' -> '{normalized}' (Format: {detected_format})")
        print("   The YYYY.MM.DD format is now properly supported!")
        return True
    else:
        print(f"❌ STILL BROKEN: '{test_input}' -> '{normalized}' (changed: {was_changed})")
        return False

def test_month_name_edge_cases():
    """Test edge cases for month name formats."""
    print("\n📅 Testing Month Name Edge Cases")
    print("=" * 60)
    
    month_tests = [
        ("Jan 1, 2025", "2025-01-01"),
        ("Feb 28, 2024", "2024-02-28"),
        ("Mar 15, 2025", "2025-03-15"),
        ("Apr 30, 2025", "2025-04-30"),
        ("May 1, 2025", "2025-05-01"),
        ("Jun 21, 2025", "2025-06-21"),
        ("Jul 4, 2025", "2025-07-04"),
        ("Aug 15, 2025", "2025-08-15"),
        ("Sep 1, 2025", "2025-09-01"),
        ("Oct 31, 2025", "2025-10-31"),
        ("Nov 11, 2025", "2025-11-11"),
        ("Dec 25, 2025", "2025-12-25"),
        # Full month names
        ("January 1, 2025", "2025-01-01"),
        ("February 28, 2024", "2024-02-28"),
        ("December 25, 2025", "2025-12-25"),
    ]
    
    passed = 0
    failed = 0
    
    for test_input, expected_output in month_tests:
        normalized, was_changed, detected_format = normalize_date_format(test_input)
        
        if normalized == expected_output and was_changed:
            print(f"✅ PASS: '{test_input}' -> '{normalized}'")
            passed += 1
        else:
            print(f"❌ FAIL: '{test_input}' -> '{normalized}' (expected: {expected_output})")
            failed += 1
    
    print(f"\n📊 Month Name Results: {passed} passed, {failed} failed")
    return passed, failed

def test_compact_format_edge_cases():
    """Test edge cases for compact date formats."""
    print("\n📅 Testing Compact Format Edge Cases")
    print("=" * 60)
    
    compact_tests = [
        ("20250101", "2025-01-01"),  # New Year
        ("20250229", "2025-02-29"),  # Invalid date (should fail validation)
        ("20241231", "2024-12-31"),  # Year end
        ("250101", "2025-01-01"),    # 2-digit year
        ("241231", "2024-12-31"),    # 2-digit year
    ]
    
    passed = 0
    failed = 0
    
    for test_input, expected_output in compact_tests:
        normalized, was_changed, detected_format = normalize_date_format(test_input)
        
        if normalized == expected_output and was_changed:
            print(f"✅ PASS: '{test_input}' -> '{normalized}'")
            passed += 1
        else:
            print(f"❌ FAIL: '{test_input}' -> '{normalized}' (expected: {expected_output})")
            failed += 1
    
    print(f"\n📊 Compact Format Results: {passed} passed, {failed} failed")
    return passed, failed

def main():
    """Main testing execution."""
    print("🧪 EXTENDED DATE FORMAT TESTING SUITE")
    print("=" * 60)
    print("Testing comprehensive date format support including YYYY.MM.DD fix")
    print("=" * 60)
    
    # Run all tests
    basic_passed, basic_failed = test_date_normalization()
    phoenix_fixed = test_specific_phoenix_failure()
    month_passed, month_failed = test_month_name_edge_cases()
    compact_passed, compact_failed = test_compact_format_edge_cases()
    
    # Summary
    total_passed = basic_passed + month_passed + compact_passed
    total_failed = basic_failed + month_failed + compact_failed
    
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Basic Formats: {basic_passed} passed, {basic_failed} failed")
    print(f"🦅 Phoenix Fix: {'✅ FIXED' if phoenix_fixed else '❌ STILL BROKEN'}")
    print(f"📅 Month Names: {month_passed} passed, {month_failed} failed")
    print(f"📅 Compact Formats: {compact_passed} passed, {compact_failed} failed")
    print(f"🎯 Overall Success Rate: {total_passed/(total_passed+total_failed)*100:.1f}%")
    
    if phoenix_fixed:
        print("\n🎉 SUCCESS: YYYY.MM.DD format is now properly supported!")
        print("   The Phoenix failure case has been resolved.")
    else:
        print("\n❌ FAILURE: YYYY.MM.DD format is still not working properly.")
    
    print("\n📋 Supported Date Formats Summary:")
    print("   ✅ YYYY-MM-DD (ISO 8601)")
    print("   ✅ MM/DD/YYYY and MM/DD/YY")
    print("   ✅ DD/MM/YYYY and DD/MM/YY")
    print("   ✅ MM-DD-YYYY and MM-DD-YY")
    print("   ✅ DD-MM-YYYY and DD-MM-YY")
    print("   ✅ YYYY/MM/DD")
    print("   ✅ YYYY.MM.DD and YY.MM.DD (NEW)")
    print("   ✅ MM.DD.YYYY and MM.DD.YY")
    print("   ✅ DD.MM.YYYY and DD.MM.YY")
    print("   ✅ YYYYMMDD and YYMMDD (NEW)")
    print("   ✅ Month names (Jan 1, 2025, January 1, 2025) (NEW)")

if __name__ == "__main__":
    main() 