"""
cli.py — Entry point CLI untuk Let-X
Menggunakan argparse (stdlib) — tidak butuh dependensi eksternal
"""

from __future__ import annotations

import argparse
import sys

from letx.ops.search  import search_packages, list_packages, available_categories
from letx.ops.info    import get_info
from letx.repo.fetch  import download_package
from letx.repo.index  import fetch_index
from letx.utils.print import (
    console,
    print_package_table,
    print_package_info,
    print_success,
    print_error,
    print_info,
    print_warn,
)


# ─── Parser ───────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="letx",
        description="Let-X — VUR Helper untuk Void Linux",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Contoh:\n"
            "  letx search discord\n"
            "  letx search browser -c extra\n"
            "  letx info wine\n"
            "  letx list\n"
            "  letx list -c multilib\n"
            "  letx get discord\n"
            "  letx update\n"
        ),
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="letx 0.1.0",
    )

    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    # ── search ──────────────────────────────────────────
    p_search = sub.add_parser("search", help="Cari package di VUR")
    p_search.add_argument("keyword", help="Kata kunci pencarian")
    p_search.add_argument(
        "-c", "--category",
        metavar="KATEGORI",
        help="Filter by kategori: core | extra | multilib",
    )

    # ── info ────────────────────────────────────────────
    p_info = sub.add_parser("info", help="Tampilkan detail package")
    p_info.add_argument("name", help="Nama package")

    # ── list ────────────────────────────────────────────
    p_list = sub.add_parser("list", help="Tampilkan semua package")
    p_list.add_argument(
        "-c", "--category",
        metavar="KATEGORI",
        help="Filter by kategori: core | extra | multilib",
    )

    # ── get ─────────────────────────────────────────────
    p_get = sub.add_parser("get", help="Download template package ke lokal")
    p_get.add_argument("name", help="Nama package")
    p_get.add_argument(
        "-f", "--force",
        action="store_true",
        help="Re-download meski sudah ada lokal",
    )

    # ── update ──────────────────────────────────────────
    sub.add_parser("update", help="Refresh cache index dari VUR")

    return parser


# ─── Handlers ─────────────────────────────────────────────

def cmd_search(args: argparse.Namespace) -> int:
    print_info(
        f"Mencari '{args.keyword}'"
        + (f" [kategori: {args.category}]" if args.category else "")
        + " ..."
    )
    try:
        results = search_packages(args.keyword, category=args.category)
    except RuntimeError as e:
        print_error(str(e))
        return 1

    if not results:
        print_warn(f"Tidak ada package yang cocok dengan '{args.keyword}'.")
        return 0

    print_package_table(results, title=f"Hasil Pencarian: {args.keyword}")
    return 0


def cmd_info(args: argparse.Namespace) -> int:
    try:
        info = get_info(args.name)
    except RuntimeError as e:
        print_error(str(e))
        return 1

    if not info:
        print_error(f"Package '{args.name}' tidak ditemukan di VUR.")
        return 1

    print_package_info(info)
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    try:
        packages = list_packages(category=args.category)
    except RuntimeError as e:
        print_error(str(e))
        return 1

    title = "Package VUR" + (f" — Kategori: {args.category}" if args.category else " — Semua")

    if not packages:
        cats = available_categories()
        print_warn(f"Tidak ada package di kategori '{args.category}'.")
        print_info(f"Kategori yang tersedia: {', '.join(cats)}")
        return 0

    print_package_table(packages, title=title)
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    try:
        info = get_info(args.name)
    except RuntimeError as e:
        print_error(str(e))
        return 1

    if not info:
        print_error(f"Package '{args.name}' tidak ditemukan di VUR.")
        return 1

    if info["installed_locally"] and not args.force:
        print_warn(
            f"Template '{args.name}' sudah ada di: {info['local_path']}\n"
            f"  Gunakan --force untuk re-download."
        )
        return 0

    print_info(f"Mengambil template '{args.name}' ({info['category']}) ...")

    def progress(msg: str) -> None:
        console.print(f"[dim]{msg}[/dim]")

    try:
        dest = download_package(
            pkg_path=info["path"],
            category=info["category"],
            pkg_name=args.name,
            progress_cb=progress,
        )
    except Exception as e:
        print_error(f"Gagal mengambil template: {e}")
        return 1

    print_success(f"Template berhasil disimpan ke: {dest}")
    print_info("Selanjutnya kamu bisa build dengan xbps-src (coming soon).")
    return 0


def cmd_update(_args: argparse.Namespace) -> int:
    print_info("Memperbarui index dari VUR ...")
    try:
        packages = fetch_index(force=True)
        print_success(f"Index diperbarui — {len(packages)} package tersedia.")
        return 0
    except RuntimeError as e:
        print_error(str(e))
        return 1


# ─── Dispatch ─────────────────────────────────────────────

_HANDLERS = {
    "search": cmd_search,
    "info":   cmd_info,
    "list":   cmd_list,
    "get":    cmd_get,
    "update": cmd_update,
}


def main() -> None:
    parser  = build_parser()
    args    = parser.parse_args()
    handler = _HANDLERS.get(args.command)
    if handler is None:
        parser.print_help()
        sys.exit(1)
    sys.exit(handler(args))


if __name__ == "__main__":
    main()
