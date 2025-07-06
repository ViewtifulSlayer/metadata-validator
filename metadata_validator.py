"""
metadata_validator.py

Enhanced metadata validator for markdown documentation files.
- Checks for required fields and ISO 8601 date compliance (YYYY-MM-DD format).
- Offers to auto-fill missing/invalid dates with the current system date.
- Automatically corrects common date formats to YYYY-MM-DD.
- By default, auto-updates 'Last Updated' to today unless --no-auto-update is passed.
- Extensible for accessibility and neurodiversity features.
- Includes timeout handling and gentle prompts for better UX.
"""
import re
import sys
import os
import time
import threading
from datetime import datetime
import subprocess
from typing import Optional

# Import configuration system
try:
    from config.config_loader import get_config_loader, get_required_fields, get_date_pattern, get_defaults, get_timeout_config
except ImportError:
    # Fallback to hardcoded values if config system is not available
    def get_required_fields():
        return ['Document Title', 'Author', 'Created', 'Last Updated', 'Version', 'Description']
    
    def get_date_pattern():
        return r'\d{4}-\d{2}-\d{2}'
    
    def get_defaults():
        return {
            'Document Title': 'Unknown',
            'Author': 'Unknown',
            'Created': None,
            'Last Updated': None,
            'Version': '0.1.0',
            'Description': 'No description provided.'
        }
    
    def get_timeout_config():
        return {
            'initial_timeout': None,
            'gentle_prompt_delay': None,
            'final_timeout': None
        }

# Load configuration values
REQUIRED_FIELDS = get_required_fields()
ISO_DATE_PATTERN = get_date_pattern()
DEFAULTS = get_defaults()
TIMEOUT_CONFIG = get_timeout_config()

# Timeout configuration - DISABLED
INITIAL_TIMEOUT = TIMEOUT_CONFIG.get('initial_timeout')
GENTLE_PROMPT_DELAY = TIMEOUT_CONFIG.get('gentle_prompt_delay')
FINAL_TIMEOUT = TIMEOUT_CONFIG.get('final_timeout')


def normalize_date_format(date_str):
    """
    Convert various date formats to YYYY-MM-DD.
    Returns (normalized_date, was_changed, original_format)
    """
    if not date_str:
        return None, False, None
    
    # Already in correct format
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
        # YYYY.MM.DD (ISO-like with dots)
        (r'(\d{4})\.(\d{1,2})\.(\d{1,2})', lambda m: f"{m.group(1)}-{m.group(2).zfill(2)}-{m.group(3).zfill(2)}"),
        # YYYY.MM.DD (2-digit year variant)
        (r'(\d{2})\.(\d{1,2})\.(\d{1,2})', lambda m: f"20{m.group(1)}-{m.group(2).zfill(2)}-{m.group(3).zfill(2)}"),
        # MM.DD.YYYY
        (r'(\d{1,2})\.(\d{1,2})\.(\d{4})', lambda m: f"{m.group(3)}-{m.group(1).zfill(2)}-{m.group(2).zfill(2)}"),
        # MM.DD.YY (2-digit year)
        (r'(\d{1,2})\.(\d{1,2})\.(\d{2})', lambda m: f"20{m.group(3)}-{m.group(1).zfill(2)}-{m.group(2).zfill(2)}"),
        # DD.MM.YYYY
        (r'(\d{1,2})\.(\d{1,2})\.(\d{4})', lambda m: f"{m.group(3)}-{m.group(2).zfill(2)}-{m.group(1).zfill(2)}"),
        # DD.MM.YY (2-digit year)
        (r'(\d{1,2})\.(\d{1,2})\.(\d{2})', lambda m: f"20{m.group(3)}-{m.group(2).zfill(2)}-{m.group(1).zfill(2)}"),
        # Compact formats (YYYYMMDD, YYMMDD)
        (r'(\d{4})(\d{2})(\d{2})', lambda m: f"{m.group(1)}-{m.group(2)}-{m.group(3)}"),
        (r'(\d{2})(\d{2})(\d{2})', lambda m: f"20{m.group(1)}-{m.group(2)}-{m.group(3)}"),
        # US format with month names (abbreviated and full)
        (r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2}),?\s+(\d{4})', 
         lambda m: f"{m.group(3)}-{str(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'].index(m.group(1))+1).zfill(2)}-{m.group(2).zfill(2)}"),
        (r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})', 
         lambda m: f"{m.group(3)}-{str(['January','February','March','April','May','June','July','August','September','October','November','December'].index(m.group(1))+1).zfill(2)}-{m.group(2).zfill(2)}"),
        # NEW: DD-Mon-YYYY and DD-Month-YYYY
        (r'(\d{1,2})-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(\d{4})',
         lambda m: f"{m.group(3)}-{str(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'].index(m.group(2))+1).zfill(2)}-{m.group(1).zfill(2)}"),
        (r'(\d{1,2})-(January|February|March|April|May|June|July|August|September|October|November|December)-(\d{4})',
         lambda m: f"{m.group(3)}-{str(['January','February','March','April','May','June','July','August','September','October','November','December'].index(m.group(2))+1).zfill(2)}-{m.group(1).zfill(2)}"),
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


