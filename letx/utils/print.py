"""
utils/print.py — Rich output helpers for Let-X
"""

from __future__ import annotations

from typing import Any

from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.text import Text

console = Console()

# ─── Color theme ──────────────────────────────────────────
C_NAME    = "bold cyan"
C_VER     = "green"
C_CAT     = "yellow"
C_MAINT   = "dim white"
C_LOCAL   = "bold green"
C_MISSING = "dim red"
C_TITLE   = "bold white"
C_URL     = "blue underline"
C_COUNT   = "bold magenta"


def print_package_table(packages: list[dict[str, Any]], title: str = "") -> None:
    """Display a list of packages as a Rich table."""
    if not packages:
        console.print("[dim]No packages found.[/dim]")
        return

    table = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
        title=title or None,
        title_style=C_TITLE,
        expand=False,
    )
    table.add_column("Name",       style=C_NAME,  no_wrap=True)
    table.add_column("Version",    style=C_VER,   no_wrap=True)
    table.add_column("Category",   style=C_CAT,   no_wrap=True)
    table.add_column("Maintainer", style=C_MAINT)

    for pkg in packages:
        table.add_row(
            pkg.get("name", ""),
            pkg.get("version", "-") or "-",
            pkg.get("category", ""),
            _short_maintainer(pkg.get("maintainer", "")),
        )

    console.print()
    console.print(table)
    console.print(f"  [dim]Total: [{C_COUNT}]{len(packages)}[/{C_COUNT}] package(s)[/dim]\n")


def print_package_info(info: dict[str, Any]) -> None:
    """Display detailed info for a single package in a Rich panel."""
    name       = info.get("name", "?")
    version    = info.get("version") or "unknown"
    category   = info.get("category", "?")
    homepage   = info.get("homepage", "-")
    maintainer = info.get("maintainer", "-")
    path       = info.get("path", "-")
    is_local   = info.get("installed_locally", False)
    local_path = info.get("local_path")

    status_text = (
        f"[{C_LOCAL}]✔ Available locally[/{C_LOCAL}] → {local_path}"
        if is_local
        else f"[{C_MISSING}]✘ Not fetched yet[/{C_MISSING}]"
    )

    content = Text.assemble(
        ("Name       : ", "dim"), (name,       C_NAME),  "\n",
        ("Version    : ", "dim"), (version,    C_VER),   "\n",
        ("Category   : ", "dim"), (category,   C_CAT),   "\n",
        ("Repo Path  : ", "dim"), (path,       "white"), "\n",
        ("Homepage   : ", "dim"), (homepage,   C_URL),   "\n",
        ("Maintainer : ", "dim"), (maintainer, C_MAINT), "\n",
    )

    console.print()
    console.print(Panel(
        content,
        title=f"[{C_TITLE}] {name} [/{C_TITLE}]",
        border_style="cyan",
        expand=False,
    ))
    console.print(f"  Status     : {status_text}\n")


def print_success(msg: str) -> None:
    console.print(f"[bold green]✔[/bold green] {msg}")


def print_error(msg: str) -> None:
    console.print(f"[bold red]✘[/bold red] {msg}")


def print_info(msg: str) -> None:
    console.print(f"[bold cyan]→[/bold cyan] {msg}")


def print_warn(msg: str) -> None:
    console.print(f"[bold yellow]![/bold yellow] {msg}")


def _short_maintainer(maintainer: str) -> str:
    """Return only the name part, stripping the email address."""
    if "<" in maintainer:
        return maintainer.split("<")[0].strip()
    return maintainer
