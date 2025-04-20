# config-crafter
config-crafter

A utility for modifying YAML configuration files while preserving formatting, indentation, and comments.

## Overview

The YAML Updater Tool provides a solution for programmatically updating YAML files without disturbing the existing structure, indentation patterns, or comments. This is particularly useful for automation tasks where configuration files need to be modified in a safe and predictable manner.

## Features

- Preserves all comments in the YAML file
- Maintains original indentation patterns
- Creates automatic backups of files before modification
- Supports targeted modifications to specific sections
- Handles nested YAML structures

## Installation

### Prerequisites

- Python 3.6 or higher
- Required Python packages:
  - `re` (standard library)
  - `sys` (standard library)
  - `os` (standard library)

### Setup

1. Save the script to a file named `yaml_updater.py`
2. Ensure the script has execution permissions:

```bash
chmod +x yaml_updater.py
```

## Implementation Details

The tool uses regular expressions to find specific sections in the YAML file and make targeted modifications. This approach is preferable to using YAML parsers when preserving exact formatting is critical, as most YAML parsers will normalize indentation and formatting when rewriting the file.

### How It Works

1. The tool reads the entire YAML file into memory
2. It uses regex patterns to locate the specific section that needs modification
3. It determines the existing indentation pattern from nearby lines
4. It creates a new line or section with matching indentation
5. It replaces the old section with the updated version
6. It writes the modified content back to the file

## Error Handling

Each function returns a boolean indicating success or failure. If a function cannot find the specified section to modify, it will return `False`.

## Backup System

The tool creates backup files (with `.bak` extension) before making changes when the `backup` parameter is set to `True`. This allows for easy recovery if modifications don't work as expected.

## Limitations

- The regex patterns are designed for specific YAML structures. You may need to adjust them for significantly different YAML formats.
- The tool assumes consistent indentation within each section.
- Very complex YAML structures might require additional pattern matching.


