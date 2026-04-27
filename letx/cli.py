"""
cli.py — CLI entry point for Let-X
Uses argparse (stdlib) — no external dependencies required
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
        description="Let-X — VUR Helper for Void Linux",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
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
        version="letx 0.1.1",
    )

    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    # ── search ──────────────────────────────────────────
    p_search = sub.add_parser("search", help="Search for a package in VUR")
    p_search.add_argument("keyword", help="Search keyword")
    p_search.add_argument(
        "-c", "--category",
        metavar="CATEGORY",
        help="Filter by category: core | extra | multilib",
    )

    # ── info ────────────────────────────────────────────
    p_info = sub.add_parser("info", help="Show package details")
    p_info.add_argument("name", help="Package name")

    # ── list ────────────────────────────────────────────
    p_list = sub.add_parser("list", help="List all available packages")
    p_list.add_argument(
        "-c", "--category",
        metavar="CATEGORY",
        help="Filter by category: core | extra | multilib",
    )

    # ── get ─────────────────────────────────────────────
    p_get = sub.add_parser("get", help="Download package template locally")
    p_get.add_argument("name", help="Package name")
    p_get.add_argument(
        "-f", "--force",
        action="store_true",
        help="Re-download even if template already exists locally",
    )

    # ── update ──────────────────────────────────────────
    sub.add_parser("update", help="Refresh the VUR package index cache")

    return parser


# ─── Handlers ─────────────────────────────────────────────

def cmd_search(args: argparse.Namespace) -> int:
    print_info(
        f"Searching for '{args.keyword}'"
        + (f" [category: {args.category}]" if args.category else "")
        + " ..."
    )
    try:
        results = search_packages(args.keyword, category=args.category)
    except RuntimeError as e:
        print_error(str(e))
        return 1

    if not results:
        print_warn(f"No packages found matching '{args.keyword}'.")
        return 0

    print_package_table(results, title=f"Search Results: {args.keyword}")
    return 0


def cmd_info(args: argparse.Namespace) -> int:
    try:
        info = get_info(args.name)
    except RuntimeError as e:
        print_error(str(e))
        return 1

    if not info:
        print_error(f"Package '{args.name}' not found in VUR.")
        return 1

    print_package_info(info)
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    try:
        packages = list_packages(category=args.category)
    except RuntimeError as e:
        print_error(str(e))
        return 1

    title = "VUR Packages" + (f" — Category: {args.category}" if args.category else " — All")

    if not packages:
        cats = available_categories()
        print_warn(f"No packages found in category '{args.category}'.")
        print_info(f"Available categories: {', '.join(cats)}")
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
        print_error(f"Package '{args.name}' not found in VUR.")
        return 1

    if info["installed_locally"] and not args.force:
        print_warn(
            f"Template '{args.name}' already exists at: {info['local_path']}\n"
            f"  Use --force to re-download."
        )
        return 0

    print_info(f"Fetching template '{args.name}' ({info['category']}) ...")

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
        print_error(f"Failed to fetch template: {e}")
        return 1

    print_success(f"Template saved to: {dest}")
    print_info("You can now build it with xbps-src (coming soon).")
    return 0


def cmd_update(_args: argparse.Namespace) -> int:
    print_info("Refreshing package index from VUR ...")
    try:
        packages = fetch_index(force=True)
        print_success(f"Index updated — {len(packages)} packages available.")
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