def confirm_date_interpretation(original_date, normalized_date, original_format):
    """Ask user to confirm date interpretation when format is ambiguous."""
    prompt = (
        f"I found a date '{original_date}' in format '{original_format}'.\n"
        f"I interpreted it as: {normalized_date}\n"
        f"Is this correct? [Y/n]: "
    )
    
    timeout_input = TimeoutInput(INITIAL_TIMEOUT, GENTLE_PROMPT_DELAY, FINAL_TIMEOUT)
    resp = timeout_input.get_input_with_timeout(prompt)
    
    if resp is None:
        print("Timeout reached. Using original date as-is.")
        return original_date
    
    resp = resp.strip().lower()
    return normalized_date if resp in ('', 'y', 'yes') else original_date


class TimeoutInput:
    """Handles input with timeout and gentle prompts."""
    
    def __init__(self, initial_timeout: Optional[int] = 60, gentle_delay: Optional[int] = 15, final_timeout: Optional[int] = 30):
        self.initial_timeout = initial_timeout
        self.gentle_delay = gentle_delay
        self.final_timeout = final_timeout
        self.user_input = None
        self.input_received = threading.Event()
    
    def _input_thread(self, prompt):
        """Thread function to get user input."""
        try:
            self.user_input = input(prompt)
            self.input_received.set()
        except (EOFError, KeyboardInterrupt):
            self.input_received.set()
    
    def get_input_with_timeout(self, prompt):
        """Get user input with timeout and gentle prompts."""
        # If timeouts are disabled (None), use regular input
        if self.initial_timeout is None:
            try:
                return input(prompt)
            except (EOFError, KeyboardInterrupt):
                return None
        
        # Start input thread
        input_thread = threading.Thread(target=self._input_thread, args=(prompt,))
        input_thread.daemon = True
        input_thread.start()
        
        # Wait for initial timeout
        if self.input_received.wait(self.gentle_delay):
            return self.user_input
        
        # Gentle prompt
        print("\n🤔 Are you there? Still waiting for your response...")
        print("(You can type 'Y' and press Enter to continue, or 'N' to skip)")
        
        # Wait for final timeout
        if self.input_received.wait(self.final_timeout):
            return self.user_input
        
        # Final timeout reached
        print(f"\n⏰ Timeout reached after {self.initial_timeout} seconds.")
        print("No response received. Exiting gracefully...")
        return None


def extract_metadata_block(lines):
    in_block = False
    metadata = {}
    block_start = block_end = None
    for idx, line in enumerate(lines):
        if line.strip().startswith('---'):
            if not in_block:
                block_start = idx
            else:
                block_end = idx
            in_block = not in_block
            continue
        if in_block and line.strip().startswith('- **'):
            match = re.match(r'- \*\*(.+?):\*\* (.+)', line.strip())
            if match:
                key, value = match.groups()
                metadata[key.strip()] = value.strip()
            else:
                # Handle empty values (no content after colon and space)
                match = re.match(r'- \*\*(.+?):\*\*$', line.strip())
                if match:
                    key = match.group(1)
                    metadata[key.strip()] = ''
    return metadata, block_start, block_end


def validate_metadata(metadata):
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in metadata or not metadata[field]:
            errors.append(f"Missing or empty field: {field}")
    # Date checks
    for date_field in ['Created', 'Last Updated']:
        if date_field in metadata:
            if not re.fullmatch(ISO_DATE_PATTERN, metadata[date_field]):
                errors.append(f"{date_field} is not in ISO 8601 format (YYYY-MM-DD): {metadata[date_field]}")
    return errors


def prompt_autofill(field_name, current_value=None):
    today = datetime.now().strftime('%Y-%m-%d')
    if current_value:
        prompt = (
            f"Field '{field_name}' has invalid value '{current_value}'. "
            f"Auto-fill with today's date ({today})? [Y/n]: "
            f"\n(Type Y and press Enter to accept, or N to skip and update manually.)\n"
        )
    else:
        prompt = (
            f"Field '{field_name}' is missing. Auto-fill with today's date ({today})? [Y/n]: "
            f"\n(Type Y and press Enter to accept, or N to skip and update manually.)\n"
        )
    
    timeout_input = TimeoutInput(INITIAL_TIMEOUT, GENTLE_PROMPT_DELAY, FINAL_TIMEOUT)
    resp = timeout_input.get_input_with_timeout(prompt)
    
    if resp is None:
        print(f"Timeout reached for '{field_name}'. Skipping auto-fill.")
        return False
    
    resp = resp.strip().lower()
    return resp in ('', 'y', 'yes')


