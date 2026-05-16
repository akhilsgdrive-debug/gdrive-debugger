# gdrive-debugger

**Debug Google Drive with confidence.**

A clean, powerful Python CLI for inspecting files, permissions, changes, and quota — with beautiful output, helpful error suggestions, and structured logging.

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

- Global `--dry-run` flag
- Rich file/folder inspection
- Permission analysis
- Recent changes & quota
- Smart error suggestions
- Structured logging (JSON + console)
- Beautiful terminal experience

## Installation

```bash
pip install gdrive-debugger
```

## Quick Start

```bash
gdrive-debugger auth login
gdrive-debugger debug file <ID>
gdrive-debugger debug folder <FOLDER_ID>
gdrive-debugger debug search "report"
gdrive-debugger permissions analyze <ID>
```

## Commands

**Auth**
- `auth login`
- `auth status`

**Debug**
- `debug file <ID>`
- `debug folder <ID>`
- `debug list`
- `debug search <query>`
- `debug changes`
- `debug quota`

**Permissions**
- `permissions analyze <ID>`

**Global Flag**
- `--dry-run` / `-n` — Safe mode (no changes)

## Roadmap

- Full structured logging integration
- More automation commands with dry-run
- PyPI release

## Contributing

Contributions welcome!

## Support

If this tool helps you debug Google Drive, please ⭐ **star** the repository!

---

**Created by [Akhil](https://github.com/akhilsgdrive-debug)**