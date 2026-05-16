# gdrive-debugger

**Debug and inspect Google Drive with confidence.**

A modern Python CLI that gives you deep visibility into files, permissions, changes, and quota — with beautiful output and helpful error suggestions.

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![PyPI](https://img.shields.io/badge/PyPI-coming_soon-orange.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Features

- 🔐 Easy OAuth authentication
- 📄 Rich file & folder inspection
- 🔍 Powerful search
- 🔐 Permission analysis
- 📜 Recent changes history
- 💾 Quota & storage insights
- 🧠 Actionable error suggestions
- 📊 Structured logging (JSON + pretty console)

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
gdrive-debugger debug quota
```

## Available Commands

**Auth**
- `auth login` — Login with Google
- `auth status` — Check login status

**Debug**
- `debug file <ID>`
- `debug folder <ID>`
- `debug list [--folder]`
- `debug search <query>`
- `debug changes`
- `debug quota`

**Permissions**
- `permissions analyze <ID>`

## Roadmap

- Structured logging (in progress)
- Dry-run mode for automation
- More error intelligence
- PyPI release

## Contributing

PRs and issues are welcome!

## Support

If this tool helps you, please ⭐ star the repo!

---

**Built by [Akhil](https://github.com/akhilsgdrive-debug)**