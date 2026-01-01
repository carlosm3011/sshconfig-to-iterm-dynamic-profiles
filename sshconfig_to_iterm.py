#!/usr/bin/env python3
"""
SSH Config to iTerm2 Dynamic Profiles Converter

Converts OpenSSH Host entries to iTerm2 dynamic profile JSON files.
Supports Include directives and generates profiles with minimal configuration.

Usage:
    python3 sshconfig_to_iterm.py [options]

For more information, use --help
"""

import argparse
import json
import os
import glob
import uuid
import sys
from pathlib import Path
from typing import List, Dict, Optional, Set


# Version information
VERSION = "1.0.0"
RELEASE_DATE = "2026-01-01"
PROGRAM_NAME = "SSH Config to iTerm2 Dynamic Profiles Converter"


# --- SSH Config Parsing Functions ---

def expand_path(path: str) -> str:
    """
    Expand ~ and environment variables in path.

    Args:
        path: Path string that may contain ~ or environment variables

    Returns:
        Fully expanded absolute path
    """
    expanded = os.path.expanduser(path)
    expanded = os.path.expandvars(expanded)
    return os.path.abspath(expanded)


def resolve_includes(include_line: str, current_dir: str) -> List[str]:
    """
    Resolve Include directive to list of file paths.
    Handles glob patterns and relative paths.

    Args:
        include_line: The Include directive value (e.g., "~/.ssh/config.d/*")
        current_dir: Directory of the current config file for resolving relative paths

    Returns:
        List of resolved file paths
    """
    # Remove leading/trailing whitespace
    pattern = include_line.strip()

    # Remove surrounding quotes (single or double)
    if (pattern.startswith('"') and pattern.endswith('"')) or \
       (pattern.startswith("'") and pattern.endswith("'")):
        pattern = pattern[1:-1]

    # Handle ~ expansion
    pattern = os.path.expanduser(pattern)

    # If relative path, make it relative to current_dir
    if not os.path.isabs(pattern):
        pattern = os.path.join(current_dir, pattern)

    # Expand glob pattern
    matches = glob.glob(pattern)

    # Return sorted list of existing files
    return sorted([f for f in matches if os.path.isfile(f)])


def parse_config_file(file_path: str, visited: Set[str], verbose: bool = True) -> List[Dict]:
    """
    Parse a single SSH config file.

    Args:
        file_path: Path to the SSH config file
        visited: Set of already-visited file paths (prevents circular includes)
        verbose: Whether to print verbose output

    Returns:
        List of host dictionaries, each containing 'name' and optionally other config
    """
    file_path = os.path.abspath(file_path)

    # Check for circular includes
    if file_path in visited:
        if verbose:
            print(f"  Warning: Skipping already-visited file: {file_path}")
        return []

    visited.add(file_path)

    if not os.path.exists(file_path):
        if verbose:
            print(f"  Warning: Config file not found: {file_path}")
        return []

    if verbose:
        print(f"  Parsing: {file_path}")

    hosts = []
    current_dir = os.path.dirname(file_path)

    try:
        with open(file_path, 'r') as f:
            for line in f:
                # Remove leading/trailing whitespace
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue

                # Split into tokens (handle multiple spaces/tabs)
                tokens = line.split()
                if not tokens:
                    continue

                keyword = tokens[0].lower()

                # Handle Include directive
                if keyword == 'include':
                    if len(tokens) < 2:
                        continue
                    include_pattern = ' '.join(tokens[1:])
                    included_files = resolve_includes(include_pattern, current_dir)

                    if verbose and included_files:
                        print(f"    Include directive resolved to {len(included_files)} file(s)")

                    # Recursively parse included files
                    for inc_file in included_files:
                        hosts.extend(parse_config_file(inc_file, visited, verbose))

                # Handle Host directive
                elif keyword == 'host':
                    if len(tokens) < 2:
                        continue

                    # Get host name (can have multiple, space-separated)
                    host_names = tokens[1:]

                    # Create entry for each host pattern
                    for host_name in host_names:
                        # Skip wildcard-only entries
                        if host_name == '*':
                            continue

                        hosts.append({
                            'name': host_name
                        })

    except Exception as e:
        if verbose:
            print(f"  Error reading {file_path}: {e}")

    return hosts


def parse_ssh_config(config_path: str, verbose: bool = True) -> List[Dict]:
    """
    Main entry point for SSH config parsing.
    Handles the initial config file and all includes.

    Args:
        config_path: Path to the main SSH config file
        verbose: Whether to print verbose output

    Returns:
        List of host dictionaries
    """
    visited: Set[str] = set()
    return parse_config_file(config_path, visited, verbose)


# --- Profile Generation Functions ---

def generate_guid() -> str:
    """
    Generate a unique GUID for profile.

    Returns:
        UUID string in uppercase format
    """
    return str(uuid.uuid4()).upper()


def create_profile(host_name: str, parent_profile: str) -> Dict:
    """
    Create a single iTerm2 profile dictionary.

    Args:
        host_name: Name of the SSH host
        parent_profile: Name of the parent iTerm2 profile

    Returns:
        Profile dictionary with iTerm2 format
    """
    return {
        "Name": host_name,
        "Guid": generate_guid(),
        "Dynamic Profile Parent Name": parent_profile,
        "Custom Command": "Yes",
        "Command": f"ssh {host_name}",
        "Tags": ["ssh"]
    }


def generate_profiles(hosts: List[Dict], parent_profile: str) -> List[Dict]:
    """
    Generate iTerm2 profiles from host list.

    Args:
        hosts: List of host dictionaries from SSH config
        parent_profile: Name of the parent iTerm2 profile

    Returns:
        List of iTerm2 profile dictionaries
    """
    profiles = []
    for host in hosts:
        profile = create_profile(host['name'], parent_profile)
        profiles.append(profile)
    return profiles


