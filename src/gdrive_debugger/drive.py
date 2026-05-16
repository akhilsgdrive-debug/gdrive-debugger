"""Google Drive service helpers with rich output."""

from typing import Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def get_file_metadata(service, file_id: str) -> dict[str, Any]:
    """Fetch detailed file metadata."""
    try:
        return (
            service.files()
            .get(
                fileId=file_id,
                fields="id,name,mimeType,size,createdTime,modifiedTime,owners,parents,webViewLink,iconLink,shared,trashed",
            )
            .execute()
        )
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise


def get_permissions(service, file_id: str) -> list[dict]:
    """Fetch permissions for a file/folder."""
    try:
        result = (
            service.permissions()
            .list(
                fileId=file_id,
                fields="permissions(id,type,role,emailAddress,displayName,domain)",
            )
            .execute()
        )
        return result.get("permissions", [])
    except Exception as e:
        console.print(f"[red]Error fetching permissions: {e}[/red]")
        raise


def get_recent_changes(service, limit: int = 20) -> list[dict]:
    """Get recent changes in Drive."""
    try:
        changes = (
            service.changes()
            .list(
                pageToken=None,
                pageSize=limit,
                fields="changes(fileId,file(name,mimeType,modifiedTime),time)",
            )
            .execute()
        )
        return changes.get("changes", [])
    except Exception as e:
        console.print(f"[red]Error fetching changes: {e}[/red]")
        raise


def get_quota(service) -> dict[str, Any]:
    """Get storage quota information."""
    try:
        about = service.about().get(fields="storageQuota,user").execute()
        return about
    except Exception as e:
        console.print(f"[red]Error fetching quota: {e}[/red]")
        raise


def display_file_info(file: dict) -> None:
    """Pretty print file metadata."""
    table = Table(title=f"📄 File: {file.get('name', 'Unknown')}", show_header=True)
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    important_fields = ["id", "name", "mimeType", "size", "createdTime", "modifiedTime", "webViewLink", "shared", "trashed"]
    for key in important_fields:
        if key in file and file[key] is not None:
            table.add_row(key, str(file[key]))

    console.print(table)

    if file.get("owners"):
        console.print(Panel.fit(str(file["owners"]), title="👤 Owners", border_style="blue"))


def display_permissions(permissions: list[dict]) -> None:
    """Display permissions in a clean table."""
    if not permissions:
        console.print("[yellow]No permissions found.[/yellow]")
        return

    table = Table(title="🔐 Permissions", show_header=True)
    table.add_column("Type", style="cyan")
    table.add_column("Role", style="magenta")
    table.add_column("Email / Name", style="green")
    table.add_column("Domain", style="yellow")

    for p in permissions:
        table.add_row(
            p.get("type", "-"),
            p.get("role", "-"),
            p.get("emailAddress") or p.get("displayName", "-"),
            p.get("domain", "-"),
        )
    console.print(table)


def display_changes(changes: list[dict]) -> None:
    """Display recent changes."""
    if not changes:
        console.print("[yellow]No recent changes found.[/yellow]")
        return

    table = Table(title="📜 Recent Changes", show_header=True)
    table.add_column("Time", style="dim")
    table.add_column("File", style="cyan")
    table.add_column("Type", style="green")

    for change in changes:
        file = change.get("file", {})
        table.add_row(
            change.get("time", "-")[:19],
            file.get("name", "(deleted or unknown)")[:40],
            file.get("mimeType", "-"),
        )
    console.print(table)


def display_quota(about: dict) -> None:
    """Display storage quota nicely."""
    quota = about.get("storageQuota", {})
    user = about.get("user", {})

    console.print(Panel.fit(
        f"[bold]User:[/bold] {user.get('displayName', 'Unknown')} ({user.get('emailAddress', '')})\n\n"
        f"[bold]Storage Used:[/bold] {quota.get('usage', 'N/A')} bytes\n"
        f"[bold]Limit:[/bold] {quota.get('limit', 'N/A')} bytes\n"
        f"[bold]Trash:[/bold] {quota.get('usageInTrash', 'N/A')} bytes",
        title="💾 Google Drive Quota",
        border_style="green",
    ))