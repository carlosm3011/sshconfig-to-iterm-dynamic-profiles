# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Version information display**: Added `--version` switch to display program name, version number, and release date. Version information is stored as constants (`VERSION`, `RELEASE_DATE`, `PROGRAM_NAME`) at the top of the script for easy maintenance.

### Fixed
- **Include directive with quoted paths not being resolved**: Fixed bug where Include directives with quoted paths (e.g., `Include "/path/to/file"`) were not being processed correctly. The quotes were being treated as part of the filename, causing the file resolution to fail. The `resolve_includes()` function now strips surrounding single or double quotes from Include paths before processing them. This fix enables proper parsing of SSH configs that use quoted Include paths, which is common in OpenSSH configurations.
  - Impact: Users with quoted Include paths would have missing Host entries from included files
  - Resolution: Added quote stripping logic in `resolve_includes()` function (line 56-59)
  - Test case: Include directive like `Include "/Users/user/.ssh/ssh-hosts.cfg"` now correctly resolves

## [1.0.0] - 2026-01-01

### Added
- Initial release of SSH Config to iTerm2 Dynamic Profiles Converter
- Parse OpenSSH config files and extract Host entries
- Support for Include directives with glob pattern expansion
- Recursive Include resolution with circular reference prevention
- Generate iTerm2 dynamic profile JSON format
- Single-file output mode (all profiles in one JSON file)
- Multi-file output mode (one JSON file per profile)
- Command-line interface with argparse
- Configurable SSH config path via `--config` option
- Configurable output directory via `--output-dir` option
- Configurable parent profile via `--parent-profile` option
- Verbose output mode (enabled by default)
- Quiet mode via `--quiet` flag
- Confirmation prompt before writing files
- Skip confirmation with `--yes` flag
- Automatic path expansion for ~ and environment variables
- Single-file implementation (no external dependencies)
- Python 3.8+ support using only standard library
- Comprehensive documentation in README.md
- Development plan documentation in PLAN.md
- MIT License

### Features
- Skips wildcard-only Host entries (`Host *`)
- Generates unique GUIDs for each profile
- Tags all profiles with "ssh" for easy filtering
- Inherits settings from parent profile
- Uses simple `ssh <hostname>` command (SSH config handles connection details)
- Handles relative and absolute Include paths
- Supports both `/path/to/file` and `~/path/to/file` syntax
- Pretty-printed JSON output with 2-space indentation
