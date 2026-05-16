import typer
from rich.console import Console
from rich.panel import Panel

from gdrive_debugger import __version__
from gdrive_debugger.auth import login as do_login, get_credentials, get_drive_service
try:
    from gdrive_debugger.drive import (
        get_file_metadata,
        get_permissions,
        display_file_info,
        display_permissions,
    )
except ImportError:
    pass

app = typer.Typer(
    name="gdrive-debugger",
    help="Debug and automate Google Drive operations with rich diagnostics.",
    add_completion=False,
)
console = Console()

auth_app = typer.Typer(help="Authentication commands")
app.add_typer(auth_app, name="auth")

debug_app = typer.Typer(help="Debugging commands")
app.add_typer(debug_app, name="debug")

permissions_app = typer.Typer(help="Permission analysis commands")
app.add_typer(permissions_app, name="permissions")


@app.command()
def version():
    """Show current version."""
    console.print(f"gdrive-debugger v{__version__}")


@app.command()
def hello():
    """Quick hello to verify installation."""
    console.print(Panel.fit(
        "[bold green]Hello from gdrive-debugger![/bold green]\n\n"
        "Your Google Drive debugging toolkit is ready.",
        title="Welcome",
        border_style="green",
    ))


# ==================== AUTH COMMANDS ====================

@auth_app.command("login")
def auth_login():
    """Login with Google OAuth (opens browser)."""
    try:
        creds = do_login()
        console.print("[bold green]✓ Successfully authenticated![/bold green]")
        console.print("Token saved to ~/.config/gdrive-debugger/token.json")
    except FileNotFoundError as e:
        console.print(f"[red]{e}[/red]")
        console.print(
            "\n[bold]How to get credentials.json:[/bold]\n"
            "1. Go to https://console.cloud.google.com/\n"
            "2. Create a project and enable Google Drive API\n"
            "3. Create OAuth 2.0 Client ID (Desktop app)\n"
            "4. Download credentials.json and place it in ~/.config/gdrive-debugger/"
        )
    except Exception as e:
        console.print(f"[red]Login failed: {e}[/red]")


@auth_app.command("status")
def auth_status():
    """Check current authentication status."""
    creds = get_credentials()
    if creds and creds.valid:
        console.print("[bold green]✓ Authenticated[/bold green]")
    else:
        console.print("[yellow]Not authenticated. Run 'gdrive-debugger auth login'[/yellow]")


# ==================== DEBUG COMMANDS ====================

@debug_app.command("file")
def debug_file(file_id: str = typer.Argument(..., help="Google Drive file ID")):
    """Debug and display detailed information about a file."""
    try:
        service = get_drive_service()
        file = get_file_metadata(service, file_id)
        display_file_info(file)
        console.print(f"\n[bold]Direct link:[/bold] {file.get('webViewLink', 'N/A')}")
    except Exception as e:
        console.print(f"[red]Failed to debug file: {e}[/red]")


# ==================== PERMISSIONS COMMANDS ====================

@permissions_app.command("analyze")
def permissions_analyze(
    file_id: str = typer.Argument(..., help="Google Drive file ID"),
):
    """Analyze permissions of a file/folder."""
    try:
        service = get_drive_service()
        perms = get_permissions(service, file_id)
        display_permissions(perms)
        console.print(f"\n[bold cyan]Total permissions:[/bold cyan] {len(perms)}")
    except Exception as e:
        console.print(f"[red]Failed to analyze permissions: {e}[/red]")


if __name__ == "__main__":
    app()