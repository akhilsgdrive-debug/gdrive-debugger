import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    name="gdrive-debugger",
    help="Debug and automate Google Drive operations with rich diagnostics.",
    add_completion=False,
)
console = Console()


@app.command()
def version():
    """Show the current version."""
    from gdrive_debugger import __version__
    console.print(f"gdrive-debugger v{__version__}")


@app.command()
def hello():
    """Quick hello command to verify installation."""
    console.print(Panel.fit(
        "[bold green]Hello from gdrive-debugger![/bold green]\n\n"
        "Your Google Drive debugging toolkit is ready.",
        title="Welcome",
        border_style="green"
    ))


if __name__ == "__main__":
    app()