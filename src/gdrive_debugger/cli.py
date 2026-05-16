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

from gdrive_debugger.errors import handle_drive_error

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
    """Login via Google OAuth."""
    try:
        do_login()
        console.print("[bold green]✓ Successfully authenticated![/bold green]")
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
def debug_file(file_id: str = typer.Argument(..., help="File or folder ID")):
    """Show detailed metadata for a file/folder."""
    try:
        service = get_drive_service()
        file = get_file_metadata(service, file_id)
        display_file_info(file)
    except Exception as e:
        handle_drive_error(e)


@debug_app.command("folder")
def debug_folder(
    folder_id: str = typer.Argument(..., help="Folder ID"),
    limit: int = typer.Option(20, "--limit", help="Max items to show"),
):
    """List contents of a folder."""
    try:
        service = get_drive_service()
        # Reuse file metadata + list children
        folder = get_file_metadata(service, folder_id)
        console.print(f"[bold]Folder:[/bold] {folder.get('name')}")

        # List children
        results = (
            service.files()
            .list(
                q=f"'{folder_id}' in parents",
                pageSize=limit,
                fields="files(id, name, mimeType, modifiedTime)",
            )
            .execute()
        )
        files = results.get("files", [])

        if not files:
            console.print("[yellow]Folder is empty.[/yellow]")
            return

        from rich.table import Table
        table = Table(title="Folder Contents")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Modified", style="dim")

        for f in files:
            table.add_row(f.get("name"), f.get("mimeType"), f.get("modifiedTime", "")[:10])
        console.print(table)
    except Exception as e:
        handle_drive_error(e)


@debug_app.command("changes")
def debug_changes(limit: int = typer.Option(20, help="Number of changes")):
    """Show recent changes in Drive."""
    try:
        service = get_drive_service()
        changes = get_recent_changes(service, limit=limit)
        from gdrive_debugger.drive import display_changes
        display_changes(changes)
    except Exception as e:
        handle_drive_error(e)


@debug_app.command("quota")
def debug_quota():
    """Show storage quota."""
    try:
        service = get_drive_service()
        about = get_quota(service)
        from gdrive_debugger.drive import display_quota
        display_quota(about)
    except Exception as e:
        handle_drive_error(e)


@debug_app.command("list")
def debug_list(
    folder_id: str = typer.Option("root", help="Folder ID (default: root)"),
    limit: int = typer.Option(30, help="Max results"),
):
    """List files in a folder (default: My Drive root)."""
    try:
        service = get_drive_service()
        results = (
            service.files()
            .list(
                q=f"'{folder_id}' in parents and trashed=false",
                pageSize=limit,
                fields="files(id, name, mimeType, modifiedTime)",
            )
            .execute()
        )
        files = results.get("files", [])

        from rich.table import Table
        table = Table(title=f"Files in {folder_id}")
        table.add_column("Name")
        table.add_column("Type")
        for f in files:
            table.add_row(f["name"], f.get("mimeType", ""))
        console.print(table)
    except Exception as e:
        handle_drive_error(e)


@debug_app.command("search")
def debug_search(
    query: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(20, help="Max results"),
):
    """Search for files by name."""
    try:
        service = get_drive_service()
        results = (
            service.files()
            .list(
                q=f"name contains '{query}' and trashed=false",
                pageSize=limit,
                fields="files(id, name, mimeType, modifiedTime)",
            )
            .execute()
        )
        files = results.get("files", [])
        if not files:
            console.print("[yellow]No results found.[/yellow]")
            return

        from rich.table import Table
        table = Table(title=f"Search results for: {query}")
        table.add_column("Name", style="cyan")
        table.add_column("ID", style="dim")
        for f in files:
            table.add_row(f["name"], f["id"])
        console.print(table)
    except Exception as e:
        handle_drive_error(e)


# ==================== PERMISSIONS ====================

@permissions_app.command("analyze")
def permissions_analyze(file_id: str = typer.Argument(..., help="File/folder ID")):
    """Analyze permissions."""
    try:
        service = get_drive_service()
        perms = get_permissions(service, file_id)
        from gdrive_debugger.drive import display_permissions
        display_permissions(perms)
    except Exception as e:
        handle_drive_error(e)


if __name__ == "__main__":
    app()