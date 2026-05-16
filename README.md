# gdrive-debugger

**Debug and automate Google Drive like a pro.**

A powerful Python CLI + library for deep visibility into Google Drive operations, beautiful diagnostics, and safe automation.

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/akhilsgdrive-debug/gdrive-debugger?style=social)](https://github.com/akhilsgdrive-debug/gdrive-debugger/stargazers)

---

## Why gdrive-debugger?

Google Drive API debugging is painful. Cryptic errors, hidden permission issues, and no visibility into what’s happening.

**gdrive-debugger** gives you:

- Crystal clear file & permission insights
- Recent change history
- Quota visibility
- Beautiful terminal experience

## ✨ Current Commands

| Command                              | Description                              |
|--------------------------------------|------------------------------------------|
| `gdrive-debugger auth login`         | OAuth login (opens browser)              |
| `gdrive-debugger auth status`        | Check authentication status              |
| `gdrive-debugger debug file <ID>`    | Detailed file/folder metadata            |
| `gdrive-debugger debug changes`      | Show recent Drive changes                |
| `gdrive-debugger debug quota`        | View storage quota & usage               |
| `gdrive-debugger permissions analyze <ID>` | Analyze who has access              |

## Quick Start

### Installation

```bash
pip install gdrive-debugger
```

### One-time Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable **Google Drive API**
3. Create **OAuth 2.0 Client ID** (Desktop app)
4. Download `credentials.json`
5. Save it to `~/.config/gdrive-debugger/credentials.json`

### Login & Use

```bash
gdrive-debugger auth login
gdrive-debugger debug file YOUR_FILE_ID
gdrive-debugger permissions analyze YOUR_FILE_ID
gdrive-debugger debug changes --limit 30
gdrive-debugger debug quota
```

## Roadmap

- [x] Authentication
- [x] File debugging
- [x] Permission analysis
- [x] Recent changes
- [x] Quota inspection
- [ ] Structured logging
- [ ] Dry-run automation helpers
- [ ] PyPI release

## Contributing

Contributions are welcome!

## Show Your Support

If this tool saves you time debugging Google Drive, please ⭐ **star** it!

---

**Created by [Akhil](https://github.com/akhilsgdrive-debug)**