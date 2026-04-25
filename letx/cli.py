"""
cli.py — Entry point CLI untuk Let-X
"""

from __future__ import annotations

from typing import Annotated, Optional

import typer
from rich.console import Console

from letx.ops.search  import search_packages, list_packages, available_categories
from letx.ops.info    import get_info
from letx.repo.fetch  import download_package
from letx.repo.index  import fetch_index, cache_info
from letx.utils.print import (
    console,
    print_package_table,
    print_package_info,
    print_success,
    print_error,
    print_info,
    print_warn,
)

app = typer.Typer(
    name="letx",
    help="[cyan]Let-X[/cyan] — VUR Helper for Void Linux",
    rich_markup_mode="rich",
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
)


# ─── letx search <keyword> ────────────────────────────────

@app.command("search")
def cmd_search(
    keyword: Annotated[str, typer.Argument(help="Kata kunci pencarian")],
    category: Annotated[
        Optional[str],
        typer.Option("--category", "-c", help="Filter by kategori (core/extra/multilib)"),
    ] = None,
) -> None:
    """Cari package di VUR berdasarkan keyword."""
    print_info(
        f"Mencari '{keyword}'"
        + (f" [kategori: {category}]" if category else "")
        + " ..."
    )

    try:
        results = search_packages(keyword, category=category)
    except RuntimeError as e:
        print_error(str(e))
        raise typer.Exit(1)

    if not results:
        print_warn(f"Tidak ada package yang cocok dengan '{keyword}'.")
        raise typer.Exit(0)

    print_package_table(results, title=f"Hasil Pencarian: {keyword}")


# ─── letx info <package> ──────────────────────────────────

@app.command("info")
def cmd_info(
    name: Annotated[str, typer.Argument(help="Nama package")],
) -> None:
    """Tampilkan detail lengkap sebuah package."""
    try:
        info = get_info(name)
    except RuntimeError as e:
        print_error(str(e))
        raise typer.Exit(1)

    if not info:
        print_error(f"Package '[bold]{name}[/bold]' tidak ditemukan di VUR.")
        raise typer.Exit(1)

    print_package_info(info)


# ─── letx list ────────────────────────────────────────────

@app.command("list")
def cmd_list(
    category: Annotated[
        Optional[str],
        typer.Option("--category", "-c", help="Filter by kategori (core/extra/multilib)"),
    ] = None,
) -> None:
    """Tampilkan semua package di VUR (opsional filter by kategori)."""
    try:
        packages = list_packages(category=category)
    except RuntimeError as e:
        print_error(str(e))
        raise typer.Exit(1)

    title = "Package VUR" + (f" — Kategori: {category}" if category else " — Semua")

    if not packages:
        cats = available_categories()
        print_warn(f"Tidak ada package di kategori '{category}'.")
        print_info(f"Kategori yang tersedia: {', '.join(cats)}")
        raise typer.Exit(0)

    print_package_table(packages, title=title)


# ─── letx get <package> ───────────────────────────────────

@app.command("get")
def cmd_get(
    name: Annotated[str, typer.Argument(help="Nama package yang akan diambil")],
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Re-download meski sudah ada lokal"),
    ] = False,
) -> None:
    """Download template package dari VUR ke lokal (~/.config/letx/)."""
    try:
        info = get_info(name)
    except RuntimeError as e:
        print_error(str(e))
        raise typer.Exit(1)

    if not info:
        print_error(f"Package '[bold]{name}[/bold]' tidak ditemukan di VUR.")
        raise typer.Exit(1)

    if info["installed_locally"] and not force:
        print_warn(
            f"Template '[bold]{name}[/bold]' sudah ada di: {info['local_path']}\n"
            f"  Gunakan [bold]--force[/bold] untuk re-download."
        )
        raise typer.Exit(0)

    pkg_path = info["path"]
    category = info["category"]

    print_info(f"Mengambil template '[bold]{name}[/bold]' ({category}) ...")

    def progress(msg: str) -> None:
        console.print(f"[dim]{msg}[/dim]")

    try:
        dest = download_package(
            pkg_path=pkg_path,
            category=category,
            pkg_name=name,
            progress_cb=progress,
        )
    except Exception as e:
        print_error(f"Gagal mengambil template: {e}")
        raise typer.Exit(1)

    print_success(f"Template berhasil disimpan ke: [bold]{dest}[/bold]")
    print_info("Selanjutnya kamu bisa build dengan xbps-src (coming soon).")


# ─── letx update ──────────────────────────────────────────

@app.command("update")
def cmd_update() -> None:
    """Refresh cache index packages dari VUR."""
    print_info("Updating the index of VUR...")
    try:
        packages = fetch_index(force=True)
        print_success(f"Index updated — {len(packages)} packages available.")
    except RuntimeError as e:
        print_error(str(e))
        raise typer.Exit(1)


# ─── Main ─────────────────────────────────────────────────

def main() -> None:
    app()


if __name__ == "__main__":
    main()
