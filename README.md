# gdrive-debugger

**Debug and automate Google Drive operations like a professional.**

A modern Python CLI + library that provides deep visibility, beautiful diagnostics, structured logging, and safe automation helpers for Google Drive.

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/akhilsgdrive-debug/gdrive-debugger?style=social)](https://github.com/akhilsgdrive-debug/gdrive-debugger/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/akhilsgdrive-debug/gdrive-debugger)](https://github.com/akhilsgdrive-debug/gdrive-debugger/issues)

---

## The Problem It Solves

Working with the Google Drive API can be frustrating:

- Cryptic error messages with little context
- Difficult permission and sharing debugging
- No built-in visibility into what your code is actually doing
- Risky bulk operations without dry-run support
- Scattered logging that is hard to analyze

**gdrive-debugger** gives you professional-grade observability and control so you can debug faster and automate safely.

## ✨ Key Features

- 🔍 **Rich Debugging Commands** — Inspect files, permissions, metadata, and recent changes with beautiful formatted output
- 📊 **Structured Logging** — JSON + human-readable logs for every Drive API call
- 🛡️ **Safe Automation** — Built-in dry-run mode, confirmations, and batch operation helpers
- 🎨 **Beautiful Terminal Experience** — Powered by [Typer](https://typer.tiangolo.com/) + [Rich](https://rich.readthedocs.io/)
- 🔑 **Flexible Authentication** — Supports both OAuth 2.0 and Service Accounts
- 🧩 **Library + CLI** — Use it as a command-line tool **or** import it directly in your Python scripts
- 💡 **Actionable Error Insights** — Common Drive errors explained with suggested fixes

## Tech Stack

- **Python** 3.9+
- **Typer** + **Rich** (modern CLI & stunning terminal UI)
- **google-api-python-client** + **google-auth**
- **Pydantic** v2 for data validation
- Clean, type-hinted codebase

## Quick Start

### Installation

```bash
pip install gdrive-debugger
```

Or install from source:

```bash
git clone https://github.com/akhilsgdrive-debug/gdrive-debugger.git
cd gdrive-debugger
pip install -e .
```

### First-time Setup

```bash
# Login with your Google account (OAuth)
gdrive-debugger auth login

# Or use a service account
# gdrive-debugger auth service-account --credentials path/to/service-account.json
```

## Usage Examples

### Debug a specific file

```bash
gdrive-debugger debug file --id 1AbCdefGhiJKlmnOp
```

### Check and analyze permissions

```bash
gdrive-debugger permissions analyze --file-id 1AbCdefGhiJKlmnOp
```

### View recent changes with explanations

```bash
gdrive-debugger changes recent --limit 15
```

### Safe bulk operations (dry-run first)

```bash
gdrive-debugger automation move \
  --source-folder "MyFolder" \
  --destination-folder "Archive" \
  --dry-run
```

## Screenshots & Demo

> **Coming soon** — Real terminal recordings and screenshots will be added.

Placeholder for beautiful CLI output.

## Roadmap

- [x] Core CLI structure & authentication
- [ ] File & permission debugging commands
- [ ] Structured logging system
- [ ] Dry-run safe automation helpers
- [ ] Actionable error explanations
- [ ] Export logs (JSON / CSV)
- [ ] PyPI package release
- [ ] Comprehensive documentation site
- [ ] Community recipes & examples

## Contributing

We welcome contributions!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

Please make sure to follow the code style and add tests where appropriate.

## Show Your Support

If **gdrive-debugger** helps you debug Google Drive issues faster or makes your automation safer, please consider giving it a ⭐ **star** on GitHub!

Stars help others discover the project and keep the momentum going.

---

**Built with care by [Akhil](https://github.com/akhilsgdrive-debug)**

*Making Google Drive development more transparent and enjoyable.*