def update_metadata_block(lines, metadata, block_start, block_end, updates):
    # Rebuild the metadata block with updates
    new_block = ['---\n', '# Metadata\n']
    for field in REQUIRED_FIELDS:
        value = updates.get(field, metadata.get(field, ''))
        new_block.append(f"- **{field}:** {value}\n")
    new_block.append('---\n')
    return lines[:block_start] + new_block + lines[block_end+1:]


def display_metadata(metadata):
    """Display the metadata in a formatted way."""
    print("\n📋 Document Metadata:")
    print("-" * 40)
    for field in REQUIRED_FIELDS:
        value = metadata.get(field, 'Not set')
        print(f"  {field}: {value}")
    print("-" * 40)


def wait_for_user_exit():
    """Wait for user input before exiting to prevent window from closing."""
    print("\n" + "="*60)
    print("✅ Validation complete!")
    print("Press Enter to exit...")
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass


def extract_first_heading(lines, metadata_block_end):
    """
    Extract the first markdown heading (e.g., # Title) after the metadata block.
    Returns the heading text, or None if not found.
    """
    for idx, line in enumerate(lines):
        if idx <= metadata_block_end:
            continue
        match = re.match(r'#+\s+(.+)', line.strip())
        if match:
            return match.group(1).strip()
    return None


def prettify_filename(filename):
    """
    Convert filename to a human-friendly title (e.g., 'my_file_name.md' -> 'My File Name').
    """
    name = os.path.splitext(os.path.basename(filename))[0]
    name = name.replace('_', ' ').replace('-', ' ')
    return name.title()


def find_changelog_file(directory):
    """Find changelog file in the given directory."""
    changelog_files = ['CHANGELOG.md', 'changelog.md', 'Changelog.md']
    for filename in changelog_files:
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            return filepath
    return None


def extract_changelog_section_from_file(file_path):
    """Extract changelog section from within a markdown file, capturing all version entries until the next top-level section or end of file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Find the start of the changelog section
        changelog_start = None
        for i, line in enumerate(lines):
            if re.match(r'^#{1,4} +Changelog *$', line.strip(), re.IGNORECASE) or \
               re.match(r'^## +History *$', line.strip(), re.IGNORECASE) or \
               re.match(r'^## +Version History *$', line.strip(), re.IGNORECASE):
                changelog_start = i
                break
        if changelog_start is None:
            return None
        # Collect all lines until the next top-level section (e.g., #, ## not part of a version heading) or end of file
        changelog_lines = []
        for line in lines[changelog_start+1:]:
            if re.match(r'^#{1,2} +[^\[]', line) and not re.match(r'^## +\[', line):
                break
            changelog_lines.append(line.rstrip('\n'))
        return '\n'.join(changelog_lines).strip()
    except Exception as e:
        print(f"⚠️  Warning: Could not read file {file_path}: {e}")
        return None


def suggest_changelog_placement(file_path, document_type=None):
    """
    Suggest optimal changelog placement based on document type and content.
    Returns placement recommendation and example structure.
    """
    if not document_type:
        filename = os.path.basename(file_path).lower()
        if filename in ['readme.md', 'readme.txt']:
            document_type = 'readme'
        elif any(keyword in filename for keyword in ['api', 'reference', 'docs/']):
            document_type = 'documentation'
        elif any(keyword in filename for keyword in ['config', 'setup', 'install']):
            document_type = 'configuration'
        else:
            document_type = 'general'
    
    placement_guide = {
        'readme': {
            'position': 'Near the end, before License/Contact sections',
            'heading_level': '##',
            'example': """## Changelog

## [1.1.0] - 2025-07-05
### Added
- New features

## [1.0.0] - 2025-01-15
### Added
- Initial release

---

## License
MIT License"""
        },
        'documentation': {
            'position': 'At the end, as a reference section',
            'heading_level': '##',
            'example': """## Changelog

## [2.0.0] - 2025-07-05
### Changed
- Updated interface

## [1.5.0] - 2025-06-01
### Added
- New features"""
        },
        'configuration': {
            'position': 'At the very end, as a footer',
            'heading_level': '##',
            'example': """---

## Changelog

## [1.2.0] - 2025-07-05
### Added
- New configuration options"""
        },
        'general': {
            'position': 'Near the end, before any appendices',
            'heading_level': '##',
            'example': """## Changelog

