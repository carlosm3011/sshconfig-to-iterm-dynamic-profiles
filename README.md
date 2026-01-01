# SSH Config to iTerm2 Dynamic Profiles Converter

A simple Python utility that converts OpenSSH `Host` config entries to iTerm2 dynamic profiles. Uses only Python 3.8+ and the standard library - no external dependencies required.

## Features

- Automatically parses your SSH config file
- Resolves `Include` directives (including glob patterns)
- Generates iTerm2 dynamic profiles with sensible defaults
- Supports both single-file and multi-file output modes
- Verbose output shows exactly what's happening
- Confirmation prompt before writing files (can be skipped with `--yes`)
- Fully customizable via command-line options

## Installation

1. Clone this repository or download `sshconfig_to_iterm.py`
2. Make it executable: `chmod +x sshconfig_to_iterm.py`
3. Run it: `./sshconfig_to_iterm.py`

Or simply run with Python:
```bash
python3 sshconfig_to_iterm.py
```

## Usage

### Basic Usage (with defaults)

```bash
python3 sshconfig_to_iterm.py
```

This will:
- Read your SSH config from `~/.ssh/config`
- Generate iTerm2 profiles for all `Host` entries
- Output to `~/Library/Application Support/iTerm2/DynamicProfiles/ssh-hosts.json`
- Use "Default" as the parent profile
- Show verbose output
- Ask for confirmation before writing

### Command-Line Options

```
--config CONFIG              Path to SSH config file (default: ~/.ssh/config)
--output-dir OUTPUT_DIR      Output directory for profile files
--single-file                Write all profiles to a single file (default)
--multi-file                 Write each profile to its own file
--parent-profile PROFILE     Parent profile name (default: Default)
-y, --yes                    Skip confirmation prompt
-v, --verbose                Enable verbose output (default: enabled)
-q, --quiet                  Disable verbose output
-h, --help                   Show help message
```

### Examples

**Use a non-standard SSH config location:**
```bash
python3 sshconfig_to_iterm.py --config ~/.ssh/work_config
```

**Generate multi-file output:**
```bash
python3 sshconfig_to_iterm.py --multi-file --output-dir ~/my-profiles
```

**Use a custom parent profile:**
```bash
python3 sshconfig_to_iterm.py --parent-profile "My Custom Theme"
```

**Automated mode (no confirmation):**
```bash
python3 sshconfig_to_iterm.py --yes
```

**Quiet mode:**
```bash
python3 sshconfig_to_iterm.py --quiet --yes
```

## How It Works

1. **Parses SSH Config**: Reads your SSH config file and resolves all `Include` directives
2. **Extracts Host Entries**: Identifies all `Host` entries (skips wildcards like `*`)
3. **Generates Profiles**: Creates iTerm2 dynamic profile JSON for each host
4. **Writes Output**: Saves profiles to the iTerm2 DynamicProfiles directory

Each generated profile:
- Uses the SSH host name as the profile name
- Inherits from your chosen parent profile (for colors, fonts, etc.)
- Runs `ssh <hostname>` when launched (SSH handles all connection details)
- Is tagged with "ssh" for easy filtering in iTerm2

## iTerm2 Dynamic Profiles

iTerm2 will automatically detect and load profiles from:
```
~/Library/Application Support/iTerm2/DynamicProfiles/
```

After running this tool, your new SSH profiles will appear in iTerm2's profile menu. They'll inherit all settings (colors, fonts, etc.) from the parent profile you specified.

## Requirements

- Python 3.8 or higher
- macOS with iTerm2
- An SSH config file with `Host` entries

## Example SSH Config

```ssh
Host production-server
    HostName prod.example.com
    User admin
    Port 2222

Host staging
    HostName staging.example.com
    User deploy

Include ~/.ssh/config.d/*
```

This will generate iTerm2 profiles named "production-server" and "staging", plus any hosts from included files.

## Troubleshooting

**No profiles generated:**
- Make sure your SSH config has `Host` entries (not just `Match`)
- Check that the config file path is correct with `--config`
- Try running with `--verbose` to see what's being parsed

**iTerm2 doesn't show the profiles:**
- Check that files are in `~/Library/Application Support/iTerm2/DynamicProfiles/`
- Restart iTerm2
- Verify the JSON is valid (should be well-formed)

**Include directives not working:**
- Make sure the paths in `Include` statements are correct
- Use absolute paths or paths relative to the config file location
- Check file permissions on included files

## Support

If you find this tool useful, consider buying me a coffee!

[![Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/carlos_cagnazzo)

## License

BSD 3-Clause - see LICENSE file for details