# --- Output Functions ---

def write_single_file(profiles: List[Dict], output_path: str, verbose: bool = True) -> None:
    """
    Write all profiles to a single JSON file.

    Args:
        profiles: List of profile dictionaries
        output_path: Path to output JSON file
        verbose: Whether to print verbose output
    """
    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Create the iTerm2 dynamic profiles structure
    output = {
        "Profiles": profiles
    }

    # Write JSON file
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    if verbose:
        print(f"\nWrote {len(profiles)} profile(s) to: {output_path}")


def write_multi_file(profiles: List[Dict], output_dir: str, verbose: bool = True) -> None:
    """
    Write each profile to its own JSON file.

    Args:
        profiles: List of profile dictionaries
        output_dir: Directory to write profile files
        verbose: Whether to print verbose output
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for profile in profiles:
        # Create filename from profile name (sanitize for filesystem)
        filename = profile['Name'].replace('/', '_').replace('*', 'wildcard')
        filepath = os.path.join(output_dir, f"{filename}.json")

        # Create the iTerm2 dynamic profiles structure
        output = {
            "Profiles": [profile]
        }

        # Write JSON file
        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2)

        if verbose:
            print(f"  Wrote: {filepath}")

    if verbose:
        print(f"\nWrote {len(profiles)} profile(s) to: {output_dir}")


# --- CLI and Main Functions ---

def print_verbose(message: str, verbose: bool = True) -> None:
    """
    Print message if verbose mode is enabled.

    Args:
        message: Message to print
        verbose: Whether verbose mode is enabled
    """
    if verbose:
        print(message)


def confirm_write(profiles: List[Dict]) -> bool:
    """
    Ask user for confirmation before writing.

    Args:
        profiles: List of profiles that will be written

    Returns:
        True if user confirms, False otherwise
    """
    print(f"\nReady to write {len(profiles)} profile(s).")
    response = input("Proceed? [Y/n]: ").strip().lower()
    return response in ('', 'y', 'yes')


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description='Convert SSH config Host entries to iTerm2 dynamic profiles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
  %(prog)s --config ~/.ssh/work_config
  %(prog)s --multi-file --output-dir ~/profiles
  %(prog)s --parent-profile "My Theme" --yes
        """
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'{PROGRAM_NAME}\nVersion: {VERSION}\nRelease Date: {RELEASE_DATE}'
    )

    parser.add_argument(
        '--config',
        default=os.path.expanduser('~/.ssh/config'),
        help='Path to SSH config file (default: ~/.ssh/config)'
    )

    parser.add_argument(
        '--output-dir',
        default=os.path.expanduser('~/Library/Application Support/iTerm2/DynamicProfiles'),
        help='Output directory for profile files (default: ~/Library/Application Support/iTerm2/DynamicProfiles)'
    )

    output_mode = parser.add_mutually_exclusive_group()
    output_mode.add_argument(
        '--single-file',
        action='store_true',
        default=True,
        help='Write all profiles to a single file (default)'
    )
    output_mode.add_argument(
        '--multi-file',
        action='store_true',
        help='Write each profile to its own file'
    )

    parser.add_argument(
        '--parent-profile',
        default='Default',
        help='Parent profile name for all generated profiles (default: Default)'
    )

    parser.add_argument(
        '-y', '--yes',
        action='store_true',
        help='Skip confirmation prompt'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=True,
        help='Enable verbose output (default: enabled)'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Disable verbose output'
    )

    return parser.parse_args()


def main() -> None:
    """
    Main entry point.
    Orchestrates the parsing, generation, and output process.
    """
    args = parse_arguments()

    # Handle verbose/quiet flags
    verbose = args.verbose and not args.quiet

    # Print banner
    print_verbose("=" * 60, verbose)
    print_verbose("SSH Config to iTerm2 Dynamic Profiles Converter", verbose)
    print_verbose("=" * 60, verbose)

    # Expand paths
    config_path = expand_path(args.config)
    output_dir = expand_path(args.output_dir)

    # Show configuration
    print_verbose(f"\nConfiguration:", verbose)
    print_verbose(f"  SSH config: {config_path}", verbose)
    print_verbose(f"  Output directory: {output_dir}", verbose)
    print_verbose(f"  Output mode: {'single-file' if not args.multi_file else 'multi-file'}", verbose)
    print_verbose(f"  Parent profile: {args.parent_profile}", verbose)

    # Check if config file exists
    if not os.path.exists(config_path):
        print(f"\nError: SSH config file not found: {config_path}")
        sys.exit(1)

    # Parse SSH config
    print_verbose(f"\nParsing SSH config...", verbose)
    hosts = parse_ssh_config(config_path, verbose)

    if not hosts:
        print("\nNo Host entries found in SSH config.")
        sys.exit(0)

    print_verbose(f"\nFound {len(hosts)} Host entries:", verbose)
    if verbose:
        for i, host in enumerate(hosts, 1):
            print(f"  {i}. {host['name']}")

    # Generate profiles
    print_verbose(f"\nGenerating iTerm2 profiles...", verbose)
    profiles = generate_profiles(hosts, args.parent_profile)

    # Ask for confirmation unless --yes flag is used
    if not args.yes:
        if not confirm_write(profiles):
            print("\nCancelled by user.")
            sys.exit(0)

    # Write output
    print_verbose("\nWriting profiles...", verbose)

    if args.multi_file:
        write_multi_file(profiles, output_dir, verbose)
    else:
        output_path = os.path.join(output_dir, 'ssh-hosts.json')
        write_single_file(profiles, output_path, verbose)

    print_verbose("\nDone!", verbose)
    print_verbose("=" * 60, verbose)


if __name__ == "__main__":
    main()
