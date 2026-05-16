"""Google Drive service helpers."""

from typing import Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def get_file_metadata(service, file_id: str) -> dict[str, Any]:
    """Fetch file metadata from Drive."""
    try:
        file = (
            service.files()
            .get(
                fileId=file_id,
                fields="id, name, mimeType, size, createdTime, modifiedTime, owners, parents, webViewLink, iconLink",
            )
            .execute()
        )
        return file
    except Exception as e:
        console.print(f"[red]Error fetching file: {e}[/red]")
        raise


def get_permissions(service, file_id: str) -> list[dict]:
    """Fetch permissions for a file."""
    try:
        permissions = (
            service.permissions()
            .list(
                fileId=file_id,
                fields="permissions(id, type, role, emailAddress, displayName, domain)",
            )
            .execute()
        )
        return permissions.get("permissions", [])
    except Exception as e:
        console.print(f"[red]Error fetching permissions: {e}[/red]")
        raise


def display_file_info(file: dict) -> None:
    """Pretty print file metadata using Rich."""
    table = Table(title=f"File: {file.get('name', 'Unknown')}", show_header=True)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    for key in ["id", "name", "mimeType", "size", "createdTime", "modifiedTime", "webViewLink"]:
        if key in file:
            table.add_row(key, str(file[key]))

    console.print(table)

    if "owners" in file:
        owners = file["owners"]
        console.print(Panel.fit(str(owners), title="Owners"))


def display_permissions(permissions: list[dict]) -> None:
    """Display permissions in a nice table."""
    if not permissions:
        console.print("[yellow]No permissions found.[/yellow]")
        return

    table = Table(title="Permissions", show_header=True)
    table.add_column("Type", style="cyan")
    table.add_column("Role", style="magenta")
    table.add_column("Email / Name", style="green")
    table.add_column("Domain", style="yellow")

    for perm in permissions:
        table.add_row(
            perm.get("type", "-"),
            perm.get("role", "-"),
            perm.get("emailAddress") or perm.get("displayName", "-"),
            perm.get("domain", "-"),
        )

    console.print(table)