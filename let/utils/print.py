"""
utils/print.py — Helper output berbasis Rich
"""

from __future__ import annotations

from typing import Any

from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.text import Text

console = Console()

# ─── Warna & style tema ───────────────────────────────────
C_NAME     = "bold cyan"
C_VER      = "green"
C_CAT      = "yellow"
C_MAINT    = "dim white"
C_LOCAL    = "bold green"
C_MISSING  = "dim red"
C_TITLE    = "bold white"
C_URL      = "blue underline"
C_COUNT    = "bold magenta"


def print_package_table(packages: list[dict[str, Any]], title: str = "") -> None:
    """Tampilkan list packages dalam tabel."""
    if not packages:
        console.print("[dim]Tidak ada package ditemukan.[/dim]")
        return

    table = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
        title=title or None,
        title_style=C_TITLE,
        expand=False,
    )
    table.add_column("Nama",       style=C_NAME,  no_wrap=True)
    table.add_column("Versi",      style=C_VER,   no_wrap=True)
    table.add_column("Kategori",   style=C_CAT,   no_wrap=True)
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
    console.print(f"  [dim]Total: [{C_COUNT}]{len(packages)}[/{C_COUNT}] package[/dim]\n")


def print_package_info(info: dict[str, Any]) -> None:
    """Tampilkan detail satu package dalam panel."""
    name     = info.get("name", "?")
    version  = info.get("version") or "tidak diketahui"
    category = info.get("category", "?")
    homepage = info.get("homepage", "-")
    maintainer = info.get("maintainer", "-")
    path     = info.get("path", "-")
    is_local = info.get("installed_locally", False)
    local_path = info.get("local_path")

    status_text = (
        f"[{C_LOCAL}]✔ Tersedia lokal[/{C_LOCAL}] → {local_path}"
        if is_local
        else f"[{C_MISSING}]✘ Belum di-get[/{C_MISSING}]"
    )

    content = Text.assemble(
        ("Nama       : ", "dim"), (name,      C_NAME),     "\n",
        ("Versi      : ", "dim"), (version,   C_VER),      "\n",
        ("Kategori   : ", "dim"), (category,  C_CAT),      "\n",
        ("Path Repo  : ", "dim"), (path,      "white"),    "\n",
        ("Homepage   : ", "dim"), (homepage,  C_URL),      "\n",
        ("Maintainer : ", "dim"), (maintainer, C_MAINT),   "\n",
        ("Status     : ", "dim"),
    )
    # Append status (Rich markup, bukan Text)
    console.print()
    panel = Panel(
        content,
        title=f"[{C_TITLE}] {name} [/{C_TITLE}]",
        border_style="cyan",
        expand=False,
    )
    console.print(panel)
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
    """Tampilkan hanya nama tanpa email untuk tabel yang ringkas."""
    if "<" in maintainer:
        return maintainer.split("<")[0].strip()
    return maintainer
