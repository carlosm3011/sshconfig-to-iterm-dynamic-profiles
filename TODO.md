# Future Features and Ideas

This document tracks potential enhancements and feature ideas for the SSH Config to iTerm2 Dynamic Profiles Converter.

## Planned Features

### Include-Based Profile Grouping

**Description:** When resolving Include directives, group all profiles from each included file into a separate JSON file.

**Current Behavior:** All profiles (from main config and includes) are written to a single JSON file or separate files per profile.

**Proposed Behavior:**
- Profiles from `~/.ssh/config` → `ssh_config_profiles.json`
- Profiles from `~/.ssh/ssh-hosts.cfg` → `ssh_hosts_cfg_profiles.json`
- Profiles from `~/.ssh/work/hosts` → `work_hosts_profiles.json`

**Benefits:**
- Better organization in iTerm2's profile list
- Easier to manage profiles by source
- Can selectively enable/disable groups by renaming files
- Clearer provenance of each profile

**Implementation Notes:**
- Track source file for each host during parsing
- Create separate output file per source file
- Sanitize filenames (replace `/` with `_`, handle special characters)
- Update `write_single_file()` or add new output mode

### Hierarchical Profile Tagging

**Description:** Use iTerm2's profile tagging feature to create hierarchical tags based on include file name and host name.

**Current Behavior:** All profiles get a simple "ssh" tag.

**Proposed Behavior:**
- Profiles from main config: `ssh/config/<hostname>`
- Profiles from includes: `ssh/<include-filename>/<hostname>`
- Example: `ssh/ssh-hosts.cfg/production-server`
- Example: `ssh/work-hosts/database-01`

**Benefits:**
- Clear visual hierarchy in iTerm2
- Easy filtering by source file
- Better organization for large SSH configurations
- Quick identification of profile source

**Implementation Notes:**
- Parse Include filename (basename without path)
- Sanitize filename for tag use (replace dots, spaces)
- Update `create_profile()` to add hierarchical tags to `Tags` array
- iTerm2 tag format: tags are just strings, hierarchy is visual via `/`
- Example tag array: `["ssh", "ssh/ssh-hosts.cfg", "ssh/ssh-hosts.cfg/hostname"]`

## Nice to Have

(Future ideas can be added here)

## Under Consideration

(Ideas being evaluated can be added here)

---

*Last updated: January 1, 2026*
