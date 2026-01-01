# Development Plan: SSH Config to iTerm2 Dynamic Profiles Converter

## Overview
Create a Python utility (3.8+) that parses OpenSSH config files and generates iTerm2 dynamic profile JSON files. Single-file implementation for easy distribution.

## Architecture

### Single File Structure (`sshconfig_to_iterm.py`)

All functionality in one file, organized into clear functions:

1. **SSH Config Parsing Functions**
   - `parse_ssh_config(config_path)` - Main parser entry point
   - `resolve_includes(include_line, current_dir)` - Handle Include directives
   - `parse_config_file(file_path)` - Parse individual config file
   - `expand_path(path)` - Handle ~ and variable expansion

2. **Profile Generation Functions**
   - `generate_profiles(hosts, parent_profile)` - Convert hosts to profiles
   - `create_profile(host_name, parent_profile)` - Create single profile dict
   - `generate_guid()` - Create unique GUID for profiles

3. **Output Functions**
   - `write_single_file(profiles, output_path)` - Write all profiles to one JSON
   - `write_multi_file(profiles, output_dir)` - Write individual JSON files

4. **CLI and Main Functions**
   - `parse_arguments()` - Setup argparse and return args
   - `print_verbose(message, verbose)` - Conditional verbose output
   - `confirm_write(profiles)` - Ask user for confirmation
   - `main()` - Orchestrate the entire flow

### File Structure
```
sshconfig-to-iterm-dynamic-profiles/
├── sshconfig_to_iterm.py          # Single file with all functionality
├── README.md                      # Usage documentation
├── LICENSE
└── .gitignore
```

## Implementation Steps

### Phase 1: SSH Config Parser Functions
1. **Parse single SSH config file**
   - `parse_config_file()`: Read file line by line
   - Identify `Host` entries
   - Extract host-specific configuration (HostName, Port, User, etc.)
   - Skip comments and empty lines
   - Return list of host dictionaries

2. **Handle Include directives**
   - `resolve_includes()`: Detect `Include` statements
   - Resolve relative/absolute paths with `expand_path()`
   - Handle glob patterns (e.g., `~/.ssh/config.d/*`)
   - `parse_ssh_config()`: Recursively parse included files
   - Prevent circular includes

3. **Default paths**
   - Primary: `~/.ssh/config`
   - Handle missing files gracefully

### Phase 2: iTerm2 Profile Generator Functions
1. **Research iTerm2 dynamic profile format**
   - Understand required fields
   - Understand parent profile mechanism
   - Map SSH config to iTerm2 properties

2. **Generate profile JSON**
   - `generate_guid()`: Create unique GUID using uuid module
   - `create_profile()`: Build profile dict with:
     - Profile name from Host entry
     - Parent profile reference
     - Command to launch SSH connection
   - `generate_profiles()`: Process all hosts

3. **Output modes**
   - `write_single_file()`: Array of profiles in one JSON file
   - `write_multi_file()`: Individual `<hostname>.json` files

### Phase 3: CLI Integration
1. **Argument parsing** (`parse_arguments()`)
   - `--config`: Override SSH config path (default: `~/.ssh/config`)
   - `--output-dir`: Specify output directory for profiles
   - `--single-file` / `--multi-file`: Output mode (default: single-file)
   - `--parent-profile`: Override parent profile (default: "Default")
   - `--yes` / `-y`: Skip confirmation prompt
   - `--verbose` / `-v`: Verbose output (default: on)

2. **User interaction flow** (`main()`)
   - Display banner/intro
   - Show detected SSH config path
   - Parse and display found hosts
   - Preview output plan
   - Ask for confirmation via `confirm_write()` (unless --yes)
   - Write output files
   - Display success summary

3. **Verbose output** (`print_verbose()`)
   - Log each major step
   - Show files being parsed
   - List hosts found
   - Show include resolution
   - Report file writes

### Phase 4: Testing & Documentation
1. **Manual testing**
   - Test with simple config
   - Test with includes
   - Test with nested includes
   - Test both output modes
   - Verify iTerm2 can load profiles

