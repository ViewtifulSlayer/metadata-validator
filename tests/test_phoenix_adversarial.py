#!/usr/bin/env python3
"""
Phoenix Adversarial Testing Suite for Metadata Validator

This script embodies the Phoenix seat's mission: "From the ashes of failure, we rise with renewed wisdom and strength."
It systematically attempts to break the metadata validator through adversarial testing, edge cases, and malformed inputs.

Author: Phoenix Seat (proto_phoenix-0.1.1)
Version: 1.0.0
"""

import os
import sys
import subprocess
import tempfile
import time
import shutil
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from metadata_validator import normalize_date_format

class PhoenixAdversarialTester:
    """Phoenix seat adversarial testing framework."""
    
    def __init__(self):
        self.validator_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'metadata_validator.py')
        self.test_results = []
        self.failures = []
        self.successes = []
        self.start_time = time.time()
        
    def log_result(self, test_name, success, details, error=None):
        """Log test results for Phoenix analysis."""
        result = {
            'test_name': test_name,
            'success': success,
            'details': details,
            'error': str(error) if error else None,
            'timestamp': datetime.now().isoformat()
        }
        
        if success:
            self.successes.append(result)
        else:
            self.failures.append(result)
        
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        if error:
            print(f"   Error: {error}")
    
    def run_validator(self, test_file, mode="", timeout=10):
        """Run the metadata validator with given parameters."""
        try:
            cmd = [sys.executable, self.validator_path, test_file]
            if mode:
                cmd.append(mode)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.path.dirname(self.validator_path)
            )
            
            return {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {
                'returncode': -1,
                'stdout': '',
                'stderr': 'Timeout expired',
                'success': False
            }
        except Exception as e:
            return {
                'returncode': -1,
                'stdout': '',
                'stderr': str(e),
                'success': False
            }
    
    def create_test_file(self, content, filename="test_file.md"):
        """Create a temporary test file with given content."""
        test_dir = os.path.join(os.path.dirname(__file__), 'test_files', 'edge_cases')
        os.makedirs(test_dir, exist_ok=True)
        
        filepath = os.path.join(test_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def test_date_normalization_edge_cases(self):
        """Test date normalization with edge cases."""
        print("\n🦅 PHOENIX: Testing Date Normalization Edge Cases")
        print("=" * 60)
        
        edge_cases = [
            ("7/5/25", "MM/DD/YY format"),
            ("25/12/2024", "DD/MM/YYYY format"),
            ("2025/7/5", "YYYY/M/D format"),
            ("7-5-25", "MM-DD-YY format"),
            ("25-7-2025", "DD-M-YYYY format"),
            ("2025.07.05", "YYYY.MM.DD format"),
            ("5 July 2025", "Text format"),
            ("20250705", "Compact format"),
            ("7/5/2025", "Inconsistent year format"),
            ("invalid", "Invalid input"),
            ("", "Empty string"),
            ("   ", "Whitespace only"),
            ("7/5/25 ", "Trailing space"),
            (" 7/5/25", "Leading space"),
            ("7/5/25\n", "With newline"),
            ("7/5/25\t", "With tab"),
        ]
        
        for date_input, description in edge_cases:
            try:
                normalized, was_changed, original_format = normalize_date_format(date_input)
                success = True
                details = f"Input: '{date_input}' -> '{normalized}' (Format: {original_format})"
                
                # Phoenix analysis: Should handle gracefully
                if date_input in ["", "   ", "invalid"]:
                    if was_changed:
                        success = False
                        details += " - Should not change invalid input"
                elif date_input in ["7/5/25", "25/12/2024", "7-5-25", "2025.07.05"]:
                    if not was_changed:
                        success = False
                        details += " - Should normalize this format"
                
            except Exception as e:
                success = False
                details = f"Input: '{date_input}' - Exception occurred"
                error = e
            
            self.log_result(f"Date Normalization: {description}", success, details, error if 'error' in locals() else None)
    
    def test_malformed_metadata_blocks(self):
        """Test with malformed metadata blocks."""
        print("\n🦅 PHOENIX: Testing Malformed Metadata Blocks")
        print("=" * 60)
        
        malformed_cases = [
            ("No metadata block", "# Test\nThis file has no metadata block."),
            ("Empty metadata block", "---\n# Metadata\n---\n# Content"),
            ("Incomplete metadata block", "---\n# Metadata\n- **Document Title:** Test\n---"),
            ("Nested metadata blocks", "---\n# Metadata\n- **Document Title:** Test\n---\n---\n# More Metadata\n---"),
            ("Corrupted metadata", "---\n# Metadata\n- **Document Title:** Test\n- **Created:** invalid-date\n---"),
            ("Special characters in metadata", "---\n# Metadata\n- **Document Title:** Test 🚀\n- **Author:** User@domain.com\n---"),
            ("Unicode in metadata", "---\n# Metadata\n- **Document Title:** 测试文档\n- **Author:** 用户\n---"),
            ("HTML entities", "---\n# Metadata\n- **Document Title:** Test &amp; More\n- **Author:** User &lt;email&gt;\n---"),
            ("Very long title", "---\n# Metadata\n- **Document Title:** " + "A" * 1000 + "\n---"),
            ("Whitespace issues", "---\n# Metadata\n- **Document Title:**   Test   \n- **Author:**   User   \n---"),
        ]
        
        for case_name, content in malformed_cases:
            try:
                test_file = self.create_test_file(content, f"malformed_{case_name.lower().replace(' ', '_')}.md")
                result = self.run_validator(test_file, "--manual")
                
                # Phoenix analysis: Should handle gracefully without crashing
                success = result['success'] or result['returncode'] == 1  # Manual mode returns 1 for errors
                details = f"File: {case_name} - Return code: {result['returncode']}"
                
                if not success and "Timeout" in result['stderr']:
                    success = False
                    details += " - Timeout occurred"
                
            except Exception as e:
                success = False
                details = f"File: {case_name} - Exception occurred"
                error = e
            
            self.log_result(f"Malformed Metadata: {case_name}", success, details, error if 'error' in locals() else None)
    
    def test_file_size_edge_cases(self):
        """Test with very large and very small files."""
        print("\n🦅 PHOENIX: Testing File Size Edge Cases")
        print("=" * 60)
        
        # Very small file
        try:
            tiny_content = "---\n# Metadata\n- **Document Title:** Tiny\n---\n# Tiny"
            test_file = self.create_test_file(tiny_content, "tiny_file.md")
            result = self.run_validator(test_file, "--manual")
            
            success = result['success'] or result['returncode'] == 1
            details = f"Tiny file ({len(tiny_content)} bytes) - Return code: {result['returncode']}"
            
        except Exception as e:
            success = False
            details = "Tiny file - Exception occurred"
            error = e
        
        self.log_result("File Size: Tiny File", success, details, error if 'error' in locals() else None)
        
        # Very large file
        try:
            large_content = "---\n# Metadata\n- **Document Title:** Large\n---\n# Large File\n\n" + "# Section " + "\n\nContent " * 1000
            test_file = self.create_test_file(large_content, "large_file.md")
            result = self.run_validator(test_file, "--manual")
            
            success = result['success'] or result['returncode'] == 1
            details = f"Large file ({len(large_content)} bytes) - Return code: {result['returncode']}"
            
        except Exception as e:
            success = False
            details = "Large file - Exception occurred"
            error = e
        
        self.log_result("File Size: Large File", success, details, error if 'error' in locals() else None)
    
    def test_special_characters_and_encoding(self):
        """Test with special characters and encoding issues."""
        print("\n🦅 PHOENIX: Testing Special Characters and Encoding")
        print("=" * 60)
        
        special_cases = [
            ("Emojis", "---\n# Metadata\n- **Document Title:** Test 🚀🎉\n- **Author:** User 😊\n---"),
            ("Unicode", "---\n# Metadata\n- **Document Title:** 测试文档\n- **Author:** 用户\n---"),
            ("HTML entities", "---\n# Metadata\n- **Document Title:** Test &amp; More\n- **Author:** User &lt;email&gt;\n---"),
            ("Control characters", "---\n# Metadata\n- **Document Title:** Test\x00\x01\x02\n---"),
            ("Mixed encoding", "---\n# Metadata\n- **Document Title:** Test 🚀 &amp; 测试\n---"),
        ]
        
        for case_name, content in special_cases:
            try:
                test_file = self.create_test_file(content, f"special_{case_name.lower().replace(' ', '_')}.md")
                result = self.run_validator(test_file, "--manual")
                
                success = result['success'] or result['returncode'] == 1
                details = f"Special chars: {case_name} - Return code: {result['returncode']}"
                
            except Exception as e:
                success = False
                details = f"Special chars: {case_name} - Exception occurred"
                error = e
            
            self.log_result(f"Special Characters: {case_name}", success, details, error if 'error' in locals() else None)
    
    def test_missing_and_corrupted_files(self):
        """Test with missing and corrupted files."""
        print("\n🦅 PHOENIX: Testing Missing and Corrupted Files")
        print("=" * 60)
        
        # Test with non-existent file
        try:
            result = self.run_validator("non_existent_file.md", "--manual")
            success = not result['success']  # Should fail gracefully
            details = f"Non-existent file - Return code: {result['returncode']}"
            
        except Exception as e:
            success = False
            details = "Non-existent file - Exception occurred"
            error = e
        
        self.log_result("File Access: Non-existent File", success, details, error if 'error' in locals() else None)
        
        # Test with directory instead of file
        try:
            result = self.run_validator(".", "--manual")
            success = not result['success']  # Should fail gracefully
            details = f"Directory as file - Return code: {result['returncode']}"
            
        except Exception as e:
            success = False
            details = "Directory as file - Exception occurred"
            error = e
        
        self.log_result("File Access: Directory as File", success, details, error if 'error' in locals() else None)
    
    def test_performance_and_timeouts(self):
        """Test performance and timeout handling."""
        print("\n🦅 PHOENIX: Testing Performance and Timeouts")
        print("=" * 60)
        
        # Test with timeout
        try:
            test_file = self.create_test_file("---\n# Metadata\n- **Document Title:** Test\n---", "timeout_test.md")
            result = self.run_validator(test_file, "--manual", timeout=1)  # Very short timeout
            
            success = True  # Should complete within timeout
            details = f"Timeout test - Return code: {result['returncode']}"
            
            if "Timeout" in result['stderr']:
                success = False
                details += " - Timeout occurred unexpectedly"
            
        except Exception as e:
            success = False
            details = "Timeout test - Exception occurred"
            error = e
        
        self.log_result("Performance: Timeout Handling", success, details, error if 'error' in locals() else None)
    
    def generate_phoenix_report(self):
        """Generate comprehensive Phoenix adversarial testing report."""
        print("\n🦅 PHOENIX: Generating Adversarial Testing Report")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        total_failures = len(self.failures)
        total_successes = len(self.successes)
        success_rate = (total_successes / total_tests * 100) if total_tests > 0 else 0
        
        report = f"""
# 🦅 Phoenix Adversarial Testing Report
## Metadata Validator Robustness Assessment

**Test Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Phoenix Agent:** proto_phoenix-0.1.1
**Testing Duration:** {time.time() - self.start_time:.2f} seconds

## 📊 Test Summary
- **Total Tests:** {total_tests}
- **Successful Tests:** {total_successes}
- **Failed Tests:** {total_failures}
- **Success Rate:** {success_rate:.1f}%

## ❌ Failure Analysis
"""
        
        if self.failures:
            for failure in self.failures:
                report += f"""
### {failure['test_name']}
- **Details:** {failure['details']}
- **Error:** {failure['error']}
- **Timestamp:** {failure['timestamp']}
"""
        else:
            report += "\n**No failures detected!** 🎉\n"
        
        report += f"""
## ✅ Success Analysis
"""
        
        if self.successes:
            for success in self.successes:
                report += f"""
### {success['test_name']}
- **Details:** {success['details']}
- **Timestamp:** {success['timestamp']}
"""
        
        report += f"""
## 🔥 Phoenix Recommendations

### Critical Issues (if any):
"""
        
        if self.failures:
            report += "- Address all identified failure modes\n"
            report += "- Improve error handling for edge cases\n"
            report += "- Enhance robustness against malformed inputs\n"
        else:
            report += "- **Excellent robustness!** No critical issues found\n"
            report += "- Continue monitoring for new edge cases\n"
            report += "- Consider stress testing with larger datasets\n"
        
        report += f"""
### Quality Improvements:
- Monitor performance metrics
- Document edge case handling
- Establish regression testing
- Consider automated adversarial testing pipeline

## 🦅 Phoenix Wisdom
"From the ashes of failure, we rise with renewed wisdom and strength."

This testing session has identified {total_failures} potential failure modes and validated {total_successes} robust behaviors. 
The metadata validator demonstrates {'excellent' if success_rate >= 95 else 'good' if success_rate >= 80 else 'needs improvement'} resilience against adversarial inputs.
"""
        
        # Save report
        report_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'phoenix_report.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 Phoenix report saved to: {report_path}")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        print(f"❌ Failures: {total_failures}")
        print(f"✅ Successes: {total_successes}")
        
        return report

def main():
    """Main Phoenix adversarial testing execution."""
    print("🦅 PHOENIX ADVERSARIAL TESTING SUITE")
    print("=" * 60)
    print("Mission: From the ashes of failure, we rise with renewed wisdom and strength.")
    print("=" * 60)
    
    tester = PhoenixAdversarialTester()
    
    # Run all Phoenix tests
    tester.test_date_normalization_edge_cases()
    tester.test_malformed_metadata_blocks()
    tester.test_file_size_edge_cases()
    tester.test_special_characters_and_encoding()
    tester.test_missing_and_corrupted_files()
    tester.test_performance_and_timeouts()
    
    # Generate Phoenix report
    tester.generate_phoenix_report()
    
    print("\n🦅 Phoenix adversarial testing complete!")
    print("The validator has been tested against various failure modes and edge cases.")

if __name__ == "__main__":
    main() 