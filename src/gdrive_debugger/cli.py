import typer
from rich.console import Console
from rich.panel import Panel
from typing import Optional

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

from gdrive_debugger.errors import handle_drive_error
from gdrive_debugger.logger import get_logger

logger = get_logger()
console = Console()

app = typer.Typer(
    name="gdrive-debugger",
    help="Debug and automate Google Drive operations with rich diagnostics.",
    add_completion=False,
)

# Global state for dry-run
state = {"dry_run": False}


def version_callback(value: bool):
    if value:
        console.print(f"gdrive-debugger v{__version__}")
        raise typer.Exit()


def dry_run_callback(ctx: typer.Context, param: typer.CallbackParam, value: bool):
    if value:
        state["dry_run"] = True
        console.print("[yellow]⚠️  DRY-RUN MODE ENABLED — No changes will be made.[/yellow]")
    return value


@app.callback()
def main(
    ctx: typer.Context,
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-n",
        help="Run in dry-run mode (no actual changes)",
        callback=dry_run_callback,
        is_eager=True,
    ),
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
):
    """gdrive-debugger CLI"""
    ctx.obj = state


auth_app = typer.Typer(help="Authentication commands")
app.add_typer(auth_app, name="auth")

debug_app = typer.Typer(help="Debugging & inspection commands")
app.add_typer(debug_app, name="debug")

permissions_app = typer.Typer(help="Permission analysis")
app.add_typer(permissions_app, name="permissions")


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
    """Login via Google OAuth."""
    try:
        do_login()
        console.print("[bold green]✓ Successfully authenticated![/bold green]")
        logger.info("User logged in successfully")
    except Exception as e:
        handle_drive_error(e)


@auth_app.command("status")
def auth_status():
    """Check authentication status."""
    creds = get_credentials()
    if creds and creds.valid:
        console.print("[bold green]✓ Authenticated[/bold green]")
    else:
        console.print("[yellow]Not authenticated. Run 'gdrive-debugger auth login'[/yellow]")


# ==================== DEBUG ====================

@debug_app.command("file")
def debug_file(file_id: str):
    """Show detailed metadata for a file/folder."""
    try:
        service = get_drive_service()
        file = get_file_metadata(service, file_id)
        display_file_info(file)
        logger.info(f"Debugged file: {file_id}")
    except Exception as e:
        handle_drive_error(e)


@debug_app.command("folder")
def debug_folder(folder_id: str, limit: int = 20):
    """List contents of a folder."""
    try:
        service = get_drive_service()
        folder = get_file_metadata(service, folder_id)
        console.print(f"[bold cyan]Folder:[/bold cyan] {folder.get('name')}")

        results = service.files().list(
            q=f"'{folder_id}' in parents",
            pageSize=limit,
            fields="files(id, name, mimeType, modifiedTime)",
        ).execute()

        files = results.get("files", [])
        if not files:
            console.print("[yellow]Folder is empty.[/yellow]")
            return

        from rich.table import Table
        table = Table(title="Folder Contents")
        table.add_column("Name", style="cyan")
        table.add_column("Type")
        for f in files:
            table.add_row(f.get("name"), f.get("mimeType", ""))
        console.print(table)
        logger.info(f"Listed folder {folder_id} ({len(files)} items)")
    except Exception as e:
        handle_drive_error(e)


@debug_app.command("list")
def debug_list(folder_id: str = "root", limit: int = 30):
    """List files in a folder (default: root)."""
    try:
        service = get_drive_service()
        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            pageSize=limit,
            fields="files(id, name, mimeType)",
        ).execute()
        files = results.get("files", [])

        from rich.table import Table
        table = Table(title=f"Contents of {folder_id}")
        table.add_column("Name")
        table.add_column("Type")
        for f in files:
            table.add_row(f["name"], f.get("mimeType", ""))
        console.print(table)
    except Exception as e:
        handle_drive_error(e)


@debug_app.command("search")
def debug_search(query: str, limit: int = 20):
    """Search files by name."""
    try:
        service = get_drive_service()
        results = service.files().list(
            q=f"name contains '{query}' and trashed=false",
            pageSize=limit,
            fields="files(id, name, mimeType)",
        ).execute()
        files = results.get("files", [])
        if not files:
            console.print("[yellow]No results found.[/yellow]")
            return

        from rich.table import Table
        table = Table(title=f"Search: {query}")
        table.add_column("Name", style="cyan")
        table.add_column("ID", style="dim")
        for f in files:
            table.add_row(f["name"], f["id"])
        console.print(table)
        logger.info(f"Search performed: {query} ({len(files)} results)")
    except Exception as e:
        handle_drive_error(e)


@debug_app.command("changes")
def debug_changes(limit: int = 20):
    """Show recent changes."""
    try:
        service = get_drive_service()
        changes = get_recent_changes(service, limit=limit)
        display_changes(changes)
    except Exception as e:
        handle_drive_error(e)


@debug_app.command("quota")
def debug_quota():
    """Show storage quota."""
    try:
        service = get_drive_service()
        about = get_quota(service)
        display_quota(about)
    except Exception as e:
        handle_drive_error(e)


# ==================== PERMISSIONS ====================

@permissions_app.command("analyze")
def permissions_analyze(file_id: str):
    """Analyze permissions of a file/folder."""
    try:
        service = get_drive_service()
        perms = get_permissions(service, file_id)
        display_permissions(perms)
        logger.info(f"Analyzed permissions for {file_id}")
    except Exception as e:
        handle_drive_error(e)


if __name__ == "__main__":
    app()