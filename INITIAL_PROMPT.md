# Convert SSH 'Host' Config Entries to iTerm2 Dynamic Profiles

## Gist

I want a python (>3.8 is fine) utility that converts OpenSSH 'Host" config entries into iTerm2 dynamic profiles.

## Functional Requirements

- As "hands off" as possible. It should use all common sense defaults for file paths. 
- It needs to be aware of ssh config includes. All includes must be fully resolved before creating the dynamic profiles.
- Single-file or multi-file target :
  - Either all profiles are created in a single "profiles.json" file or each profile is created in its own json file 
  - Defaults to single file, overrideable via CLI switch
- All profiles need to have a parent profile 
  - The parent should "Default" by default
  - Overrideable via CLI switch
- Verbose output, informing the user of what it is doing at all times 
  - Ask the user for his OK before writing the JSON output file(s)
    - Overrideable via CLI switch

## Stack requirements

- Python, 3.8+
- Standard library, no additional dependencies
- Argparse for CLI switches

## Other requirements

- Clean code, divide steps in functions (avoid a gigantic MAIN block)
- All functions should reside in a single file in order to simplify distribution
- Code for clarity rather than cleverness
- Performance is not importante, clarity is

## Next Steps

- Propose a development plan, document it in PLAN.md
- Discuss plan with me before coding anything