2. **README documentation**
   - Installation instructions
   - Usage examples
   - CLI options reference
   - iTerm2 dynamic profiles location
   - Troubleshooting

## Code Organization in Single File

```python
#!/usr/bin/env python3
"""
SSH Config to iTerm2 Dynamic Profiles Converter
Converts OpenSSH Host entries to iTerm2 dynamic profile JSON files
"""

import argparse
import json
import os
import glob
import uuid
from pathlib import Path
from typing import List, Dict, Optional

# --- SSH Config Parsing Functions ---
def expand_path(path: str) -> str:
    """Expand ~ and environment variables in path"""
    pass

def resolve_includes(include_line: str, current_dir: str) -> List[str]:
    """Resolve Include directive to list of file paths"""
    pass

def parse_config_file(file_path: str, visited: set) -> List[Dict]:
    """Parse a single SSH config file"""
    pass

def parse_ssh_config(config_path: str) -> List[Dict]:
    """Main entry point for SSH config parsing"""
    pass

# --- Profile Generation Functions ---
def generate_guid() -> str:
    """Generate a unique GUID for profile"""
    pass

def create_profile(host_name: str, parent_profile: str) -> Dict:
    """Create a single iTerm2 profile dictionary"""
    pass

def generate_profiles(hosts: List[Dict], parent_profile: str) -> List[Dict]:
    """Generate iTerm2 profiles from host list"""
    pass

# --- Output Functions ---
def write_single_file(profiles: List[Dict], output_path: str) -> None:
    """Write all profiles to a single JSON file"""
    pass

def write_multi_file(profiles: List[Dict], output_dir: str) -> None:
    """Write each profile to its own JSON file"""
    pass

# --- CLI and Main Functions ---
def print_verbose(message: str, verbose: bool = True) -> None:
    """Print message if verbose mode is enabled"""
    pass

def confirm_write(profiles: List[Dict]) -> bool:
    """Ask user for confirmation before writing"""
    pass

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    pass

def main() -> None:
    """Main entry point"""
    pass

if __name__ == "__main__":
    main()
```

## Key Design Decisions

### SSH Config Parsing
- Use standard library only (no `paramiko` or external parsers)
- Simple line-by-line parsing sufficient for our needs
- Focus on `Host` entries (ignore `Match` initially)
- Store minimal config: Host, HostName, Port, User

### iTerm2 Profile Mapping
- Profile Name = SSH Host entry name
- Command = `ssh <host>` (let SSH handle the config)
- Parent Profile = "Default" (ensures consistent theme/settings)
- Minimal profile (rely on parent for styling)

### Default Behavior
- Look for `~/.ssh/config`
- Output to `~/Library/Application Support/iTerm2/DynamicProfiles/ssh-hosts.json`
- Single-file mode
- Verbose output enabled
- Require user confirmation

### Error Handling
- Gracefully handle missing SSH config
- Warn on unreadable included files
- Validate output directory writability
- Provide clear error messages

## Implementation Notes

### iTerm2 Dynamic Profile Structure
```json
{
  "Profiles": [
    {
      "Name": "production-server",
      "Guid": "unique-guid-here",
      "Dynamic Profile Parent Name": "Default",
      "Custom Command": "Yes",
      "Command": "ssh production-server",
      "Initial Text": "",
      "Tags": ["ssh"]
    }
  ]
}
```

### SSH Config Considerations
- Host entries can use wildcards (*, ?) - keep them as-is
- Only process valid Host entries (skip `Match`)
- Preserve original host name for SSH to resolve
- Handle `~` expansion in Include paths

## Future Enhancements (Out of Scope)
- GUI interface
- Watch mode (auto-update on config changes)
- Custom profile templates
- Badge/tag customization
- Match directive support
- Integration with SSH key management

## Success Criteria
- ✓ Parses standard SSH config files
- ✓ Resolves Include directives correctly
- ✓ Generates valid iTerm2 dynamic profiles
- ✓ Provides clear, verbose output
- ✓ Works with default paths out-of-box
- ✓ Asks for confirmation before writing
- ✓ No external dependencies
- ✓ Clean, readable code in single file
- ✓ Easy to distribute and run
