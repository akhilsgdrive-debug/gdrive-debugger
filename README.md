# gdrive-debugger

**Debug and automate Google Drive operations like a professional.**

A modern Python CLI + library that provides deep visibility, beautiful diagnostics, structured logging, and safe automation helpers for Google Drive.

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/akhilsgdrive-debug/gdrive-debugger?style=social)](https://github.com/akhilsgdrive-debug/gdrive-debugger/stargazers)

---

## The Problem It Solves

Working with the Google Drive API can be frustrating:

- Cryptic error messages with little context
- Difficult permission and sharing debugging
- No built-in visibility into what your code is actually doing
- Risky bulk operations without dry-run support

**gdrive-debugger** gives you professional-grade observability and control.

## ✨ Key Features

- 🔐 **Easy OAuth Login** — `gdrive-debugger auth login` (opens browser)
- 🔍 **Rich File Debugging** — Inspect metadata, owners, links with beautiful tables
- 🔎 **Permission Analyzer** — See exactly who has access and what role
- 🎨 **Beautiful Terminal UI** — Powered by Typer + Rich
- 🧩 **Usable as Library** — Import in your own scripts
- 🛡️ **Safe by Design** — Clear errors + future dry-run support

## Tech Stack

- Python 3.9+
- Typer + Rich
- google-api-python-client + google-auth + google-auth-oauthlib
- Pydantic

## Quick Start

### 1. Installation

```bash
pip install gdrive-debugger
```

Or from source:

```bash
git clone https://github.com/akhilsgdrive-debug/gdrive-debugger.git
cd gdrive-debugger
pip install -e .
```

### 2. Get Google Cloud Credentials (One-time setup)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the **Google Drive API**
4. Go to **APIs & Services → Credentials** → **+ Create Credentials** → **OAuth client ID** (choose **Desktop app**)
5. Download the `credentials.json` file
6. Place it here: `~/.config/gdrive-debugger/credentials.json`

### 3. Authenticate

```bash
gdrive-debugger auth login
```

This opens your browser for Google sign-in.

## Usage Examples

### Check if you're logged in

```bash
gdrive-debugger auth status
```

### Debug a specific file

```bash
gdrive-debugger debug file 1AbCdefGhiJKlmnOpQrStUv
```

### Analyze permissions of a file or folder

```bash
gdrive-debugger permissions analyze 1AbCdefGhiJKlmnOpQrStUv
```

## Roadmap

- [x] OAuth authentication (`auth login` + `auth status`)
- [x] File metadata debugging (`debug file`)
- [x] Permission analysis (`permissions analyze`)
- [ ] Structured logging system
- [ ] Dry-run mode for safe automation
- [ ] More commands (recent changes, quota insights, bulk helpers)
- [ ] Publish to PyPI
- [ ] Full documentation site

## Contributing

We welcome contributions! Feel free to open issues or pull requests.

## Show Your Support

If **gdrive-debugger** helps you debug Google Drive faster, please consider giving it a ⭐ **star**!

Stars help others discover the project.

---

**Built with care by [Akhil](https://github.com/akhilsgdrive-debug)**