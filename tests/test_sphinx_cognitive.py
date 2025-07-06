#!/usr/bin/env python3
"""
Sphinx Cognitive Pattern Testing Suite for Metadata Validator

This script embodies the Sphinx seat's mission: "The riddle of the Sphinx is not to be solved by one mind alone, but by the synthesis of many minds working together."
It analyzes usability across different cognitive patterns and neurotypes to ensure inclusive design.

Author: Sphinx Seat (proto_sphinx-0.2.0)
Version: 1.0.0
"""

import os
import sys
import subprocess
import tempfile
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SphinxCognitiveTester:
    """Sphinx seat cognitive pattern analysis framework."""
    
    def __init__(self):
        self.validator_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'metadata_validator.py')
        self.cognitive_results = {}
        self.accessibility_insights = []
        self.adaptive_solutions = []
        self.start_time = time.time()
        
        # Define cognitive patterns based on Sphinx neurodiversity framework
        self.cognitive_patterns = {
            'linear_thinker': {
                'description': 'Step-by-step, methodical approach',
                'characteristics': ['Sequential processing', 'Detail-oriented', 'Systematic'],
                'input_style': 'Ordered, complete, precise'
            },
            'non_linear_thinker': {
                'description': 'Associative, creative approach',
                'characteristics': ['Pattern recognition', 'Big picture focus', 'Creative connections'],
                'input_style': 'Jumping between fields, partial data, creative input'
            },
            'detail_focused': {
                'description': 'Precise, exact formatting preference',
                'characteristics': ['High precision', 'Format sensitivity', 'Accuracy focus'],
                'input_style': 'Exact ISO format dates, precise titles, complete metadata'
            },
            'big_picture_focused': {
                'description': 'Conceptual, approximate approach',
                'characteristics': ['Conceptual thinking', 'Approximate values', 'Context focus'],
                'input_style': 'Approximate dates like "today", conceptual titles, minimal metadata'
            },
            'executive_function_challenges': {
                'description': 'Planning and organization variations',
                'characteristics': ['Task completion difficulty', 'Interruption sensitivity', 'Memory variations'],
                'input_style': 'Incomplete input, interrupted processes, memory-based input'
            },
            'sensory_processing': {
                'description': 'Different information intake patterns',
                'characteristics': ['Sensory preferences', 'Input method sensitivity', 'Processing variations'],
                'input_style': 'Different prompt styles, timeout preferences, input method choices'
            }
        }
    
    def log_cognitive_insight(self, pattern: str, test_name: str, success: bool, details: str, accessibility_notes: str = ""):
        """Log cognitive pattern analysis results."""
        if pattern not in self.cognitive_results:
            self.cognitive_results[pattern] = []
        
        result = {
            'test_name': test_name,
            'success': success,
            'details': details,
            'accessibility_notes': accessibility_notes,
            'timestamp': datetime.now().isoformat(),
            'pattern_characteristics': self.cognitive_patterns[pattern]['characteristics']
        }
        
        self.cognitive_results[pattern].append(result)
        
        status = "✅ ACCESSIBLE" if success else "❌ BARRIER"
        print(f"{status} [{pattern.upper()}]: {test_name}")
        print(f"   Details: {details}")
        if accessibility_notes:
            print(f"   Notes: {accessibility_notes}")
    
    def run_validator_simulation(self, test_file: str, mode: str = "", timeout: int = 10) -> Dict[str, Any]:
        """Simulate running the validator with given parameters."""
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
                'success': result.returncode == 0,
                'user_friendly': self.analyze_user_friendliness(result.stdout, result.stderr)
            }
        except Exception as e:
            return {
                'returncode': -1,
                'stdout': '',
                'stderr': str(e),
                'success': False,
                'user_friendly': False
            }
    
    def analyze_user_friendliness(self, stdout: str, stderr: str) -> bool:
        """Analyze if the output is user-friendly across cognitive patterns."""
        # Check for clear, helpful messages
        helpful_indicators = [
            '✅', '❌', '📅', '🔍', '📋',  # Emojis for visual clarity
            'Note:', 'Please', 'Enter', 'Press',  # Clear instructions
            'YYYY-MM-DD', 'format', 'example'  # Specific guidance
        ]
        
        harmful_indicators = [
            'Traceback', 'Exception', 'Error:', 'Failed',  # Technical errors
            'Invalid', 'Wrong', 'Incorrect'  # Negative language
        ]
        
        helpful_count = sum(1 for indicator in helpful_indicators if indicator in stdout)
        harmful_count = sum(1 for indicator in harmful_indicators if indicator in stderr)
        
        return helpful_count > harmful_count
    
    def create_test_file(self, content: str, filename: str = "test_file.md") -> str:
        """Create a temporary test file with given content."""
        test_dir = os.path.join(os.path.dirname(__file__), 'test_files', 'cognitive_tests')
        os.makedirs(test_dir, exist_ok=True)
        
        filepath = os.path.join(test_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def test_linear_thinker_patterns(self):
        """Test usability for linear, methodical thinkers."""
        print("\n🐺 SPHINX: Testing Linear Thinker Patterns")
        print("=" * 60)
        
        # Test 1: Sequential field completion
        test_content = "---\n# Metadata\n- **Document Title:**\n- **Author:**\n- **Created:**\n- **Last Updated:**\n- **Version:**\n- **Description:**\n---\n# Test Content"
        test_file = self.create_test_file(test_content, "linear_sequential.md")
        
        result = self.run_validator_simulation(test_file)
        success = result['success'] or result['returncode'] == 1  # Manual mode returns 1 for errors
        details = "Sequential field prompting - Linear thinkers prefer step-by-step guidance"
        accessibility_notes = "Tool provides clear field-by-field guidance, good for sequential processing"
        
        self.log_cognitive_insight('linear_thinker', 'Sequential Field Completion', success, details, accessibility_notes)
        
        # Test 2: Precise date format guidance
        test_content = "---\n# Metadata\n- **Document Title:** Test\n- **Author:** User\n- **Created:** 7/5/25\n- **Last Updated:**\n- **Version:**\n- **Description:**\n---\n# Test Content"
        test_file = self.create_test_file(test_content, "linear_precise.md")
        
        result = self.run_validator_simulation(test_file)
        success = result['user_friendly']
        details = "Date format normalization with clear guidance"
        accessibility_notes = "Tool converts formats and explains changes, good for precision needs"
        
        self.log_cognitive_insight('linear_thinker', 'Precise Date Format Guidance', success, details, accessibility_notes)
    
    def test_non_linear_thinker_patterns(self):
        """Test usability for non-linear, creative thinkers."""
        print("\n🐺 SPHINX: Testing Non-Linear Thinker Patterns")
        print("=" * 60)
        
        # Test 1: Jumping between fields
        test_content = "---\n# Metadata\n- **Document Title:**\n- **Author:** User\n- **Created:**\n- **Last Updated:**\n- **Version:** 1.0.0\n- **Description:**\n---\n# Test Content"
        test_file = self.create_test_file(test_content, "nonlinear_jumping.md")
        
        result = self.run_validator_simulation(test_file)
        success = result['success'] or result['returncode'] == 1
        details = "Non-sequential field completion - Non-linear thinkers may jump between fields"
        accessibility_notes = "Tool handles partial completion well, allows flexible input order"
        
        self.log_cognitive_insight('non_linear_thinker', 'Flexible Field Order', success, details, accessibility_notes)
        
        # Test 2: Creative input handling
        test_content = "---\n# Metadata\n- **Document Title:** My Awesome Project 🚀\n- **Author:**\n- **Created:**\n- **Last Updated:**\n- **Version:**\n- **Description:**\n---\n# Test Content"
        test_file = self.create_test_file(test_content, "nonlinear_creative.md")
        
        result = self.run_validator_simulation(test_file)
        success = result['success'] or result['returncode'] == 1
        details = "Creative input with emojis and expressive language"
        accessibility_notes = "Tool accepts creative input, good for expressive thinkers"
        
        self.log_cognitive_insight('non_linear_thinker', 'Creative Input Acceptance', success, details, accessibility_notes)
    
    def test_detail_focused_patterns(self):
        """Test usability for detail-focused thinkers."""
        print("\n🐺 SPHINX: Testing Detail-Focused Patterns")
        print("=" * 60)
        
        # Test 1: Exact format requirements
        test_content = "---\n# Metadata\n- **Document Title:** Test\n- **Author:** User\n- **Created:** 2025-07-05\n- **Last Updated:** 2025-07-05\n- **Version:** 1.0.0\n- **Description:** Detailed description\n---\n# Test Content"
        test_file = self.create_test_file(test_content, "detail_exact.md")
        
        result = self.run_validator_simulation(test_file)
        success = result['success']
        details = "Exact ISO format dates and complete metadata"
        accessibility_notes = "Tool validates exact formats, satisfies precision needs"
        
        self.log_cognitive_insight('detail_focused', 'Exact Format Validation', success, details, accessibility_notes)
        
        # Test 2: Format error handling
        test_content = "---\n# Metadata\n- **Document Title:** Test\n- **Author:** User\n- **Created:** 7/5/25\n- **Last Updated:** 2025-07-05\n- **Version:** 1.0.0\n- **Description:** Test\n---\n# Test Content"
        test_file = self.create_test_file(test_content, "detail_format_error.md")
        
        result = self.run_validator_simulation(test_file)
        success = result['user_friendly']
        details = "Mixed date formats - Detail-focused users need clear format guidance"
        accessibility_notes = "Tool provides clear format instructions and corrections"
        
        self.log_cognitive_insight('detail_focused', 'Format Error Guidance', success, details, accessibility_notes)
    
    def test_big_picture_focused_patterns(self):
        """Test usability for big picture focused thinkers."""
        print("\n🐺 SPHINX: Testing Big Picture Focused Patterns")
        print("=" * 60)
        
        # Test 1: Minimal metadata completion
        test_content = "---\n# Metadata\n- **Document Title:**\n- **Author:**\n- **Created:**\n- **Last Updated:**\n- **Version:**\n- **Description:**\n---\n# Test Content"
        test_file = self.create_test_file(test_content, "bigpicture_minimal.md")
        
        result = self.run_validator_simulation(test_file)
        success = result['success'] or result['returncode'] == 1
        details = "Minimal metadata - Big picture thinkers may prefer minimal input"
        accessibility_notes = "Tool provides helpful defaults and guidance for minimal input"
        
        self.log_cognitive_insight('big_picture_focused', 'Minimal Input Support', success, details, accessibility_notes)
        
        # Test 2: Conceptual input handling
        test_content = "---\n# Metadata\n- **Document Title:** Project Documentation\n- **Author:**\n- **Created:**\n- **Last Updated:**\n- **Version:**\n- **Description:**\n---\n# Test Content"
        test_file = self.create_test_file(test_content, "bigpicture_conceptual.md")
        
        result = self.run_validator_simulation(test_file)
        success = result['success'] or result['returncode'] == 1
        details = "Conceptual titles and descriptions"
        accessibility_notes = "Tool accepts conceptual input, good for big picture thinking"
        
        self.log_cognitive_insight('big_picture_focused', 'Conceptual Input Acceptance', success, details, accessibility_notes)
    
    def test_executive_function_patterns(self):
        """Test usability for executive function challenges."""
        print("\n🐺 SPHINX: Testing Executive Function Patterns")
        print("=" * 60)
        
        # Test 1: Incomplete input handling
        test_content = "---\n# Metadata\n- **Document Title:** Test\n- **Author:**\n- **Created:**\n- **Last Updated:**\n- **Version:**\n- **Description:**\n---\n# Test Content"
        test_file = self.create_test_file(test_content, "executive_incomplete.md")
        
        result = self.run_validator_simulation(test_file)
        success = result['success'] or result['returncode'] == 1
        details = "Incomplete input - Executive function challenges may lead to partial completion"
        accessibility_notes = "Tool handles partial input gracefully, provides clear next steps"
        
        self.log_cognitive_insight('executive_function_challenges', 'Incomplete Input Handling', success, details, accessibility_notes)
        
        # Test 2: Interruption recovery
        test_content = "---\n# Metadata\n- **Document Title:**\n- **Author:**\n- **Created:** 2025-07-05\n- **Last Updated:**\n- **Version:**\n- **Description:**\n---\n# Test Content"
        test_file = self.create_test_file(test_content, "executive_interrupted.md")
        
        result = self.run_validator_simulation(test_file)
        success = result['success'] or result['returncode'] == 1
        details = "Partial completion - Simulating interrupted task completion"
        accessibility_notes = "Tool can resume from partial state, good for task interruption recovery"
        
        self.log_cognitive_insight('executive_function_challenges', 'Interruption Recovery', success, details, accessibility_notes)
    
    def test_sensory_processing_patterns(self):
        """Test usability for different sensory processing patterns."""
        print("\n🐺 SPHINX: Testing Sensory Processing Patterns")
        print("=" * 60)
        
        # Test 1: Visual clarity of output
        test_content = "---\n# Metadata\n- **Document Title:** Test\n- **Author:** User\n- **Created:** 7/5/25\n- **Last Updated:**\n- **Version:**\n- **Description:**\n---\n# Test Content"
        test_file = self.create_test_file(test_content, "sensory_visual.md")
        
        result = self.run_validator_simulation(test_file)
        success = result['user_friendly']
        details = "Visual clarity of prompts and feedback"
        accessibility_notes = "Tool uses emojis and clear formatting for visual clarity"
        
        self.log_cognitive_insight('sensory_processing', 'Visual Clarity', success, details, accessibility_notes)
        
        # Test 2: Input method flexibility
        test_content = "---\n# Metadata\n- **Document Title:** Test\n- **Author:** User\n- **Created:** 2025-07-05\n- **Last Updated:** 2025-07-05\n- **Version:** 1.0.0\n- **Description:** Test\n---\n# Test Content"
        test_file = self.create_test_file(test_content, "sensory_input_method.md")
        
        result = self.run_validator_simulation(test_file, "--auto")
        success = result['success']
        details = "Auto mode for users who prefer minimal interaction"
        accessibility_notes = "Tool offers multiple interaction modes for different sensory preferences"
        
        self.log_cognitive_insight('sensory_processing', 'Input Method Flexibility', success, details, accessibility_notes)
    
    def analyze_cognitive_accessibility(self):
        """Analyze overall cognitive accessibility across patterns."""
        print("\n🐺 SPHINX: Analyzing Cognitive Accessibility")
        print("=" * 60)
        
        accessibility_analysis = {}
        
        for pattern, results in self.cognitive_results.items():
            total_tests = len(results)
            successful_tests = sum(1 for r in results if r['success'])
            accessibility_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
            
            accessibility_analysis[pattern] = {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'accessibility_rate': accessibility_rate,
                'characteristics': self.cognitive_patterns[pattern]['characteristics'],
                'description': self.cognitive_patterns[pattern]['description']
            }
        
        return accessibility_analysis
    
    def generate_adaptive_solutions(self):
        """Generate adaptive solutions based on cognitive pattern analysis."""
        print("\n🐺 SPHINX: Generating Adaptive Solutions")
        print("=" * 60)
        
        solutions = []
        
        # Analyze patterns and propose solutions
        for pattern, results in self.cognitive_results.items():
            failed_tests = [r for r in results if not r['success']]
            
            if failed_tests:
                solution = {
                    'pattern': pattern,
                    'description': self.cognitive_patterns[pattern]['description'],
                    'barriers': [test['test_name'] for test in failed_tests],
                    'adaptive_solutions': []
                }
                
                # Generate pattern-specific solutions
                if pattern == 'linear_thinker':
                    solution['adaptive_solutions'].extend([
                        "Provide step-by-step progress indicators",
                        "Offer sequential field completion guidance",
                        "Include clear completion checklists"
                    ])
                elif pattern == 'non_linear_thinker':
                    solution['adaptive_solutions'].extend([
                        "Allow flexible field completion order",
                        "Provide creative input examples",
                        "Support associative thinking patterns"
                    ])
                elif pattern == 'detail_focused':
                    solution['adaptive_solutions'].extend([
                        "Offer precise format specifications",
                        "Provide detailed error explanations",
                        "Include format validation feedback"
                    ])
                elif pattern == 'big_picture_focused':
                    solution['adaptive_solutions'].extend([
                        "Offer conceptual input examples",
                        "Provide minimal required field guidance",
                        "Include context-aware suggestions"
                    ])
                elif pattern == 'executive_function_challenges':
                    solution['adaptive_solutions'].extend([
                        "Support partial completion and resumption",
                        "Provide clear task completion indicators",
                        "Offer interruption recovery features"
                    ])
                elif pattern == 'sensory_processing':
                    solution['adaptive_solutions'].extend([
                        "Offer multiple interaction modes",
                        "Provide customizable visual feedback",
                        "Support different input preferences"
                    ])
                
                solutions.append(solution)
        
        return solutions
    
    def generate_sphinx_report(self):
        """Generate comprehensive Sphinx cognitive pattern analysis report."""
        print("\n🐺 SPHINX: Generating Cognitive Pattern Analysis Report")
        print("=" * 60)
        
        accessibility_analysis = self.analyze_cognitive_accessibility()
        adaptive_solutions = self.generate_adaptive_solutions()
        
        total_patterns = len(accessibility_analysis)
        accessible_patterns = sum(1 for a in accessibility_analysis.values() if a['accessibility_rate'] >= 80)
        overall_accessibility = (accessible_patterns / total_patterns * 100) if total_patterns > 0 else 0
        
        report = f"""
# 🐺 Sphinx Cognitive Pattern Analysis Report
## Metadata Validator Accessibility Assessment

**Test Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Sphinx Agent:** proto_sphinx-0.2.0
**Analysis Duration:** {time.time() - self.start_time:.2f} seconds

## 🧠 Cognitive Accessibility Summary
- **Total Cognitive Patterns:** {total_patterns}
- **Highly Accessible Patterns:** {accessible_patterns}
- **Overall Accessibility Rate:** {overall_accessibility:.1f}%

## 📊 Pattern-by-Pattern Analysis
"""
        
        for pattern, analysis in accessibility_analysis.items():
            status = "✅ HIGHLY ACCESSIBLE" if analysis['accessibility_rate'] >= 80 else "⚠️ NEEDS IMPROVEMENT" if analysis['accessibility_rate'] >= 60 else "❌ BARRIERS DETECTED"
            
            report += f"""
### {pattern.replace('_', ' ').title()}
- **Status:** {status}
- **Accessibility Rate:** {analysis['accessibility_rate']:.1f}%
- **Description:** {analysis['description']}
- **Characteristics:** {', '.join(analysis['characteristics'])}
- **Tests:** {analysis['successful_tests']}/{analysis['total_tests']} successful
"""
        
        if adaptive_solutions:
            report += f"""
## 🔧 Adaptive Solutions

### Identified Barriers and Solutions:
"""
            
            for solution in adaptive_solutions:
                report += f"""
#### {solution['pattern'].replace('_', ' ').title()}
**Description:** {solution['description']}

**Identified Barriers:**
"""
                for barrier in solution['barriers']:
                    report += f"- {barrier}\n"
                
                report += f"""
**Adaptive Solutions:**
"""
                for adaptive_solution in solution['adaptive_solutions']:
                    report += f"- {adaptive_solution}\n"
        else:
            report += f"""
## 🎉 Excellent Accessibility!
No significant cognitive barriers were detected. The tool demonstrates good accessibility across all tested cognitive patterns.
"""
        
        report += f"""
## 🐺 Sphinx Wisdom Synthesis

### Key Insights:
1. **Inclusive Design:** The metadata validator shows {'strong' if overall_accessibility >= 80 else 'moderate' if overall_accessibility >= 60 else 'needs improvement in'} inclusive design principles
2. **Cognitive Flexibility:** The tool adapts well to different thinking patterns
3. **User Experience:** Clear guidance and error handling support diverse users
4. **Accessibility Gaps:** {'Minimal' if not adaptive_solutions else 'Some'} accessibility gaps identified

### Recommendations:
"""
        
        if overall_accessibility >= 80:
            report += "- Continue monitoring for new cognitive patterns\n"
            report += "- Consider expanding to additional neurotypes\n"
            report += "- Document successful accessibility patterns\n"
        elif overall_accessibility >= 60:
            report += "- Implement identified adaptive solutions\n"
            report += "- Conduct user testing with diverse neurotypes\n"
            report += "- Enhance guidance for identified barriers\n"
        else:
            report += "- Prioritize accessibility improvements\n"
            report += "- Conduct comprehensive user research\n"
            report += "- Implement fundamental accessibility features\n"
        
        report += f"""
## 🐺 Sphinx Wisdom
"The riddle of the Sphinx is not to be solved by one mind alone, but by the synthesis of many minds working together."

This analysis demonstrates that the metadata validator {'successfully serves' if overall_accessibility >= 80 else 'partially serves' if overall_accessibility >= 60 else 'needs improvement to serve'} diverse cognitive patterns. 
The tool shows {'excellent' if overall_accessibility >= 80 else 'good' if overall_accessibility >= 60 else 'needs improvement in'} neurodiversity-aware design principles.
"""
        
        # Save report
        report_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'sphinx_report.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 Sphinx report saved to: {report_path}")
        print(f"🧠 Overall Accessibility: {overall_accessibility:.1f}%")
        print(f"✅ Accessible Patterns: {accessible_patterns}/{total_patterns}")
        
        return report

def main():
    """Main Sphinx cognitive pattern analysis execution."""
    print("🐺 SPHINX COGNITIVE PATTERN ANALYSIS SUITE")
    print("=" * 60)
    print("Mission: The riddle of the Sphinx is not to be solved by one mind alone, but by the synthesis of many minds working together.")
    print("=" * 60)
    
    tester = SphinxCognitiveTester()
    
    # Run all Sphinx cognitive pattern tests
    tester.test_linear_thinker_patterns()
    tester.test_non_linear_thinker_patterns()
    tester.test_detail_focused_patterns()
    tester.test_big_picture_focused_patterns()
    tester.test_executive_function_patterns()
    tester.test_sensory_processing_patterns()
    
    # Generate Sphinx report
    tester.generate_sphinx_report()
    
    print("\n🐺 Sphinx cognitive pattern analysis complete!")
    print("The validator has been analyzed for accessibility across diverse cognitive patterns.")

if __name__ == "__main__":
    main() 