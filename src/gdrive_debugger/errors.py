"""Centralized error handling with actionable suggestions."""

from rich.console import Console

console = Console()


ERROR_SUGGESTIONS = {
    403: "Permission denied. Check sharing settings or OAuth scopes.",
    404: "File not found. Verify the file ID or check if it was moved to trash.",
    429: "Rate limit exceeded. Wait a bit or reduce request frequency.",
    "insufficientFilePermissions": "You don't have permission to perform this action on the file.",
    "notFound": "The requested file/folder does not exist or was deleted.",
}


def handle_drive_error(error: Exception) -> None:
    """Handle common Google Drive errors with helpful messages."""
    error_str = str(error).lower()
    status_code = getattr(error, "status", None) or getattr(error, "code", None)

    suggestion = None

    if status_code in ERROR_SUGGESTIONS:
        suggestion = ERROR_SUGGESTIONS[status_code]
    else:
        for key in ERROR_SUGGESTIONS:
            if key in error_str:
                suggestion = ERROR_SUGGESTIONS[key]
                break

    if suggestion:
        console.print(f"[yellow]Suggestion:[/yellow] {suggestion}")
    else:
        console.print("[dim]Tip: Try running with more verbose logging or check Google Cloud quotas.[/dim]")

    console.print(f"[red]Error:[/red] {error}")