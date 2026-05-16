import typer
from rich.console import Console
from rich.panel import Panel

from gdrive_debugger import __version__
from gdrive_debugger.auth import login as do_login, get_credentials, get_drive_service
try:
    from gdrive_debugger.drive import (
        get_file_metadata,
        get_permissions,
        get_recent_changes,
        get_quota,
        display_file_info,
        display_permissions,
        display_changes,
        display_quota,
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

debug_app = typer.Typer(help="Debugging & inspection commands")
app.add_typer(debug_app, name="debug")

permissions_app = typer.Typer(help="Permission analysis")
app.add_typer(permissions_app, name="permissions")


@app.command()
def version():
    """Show current version."""
    console.print(f"gdrive-debugger v{__version__}")


@app.command()
def hello():
    """Quick hello command."""
    console.print(Panel.fit(
        "[bold green]Hello from gdrive-debugger![/bold green]\n\n"
        "Your Google Drive debugging toolkit is ready.",
        title="Welcome",
        border_style="green",
    ))


# ==================== AUTH ====================

@auth_app.command("login")
def auth_login():
    """Login via Google OAuth (opens browser)."""
    try:
        do_login()
        console.print("[bold green]✓ Successfully authenticated![/bold green]")
        console.print("Credentials saved to ~/.config/gdrive-debugger/token.json")
    except FileNotFoundError as e:
        console.print(f"[red]{e}[/red]")
        console.print(
            "\n[bold yellow]Setup Instructions:[/bold yellow]\n"
            "1. Go to https://console.cloud.google.com/\n"
            "2. Enable Google Drive API\n"
            "3. Create OAuth 2.0 Client ID (Desktop app)\n"
            "4. Download credentials.json\n"
            "5. Place it at ~/.config/gdrive-debugger/credentials.json"
        )
    except Exception as e:
        console.print(f"[red]Login failed: {e}[/red]")


@auth_app.command("status")
def auth_status():
    """Check authentication status."""
    creds = get_credentials()
    if creds and creds.valid:
        console.print("[bold green]✓ You are authenticated[/bold green]")
    else:
        console.print("[yellow]Not authenticated. Run 'gdrive-debugger auth login'[/yellow]")


# ==================== DEBUG ====================

@debug_app.command("file")
def debug_file(file_id: str = typer.Argument(..., help="Google Drive file/folder ID")):
    """Show detailed metadata for a file or folder."""
    try:
        service = get_drive_service()
        file = get_file_metadata(service, file_id)
        display_file_info(file)
    except Exception as e:
        console.print(f"[red]Failed: {e}[/red]")


@debug_app.command("changes")
def debug_changes(
    limit: int = typer.Option(20, "--limit", "-l", help="Number of changes to show"),
):
    """Show recent changes in your Drive."""
    try:
        service = get_drive_service()
        changes = get_recent_changes(service, limit=limit)
        display_changes(changes)
        console.print(f"\n[dim]Showing last {len(changes)} changes[/dim]")
    except Exception as e:
        console.print(f"[red]Failed to fetch changes: {e}[/red]")


@debug_app.command("quota")
def debug_quota():
    """Show your Google Drive storage quota."""
    try:
        service = get_drive_service()
        about = get_quota(service)
        display_quota(about)
    except Exception as e:
        console.print(f"[red]Failed to fetch quota: {e}[/red]")


# ==================== PERMISSIONS ====================

@permissions_app.command("analyze")
def permissions_analyze(file_id: str = typer.Argument(..., help="File or folder ID")):
    """Analyze who has access to a file/folder."""
    try:
        service = get_drive_service()
        perms = get_permissions(service, file_id)
        display_permissions(perms)
        console.print(f"\n[bold cyan]Total permissions found:[/bold cyan] {len(perms)}")
    except Exception as e:
        console.print(f"[red]Failed: {e}[/red]")


if __name__ == "__main__":
    app()