"""Authentication module for gdrive-debugger."""

import json
import os
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/drive"]

CONFIG_DIR = Path.home() / ".config" / "gdrive-debugger"
TOKEN_FILE = CONFIG_DIR / "token.json"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"


def get_credentials() -> Credentials | None:
    """Load credentials from token file if available."""
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        if creds and creds.valid:
            return creds
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            save_credentials(creds)
            return creds
    return None


def save_credentials(creds: Credentials) -> None:
    """Save credentials to token file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_FILE, "w") as token:
        token.write(creds.to_json())


def login() -> Credentials:
    """Perform OAuth login flow."""
    if not CREDENTIALS_FILE.exists():
        raise FileNotFoundError(
            f"credentials.json not found at {CREDENTIALS_FILE}\n"
            "Please download it from Google Cloud Console and place it there."
        )

    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    save_credentials(creds)
    return creds


def get_drive_service():
    """Get authenticated Google Drive service."""
    from googleapiclient.discovery import build

    creds = get_credentials()
    if not creds:
        raise RuntimeError("Not authenticated. Run 'gdrive-debugger auth login' first.")

    return build("drive", "v3", credentials=creds)