## [1.0.0] - 2025-07-05
### Added
- Initial features"""
        }
    }
    
    return placement_guide.get(document_type, placement_guide['general'])


def determine_changelog_preference(file_path, directory):
    """
    Determine whether to prefer separate CHANGELOG.md or embedded changelog section.
    Returns: 'separate', 'embedded', or 'both'
    """
    # Check if separate changelog file exists
    separate_changelog = find_changelog_file(directory)
    
    # Check if current file has embedded changelog
    embedded_changelog = extract_changelog_section_from_file(file_path)
    
    # Determine file type and context
    filename = os.path.basename(file_path).lower()
    is_package_file = any(keyword in filename for keyword in ['__init__.py', 'setup.py', 'pyproject.toml'])
    is_readme = filename in ['readme.md', 'readme.txt']
    is_documentation = any(keyword in filename for keyword in ['docs/', 'documentation', 'guide', 'manual'])
    
    # Decision logic
    if is_package_file:
        return 'separate'  # Python packages should use separate CHANGELOG.md
    elif is_readme and separate_changelog:
        return 'separate'  # README with separate changelog file
    elif is_readme and embedded_changelog:
        return 'embedded'  # README with embedded changelog
    elif is_documentation and embedded_changelog:
        return 'embedded'  # Documentation files often have embedded changelogs
    elif separate_changelog:
        return 'separate'  # Separate file exists, prefer it
    elif embedded_changelog:
        return 'embedded'  # Only embedded changelog exists
    else:
        return 'both'  # No changelog found, suggest both options


def extract_latest_version_from_changelog(changelog_path):
    """Extract the latest version from a changelog file."""
    try:
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for version patterns like [1.0.0] or ## [1.0.0]
        version_patterns = [
            r'## \[([0-9]+\.[0-9]+\.[0-9]+)\]',  # ## [1.0.0]
            r'\[([0-9]+\.[0-9]+\.[0-9]+)\]',     # [1.0.0]
            r'## ([0-9]+\.[0-9]+\.[0-9]+)',      # ## 1.0.0
        ]
        
        all_versions = []
        for pattern in version_patterns:
            matches = re.findall(pattern, content)
            all_versions.extend(matches)
        
        if all_versions:
            # Sort versions and return the latest (highest)
            def version_key(version):
                return tuple(map(int, version.split('.')))
            
            latest_version = max(all_versions, key=version_key)
            return latest_version
        
        return None
    except Exception as e:
        print(f"⚠️  Warning: Could not read changelog file {changelog_path}: {e}")
        return None


def normalize_changelog_dates(changelog_path, auto_fix=False):
    """
    Normalize all dates in changelog headings to YYYY-MM-DD format.
    If auto_fix is True, update the file in place.
    Returns True if changes were made, False otherwise.
    """
    try:
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex to match headings like: ## [1.2.0] - <date>
        pattern = r'(## \[[0-9]+\.[0-9]+\.[0-9]+\] - )(.*)'
        changes_made = False

        def replacer(match):
            nonlocal changes_made
            prefix, date_str = match.groups()
            original_date = date_str.strip()
            normalized = normalize_date_format(original_date)
            
            if normalized and normalized != original_date:
                changes_made = True
                print(f"🔄 Normalizing changelog date: '{original_date}' → '{normalized}'")
                return f"{prefix}{normalized}"
            return match.group(0)

        new_content = re.sub(pattern, replacer, content)

        if changes_made and auto_fix:
            with open(changelog_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("✅ Changelog dates normalized in file.")
        elif changes_made:
            print("💡 Suggestion: Update changelog dates to normalized format (use --auto to apply).")
        
        return changes_made
        
    except Exception as e:
        print(f"⚠️  Warning: Could not normalize changelog dates in {changelog_path}: {e}")
        return False


def validate_changelog_date_format(changelog_path):
    """
    Validate that all dates in changelog headings are in YYYY-MM-DD format.
    Returns True if all dates are properly formatted, False otherwise.
    """
    try:
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex to match headings like: ## [1.2.0] - <date>
        pattern = r'## \[[0-9]+\.[0-9]+\.[0-9]+\] - (.*)'
        matches = re.findall(pattern, content)
        
        invalid_dates = []
        for date_str in matches:
            date_str = date_str.strip()
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                invalid_dates.append(date_str)
        
        if invalid_dates:
            print(f"⚠️  Found {len(invalid_dates)} changelog entries with non-standard date formats:")
            for date in invalid_dates:
                print(f"   • {date}")
            print("💡 Use --normalize-dates to convert to YYYY-MM-DD format.")
            return False
        
        return True
        
    except Exception as e:
        print(f"⚠️  Warning: Could not validate changelog dates in {changelog_path}: {e}")
        return False


def check_changelog_consistency(metadata_version, file_path, directory):
    """Check if the metadata version matches the changelog version (separate or embedded)."""
    # Determine changelog preference for this file
    preference = determine_changelog_preference(file_path, directory)
    
    # Check separate changelog file
    separate_changelog_path = find_changelog_file(directory)
    separate_version = None
    if separate_changelog_path:
        separate_version = extract_latest_version_from_changelog(separate_changelog_path)
    
    # Check embedded changelog section
    embedded_changelog_content = extract_changelog_section_from_file(file_path)
    embedded_version = None
    if embedded_changelog_content:
        # Create a temporary file to use existing extraction logic
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
            temp_file.write(embedded_changelog_content)
            temp_file_path = temp_file.name
        
        try:
            embedded_version = extract_latest_version_from_changelog(temp_file_path)
        finally:
            os.unlink(temp_file_path)
    
    # Determine which version to check based on preference
    if preference == 'separate':
        if separate_version:
            if metadata_version != separate_version:
                print(f"⚠️  Version mismatch detected:")
                print(f"   Metadata version: {metadata_version}")
                print(f"   Separate changelog version: {separate_version}")
                print(f"   Changelog file: {separate_changelog_path}")
                print(f"\n💡 To fix this:")
                print(f"   1. Update your metadata version to {separate_version}, OR")
                print(f"   2. Add a new changelog entry for version {metadata_version}")
                print(f"\n📝 Suggested changelog entry:")
                print(suggest_changelog_entry(metadata_version, "minor"))
                return False
            else:
                print(f"✅ Version consistency verified: {metadata_version} (separate changelog)")
                return True
        else:
            print("ℹ️  No separate changelog file found. Consider creating CHANGELOG.md")
            print(f"💡 You can create a CHANGELOG.md file with:")
            print(suggest_changelog_entry(metadata_version, "initial"))
            return True
    
    elif preference == 'embedded':
        if embedded_version:
            if metadata_version != embedded_version:
                print(f"⚠️  Version mismatch detected:")
                print(f"   Metadata version: {metadata_version}")
                print(f"   Embedded changelog version: {embedded_version}")
                print(f"   File: {file_path}")
                return False
            else:
                print(f"✅ Version consistency verified: {metadata_version} (embedded changelog)")
                return True
        else:
            print("ℹ️  No embedded changelog section found. Consider adding a Changelog section")
            return True
    
    else:  # preference == 'both'
        # Check both and report any mismatches
        mismatches = []
        if separate_version and metadata_version != separate_version:
            mismatches.append(f"Separate changelog: {separate_version}")
        if embedded_version and metadata_version != embedded_version:
            mismatches.append(f"Embedded changelog: {embedded_version}")
        
        if mismatches:
            print(f"⚠️  Version mismatch detected:")
            print(f"   Metadata version: {metadata_version}")
            for mismatch in mismatches:
                print(f"   {mismatch}")
            return False
        elif separate_version or embedded_version:
            print(f"✅ Version consistency verified: {metadata_version}")
            return True
        else:
            print("ℹ️  No changelog found. Consider adding a changelog section or file")
            return True


def suggest_changelog_entry(version, changes_type="patch"):
    """Suggest a changelog entry based on version bump type."""
    today = datetime.now().strftime('%Y-%m-%d')
    
    if changes_type == "major":
        return f"## [{version}] - {today}\n\n### Changed\n- Breaking changes (describe what changed)\n\n### Added\n- New features (describe additions)\n\n### Removed\n- Removed features (describe removals)\n"
    elif changes_type == "minor":
        return f"## [{version}] - {today}\n\n### Added\n- New features (describe additions)\n\n### Changed\n- Improvements (describe changes)\n"
    else:  # patch
        return f"## [{version}] - {today}\n\n### Fixed\n- Bug fixes (describe fixes)\n\n### Changed\n- Minor improvements (describe changes)\n"


def main():
    # Valid flags
    valid_flags = {'--auto', '--manual', '--no-auto-update', '--help', '--batch', '--report'}
    
    # Help message
    if '--help' in sys.argv or len(sys.argv) < 2:
        print("Usage: python metadata_validator.py <markdown_file> [--auto] [--manual] [--no-auto-update]")
        print("       python metadata_validator.py --batch <directory> [--auto] [--manual]")
        print("       python metadata_validator.py --report [<directory>]")
        print("       python metadata_validator.py --normalize-dates <changelog_file> [--auto]")
        print("\nModes (choose one):")
        print("  (no flag)      Interactive mode (prompts for all missing/empty fields)")
        print("  --auto         Fill all missing/empty fields with defaults, no prompts")
        print("  --manual       Only report errors, no prompts or auto-fill")
        print("  --batch        Process all markdown files in directory")
        print("  --report       Generate validation report")
        print("  --normalize-dates  Normalize changelog dates to YYYY-MM-DD format")
        print("\nOptions:")
        print("  --no-auto-update    Don't automatically update 'Last Updated' field")
        print("  --help              Show this help message")
        print("\n📅 Date Format:")
        print("  All dates should be in YYYY-MM-DD format (e.g., 2025-07-05)")
        print("  The script will automatically convert common formats like MM/DD/YYYY")
        print("  Changelog dates can be normalized using --normalize-dates")
        sys.exit(0)
    
    # Parse flags
    args = sys.argv[1:]
    flags = set(arg for arg in args if arg.startswith('-'))
    
    # Handle normalize-dates mode
    if '--normalize-dates' in flags:
        # Find the changelog file argument (it's the argument after --normalize-dates)
        changelog_file = None
        for i, arg in enumerate(args):
            if arg == '--normalize-dates' and i + 1 < len(args):
                changelog_file = args[i + 1]
                break
        
        if not changelog_file:
            print("❌ Error: --normalize-dates requires a changelog file path")
            print("Usage: python metadata_validator.py --normalize-dates <changelog_file> [--auto]")
            sys.exit(1)
        
        if not os.path.exists(changelog_file):
            print(f"❌ Changelog file not found: {changelog_file}")
            sys.exit(1)
        
        print(f"📅 Normalizing dates in changelog: {changelog_file}")
        
        # First validate the current format
        validate_changelog_date_format(changelog_file)
        
        # Then normalize dates
        auto_fix = '--auto' in flags
        changes_made = normalize_changelog_dates(changelog_file, auto_fix)
        
        if changes_made and not auto_fix:
            print("\n💡 To apply these changes automatically, run with --auto flag")
        
        sys.exit(0)
    
    # Handle batch mode
    if '--batch' in flags:
        if len(args) < 2 or args[0] == '--batch':
            print("❌ Error: --batch requires a directory path")
            print("Usage: python metadata_validator.py --batch <directory> [--auto] [--manual]")
            sys.exit(1)
        
        batch_dir = args[1] if args[0] == '--batch' else args[0]
        if not os.path.isdir(batch_dir):
            print(f"❌ Directory not found: {batch_dir}")
            sys.exit(1)
        
        print(f"🔍 Batch processing markdown files in: {batch_dir}")
        
        # Find all markdown files
        markdown_files = []
        for root, dirs, files in os.walk(batch_dir):
            # Skip common directories to avoid
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv', 'venv']]
            for file in files:
                if file.endswith('.md'):
                    markdown_files.append(os.path.join(root, file))
        
        if not markdown_files:
            print("❌ No markdown files found in directory")
            sys.exit(1)
        
        print(f"📄 Found {len(markdown_files)} markdown files")
        
        # Process each file
        success_count = 0
        error_count = 0
        
        for md_file in markdown_files:
            print(f"\n{'='*60}")
            print(f"📄 Processing: {md_file}")
            print(f"{'='*60}")
            
            try:
                # Create new args for this file
                file_args = [sys.executable, sys.argv[0], md_file]
                if '--auto' in flags:
                    file_args.append('--auto')
                if '--manual' in flags:
                    file_args.append('--manual')
                if '--no-auto-update' in flags:
                    file_args.append('--no-auto-update')
                
                result = subprocess.run(file_args, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ Success: {md_file}")
                    success_count += 1
                else:
                    print(f"❌ Error: {md_file}")
                    print(f"   {result.stderr}")
                    error_count += 1
                    
            except Exception as e:
                print(f"❌ Exception: {md_file} - {e}")
                error_count += 1
        
        print(f"\n{'='*60}")
        print(f"📊 Batch Processing Complete")
        print(f"✅ Successful: {success_count}")
        print(f"❌ Errors: {error_count}")
        print(f"📄 Total: {len(markdown_files)}")
        print(f"{'='*60}")
        sys.exit(0 if error_count == 0 else 1)
    
    # Handle report mode
    if '--report' in flags:
        report_dir = args[0] if len(args) > 0 and not args[0].startswith('-') else '.'
        if not os.path.isdir(report_dir):
            print(f"❌ Directory not found: {report_dir}")
            sys.exit(1)
        
        print(f"📊 Generating validation report for: {report_dir}")
        
        # Find all markdown files
        markdown_files = []
        for root, dirs, files in os.walk(report_dir):
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv', 'venv']]
            for file in files:
                if file.endswith('.md'):
                    markdown_files.append(os.path.join(root, file))
        
        if not markdown_files:
            print("❌ No markdown files found in directory")
            sys.exit(1)
        
        print(f"📄 Found {len(markdown_files)} markdown files")
        print(f"\n📋 Validation Report")
        print(f"{'='*60}")
        
        total_files = len(markdown_files)
        valid_files = 0
        invalid_files = 0
        missing_metadata = 0
        
        for md_file in markdown_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                metadata, block_start, block_end = extract_metadata_block(lines)
                
                if block_start is None:
                    print(f"❌ {md_file}: No metadata block found")
                    missing_metadata += 1
                    invalid_files += 1
                else:
                    errors = validate_metadata(metadata)
                    if errors:
                        print(f"⚠️  {md_file}: {len(errors)} validation errors")
                        for error in errors:
                            print(f"   - {error}")
                        invalid_files += 1
                    else:
                        print(f"✅ {md_file}: Valid metadata")
                        valid_files += 1
                        
            except Exception as e:
                print(f"❌ {md_file}: Error reading file - {e}")
                invalid_files += 1
        
        print(f"\n{'='*60}")
        print(f"📊 Summary")
        print(f"✅ Valid files: {valid_files}")
        print(f"⚠️  Invalid files: {invalid_files}")
        print(f"❌ Missing metadata: {missing_metadata}")
        print(f"📄 Total files: {total_files}")
        print(f"📈 Success rate: {(valid_files/total_files)*100:.1f}%")
        print(f"{'='*60}")
        sys.exit(0)
    
    # Regular single file mode
    md_path = args[0]
    
    # Strict flag validation
    for flag in flags:
        if flag not in valid_flags:
            print(f"Error: Unrecognized option '{flag}'.")
            print("Use --help to see available options.")
            sys.exit(1)
    # Mutually exclusive check
    if '--auto' in flags and '--manual' in flags:
        print("Error: --auto and --manual cannot be used together. Please choose only one mode.")
        sys.exit(1)
    auto_mode = '--auto' in flags
    manual_mode = '--manual' in flags
    auto_update = '--no-auto-update' not in flags
    
    if not os.path.isfile(md_path):
        print(f"❌ File not found: {md_path}")
        wait_for_user_exit()
        sys.exit(1)
    
    print(f"🔍 Validating metadata for: {md_path}")
    print("📅 Note: All dates should be in YYYY-MM-DD format (e.g., 2025-07-05)")
    if INITIAL_TIMEOUT is None:
        print("⏱️  Timeout settings: DISABLED (no timeouts)")
    else:
        print(f"⏱️  Timeout settings: {INITIAL_TIMEOUT}s initial, {GENTLE_PROMPT_DELAY}s gentle prompt, {FINAL_TIMEOUT}s final")
    print()
    
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        wait_for_user_exit()
        sys.exit(1)
    
    metadata, block_start, block_end = extract_metadata_block(lines)
    today = datetime.now().strftime('%Y-%m-%d')
    updates = {}
    
    # --- ENHANCED DEFAULT FOR DOCUMENT TITLE ---
    doc_title_default = None
    if 'Document Title' not in metadata or not metadata['Document Title']:
        heading = extract_first_heading(lines, block_end if block_end is not None else -1)
        if heading:
            doc_title_default = heading
        else:
            doc_title_default = prettify_filename(md_path)
    else:
        doc_title_default = metadata['Document Title']

    # --- DATE FORMAT NORMALIZATION ---
    print("📅 Checking and normalizing date formats...")
    for date_field in ['Created', 'Last Updated']:
        if date_field in metadata and metadata[date_field]:
            original_date = metadata[date_field]
            normalized_date, was_changed, original_format = normalize_date_format(original_date)
            
            if was_changed:
                if auto_mode:
                    updates[date_field] = normalized_date
                    print(f"✅ Auto-converted '{date_field}' from '{original_date}' to '{normalized_date}' (auto mode)")
                elif manual_mode:
                    print(f"⚠️  '{date_field}' has non-standard format '{original_date}' (should be YYYY-MM-DD)")
                else:
                    # Interactive mode - ask for confirmation
                    final_date = confirm_date_interpretation(original_date, normalized_date, original_format)
                    if final_date != original_date:
                        updates[date_field] = final_date
                        print(f"✅ Converted '{date_field}' from '{original_date}' to '{final_date}'")
    
    # --- EARLY DATE CHECK/UPDATE ---
    print("📅 Checking for missing or invalid date fields...")
    for date_field in ['Created', 'Last Updated']:
        if date_field not in metadata or not metadata[date_field] or not re.fullmatch(ISO_DATE_PATTERN, metadata[date_field]):
            if auto_mode:
                updates[date_field] = today
                print(f"✅ Auto-filled '{date_field}' with {today} (auto mode)")
            elif manual_mode:
                continue  # Only report, do not prompt or fill
            else:
                val = prompt_field(date_field, today, auto_mode)
                if val:
                    updates[date_field] = val
                    print(f"✅ Filled '{date_field}' with {val}")
                else:
                    print(f"❌ You chose not to fill '{date_field}'. Please update manually.")
                    wait_for_user_exit()
                    sys.exit(1)
    
    # --- AUTO-UPDATE LOGIC (FIXED) ---
    if auto_update and not manual_mode:  # Don't auto-update in manual mode
        # Only update 'Last Updated' if it's missing, invalid, or not today's date
        # AND if the user didn't just enter today's date in the previous step
        if (
            'Last Updated' not in metadata
            or not re.fullmatch(ISO_DATE_PATTERN, metadata['Last Updated'])
            or (metadata['Last Updated'] != today and 'Last Updated' not in updates)
        ):
            print(f"🔄 Auto-updating 'Last Updated' to today's date ({today}).")
            updates['Last Updated'] = today
        elif 'Last Updated' in updates and updates['Last Updated'] == today:
            print(f"✅ 'Last Updated' already set to today's date ({today}) by user input.")
    elif manual_mode and auto_update:
        print("ℹ️  Manual mode: Skipping auto-update of 'Last Updated' field.")
    
    # --- Handle all other required fields ---
    for field in REQUIRED_FIELDS:
        if field in ['Created', 'Last Updated']:
            continue
        if field not in metadata or not metadata[field]:
            if field == 'Document Title':
                default = doc_title_default or DEFAULTS.get(field, '')
            else:
                default = today if field in ['Created', 'Last Updated'] else DEFAULTS.get(field, '')
            if auto_mode:
                updates[field] = default
                print(f"✅ Auto-filled '{field}' with '{default}' (auto mode)")
            elif manual_mode:
                continue  # Only report, do not prompt or fill
            else:
                val = prompt_field(field, default, auto_mode)
                if val:
                    updates[field] = val
                    print(f"✅ Filled '{field}' with '{val}'")
                else:
                    print(f"❌ You chose not to fill '{field}'. Please update manually.")
                    wait_for_user_exit()
                    sys.exit(1)
    
    if updates:
        try:
            new_lines = update_metadata_block(lines, metadata, block_start, block_end, updates)
            with open(md_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print("✅ Metadata block updated with new value(s). Re-running validator to complete validation...")
            # Automatically re-run the validator on the same file
            args = [sys.executable, sys.argv[0], md_path]
            if not auto_update:
                args.append('--no-auto-update')
            if auto_mode:
                args.append('--auto')
            if manual_mode:
                args.append('--manual')
            subprocess.run(args)
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error updating file: {e}")
            wait_for_user_exit()
            sys.exit(1)
    
    # --- END EARLY DATE CHECK/UPDATE ---
    print("🔍 Running full metadata validation...")
    errors = validate_metadata(metadata)
    if errors:
        print("❌ Metadata validation errors:")
        for err in errors:
            print(f"  - {err}")
        print("\nPlease update the metadata block and re-run the validator.")
        display_metadata(metadata)
        wait_for_user_exit()
        sys.exit(1)
    print("✅ Metadata validation passed!")
    display_metadata(metadata)
    
    # --- CHANGELOG CONSISTENCY CHECK ---
    if 'Version' in metadata and metadata['Version']:
        print("\n📋 Checking changelog consistency...")
        file_directory = os.path.dirname(os.path.abspath(md_path))
        changelog_consistent = check_changelog_consistency(metadata['Version'], md_path, file_directory)
        
        # Check changelog date format if separate changelog exists
        changelog_path = find_changelog_file(file_directory)
        if changelog_path:
            print("📅 Checking changelog date formats...")
            date_format_ok = validate_changelog_date_format(changelog_path)
            if not date_format_ok and not manual_mode:
                print("💡 To normalize changelog dates, run:")
                print(f"   python {sys.argv[0]} --normalize-dates {changelog_path} --auto")
        
        if not changelog_consistent and not manual_mode:
            print("\n💡 Changelog suggestion:")
            print("Consider updating your changelog to match the metadata version.")
            
            # Get placement recommendation
            placement_info = suggest_changelog_placement(md_path)
            print(f"\n📍 Recommended placement: {placement_info['position']}")
            print(f"📝 Suggested heading level: {placement_info['heading_level']}")
            
            print("\n📋 You can add a new entry like this:")
            print(suggest_changelog_entry(metadata['Version']))
            
            print("\n📖 Example structure for this document type:")
            print(placement_info['example'])
    
    wait_for_user_exit()


def prompt_field(field, default=None, auto_mode=False):
    prompt = f"Field '{field}' is missing or empty. Enter a value"
    if default:
        prompt += f" [default: {default}]"
    prompt += ": "
    
    # Add format instruction for date fields
    if field in ['Created', 'Last Updated']:
        prompt += f"\n(Use YYYY-MM-DD format, e.g., {default} for today)"
    if field == 'Document Title':
        prompt += "\n(If left blank, the script will use the first heading or filename as the title.)"
    prompt += "\n(Press Enter to accept the default, or type your value.)\n"
    
    timeout_input = TimeoutInput(INITIAL_TIMEOUT, GENTLE_PROMPT_DELAY, FINAL_TIMEOUT)
    resp = timeout_input.get_input_with_timeout(prompt)
    if resp is None or resp.strip() == '':
        return default
    
    user_input = resp.strip()
    
    # Normalize date formats for date fields
    if field in ['Created', 'Last Updated']:
        normalized_date, was_changed, original_format = normalize_date_format(user_input)
        if was_changed:
            print(f"📅 Detected date format '{original_format}': {user_input}")
            print(f"📅 Converting to YYYY-MM-DD format: {normalized_date}")
            
            if not auto_mode:  # Only ask for confirmation in interactive mode
                confirm_prompt = f"Is this correct? [Y/n]: "
                timeout_input = TimeoutInput(INITIAL_TIMEOUT, GENTLE_PROMPT_DELAY, FINAL_TIMEOUT)
                confirm_resp = timeout_input.get_input_with_timeout(confirm_prompt)
                if confirm_resp is None:
                    print("Timeout reached. Using original input as-is.")
                    return user_input
                
                confirm_resp = confirm_resp.strip().lower()
                if confirm_resp in ('', 'y', 'yes'):
                    print(f"✅ Using normalized date: {normalized_date}")
                    return normalized_date
                else:
                    print(f"✅ Using original input: {user_input}")
                    return user_input
            else:
                # Auto mode - use normalized date
                return normalized_date
    
    return user_input


if __name__ == "__main__":
    main() 