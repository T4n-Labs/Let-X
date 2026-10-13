"""
cli.py — CLI entry point for Let-X v0.1.2
"""

from __future__ import annotations

import argparse
import sys

from letx.ops.search import (
    search_packages,
    list_packages,
    latest_packages,
    available_categories,
    count_packages,
    search_local_template,
)
from letx.ops.info    import get_info, get_local_template_info
from letx.repo.fetch  import download_package
from letx.repo.index  import fetch_index
from letx.utils.print import (
    console,
    print_package_table,
    print_package_info,
    print_local_template_info,
    print_package_counts,
    print_success,
    print_error,
    print_info,
    print_warn,
)

VERSION = "0.1.2"

# ─── Helpers ──────────────────────────────────────────────

def _no_args_error(parser: argparse.ArgumentParser) -> int:
    """Print [ERROR] No Options + usage and exit 1."""
    console.print("[bold red][ERROR][/bold red] No Options\n")
    parser.print_help()
    return 1


# ─── Parser ───────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="letx",
        description="Let-X — VUR Helper for Void Linux",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  letx -h\n"
            "  letx -v\n"
            "  letx update\n"
        ),
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"letx {VERSION}",
    )

    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.required = False   # allow bare 'letx' → custom error

    # ── search ──────────────────────────────────────────
    p_search = sub.add_parser(
        "search",
        help="Search for a package in VUR",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  letx search discord\n"
            '  letx search "Programming Language"\n'
            "  letx search browser -c extra\n"
            "  letx search -t discord\n"
        ),
    )
    p_search.add_argument(
        "keyword",
        nargs="?",
        help="Package name or description to search",
    )
    p_search.add_argument(
        "-c", "--category",
        metavar="CATEGORY",
        help="Filter by category: core | extra | multilib",
    )
    p_search.add_argument(
        "-t", "--template",
        metavar="PKG_NAME",
        help="Search for a template locally in ~/.config/letx/",
    )

    # ── info ────────────────────────────────────────────
    p_info = sub.add_parser(
        "info",
        help="Show package details",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  letx info discord\n"
            "  letx info all\n"
            "  letx info -c extra\n"
            "  letx info -t discord\n"
        ),
    )
    p_info.add_argument(
        "name",
        nargs="?",
        help="Package name | all | core | extra | multilib",
    )
    p_info.add_argument(
        "-c", "--category",
        metavar="CATEGORY",
        help="Display packages in a specific category (all|core|extra|multilib)",
    )
    p_info.add_argument(
        "-t", "--template",
        metavar="PKG_NAME",
        help="Show local template information",
    )

    # ── list ────────────────────────────────────────────
    p_list = sub.add_parser(
        "list",
        help="List available packages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  letx list all\n"
            "  letx list -c extra\n"
            "  letx list -p\n"
            "  letx list -p core\n"
        ),
    )
    p_list.add_argument(
        "scope",
        nargs="?",
        help="Scope: all | core | extra | multilib (shows top 20 newest)",
    )
    p_list.add_argument(
        "-c", "--category",
        metavar="CATEGORY",
        help="List all packages in a category",
    )
    p_list.add_argument(
        "-p", "--package",
        nargs="?",
        const="__all__",
        metavar="CATEGORY",
        help="Show package count info (optionally for a specific category)",
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


# ─── Command Handlers ─────────────────────────────────────

def cmd_search(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    # letx search -t <pkg>
    if args.template:
        return _search_local_template(args.template)

    # letx search (no keyword, no flags)
    if not args.keyword:
        console.print("[bold red][ERROR][/bold red] No Options\n")
        parser.parse_args(["search", "-h"])
        return 1

    # letx search <keyword> [-c category]
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

    # Show description column when searching by description (quoted or multi-word)
    show_desc = " " in args.keyword or args.keyword.startswith('"')
    print_package_table(results, title=f"Search Results: {args.keyword}", show_desc=show_desc)
    return 0


def _search_local_template(pkg_name: str) -> int:
    """Handle letx search -t <pkg_name>."""
    print_info(f"Searching local templates for '{pkg_name}' ...")

    info = get_local_template_info(pkg_name)

    if not info["found"]:
        print_warn(
            f"Template '{pkg_name}' not found locally.\n"
            f"  Checked: core → extra → multilib\n"
            f"  Run 'letx get {pkg_name}' to download it."
        )
        return 1

    print_local_template_info(info)
    return 0


def cmd_info(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    # letx info -t <pkg>
    if args.template:
        return _info_local_template(args.template)

    # letx info -c <category>
    if args.category and not args.name:
        return _info_list_category(args.category)

    # letx info <name> -c <category>  (category used as hint, show detail)
    if args.name and args.category:
        return _info_detail(args.name)

    # letx info all|core|extra|multilib
    if args.name in ("all", "core", "extra", "multilib"):
        cat = None if args.name == "all" else args.name
        return _info_top20(cat, label=args.name)

    # letx info <pkg_name>
    if args.name:
        return _info_detail(args.name)

    # letx info (no args)
    return _no_args_error(parser)


def _info_detail(name: str) -> int:
    try:
        info = get_info(name)
    except RuntimeError as e:
        print_error(str(e))
        return 1

    if not info:
        print_error(f"Package '{name}' not found in VUR.")
        return 1

    print_package_info(info)
    return 0


def _info_list_category(category: str) -> int:
    if category.lower() == "all":
        packages = list_packages()
        title    = "VUR Packages — All"
    else:
        packages = list_packages(category=category)
        title    = f"VUR Packages — {category}"

    if not packages:
        cats = available_categories()
        print_warn(f"No packages in category '{category}'.")
        print_info(f"Available categories: {', '.join(cats)}")
        return 1

    print_package_table(packages, title=title, show_desc=True)
    return 0


def _info_top20(category: str | None, label: str) -> int:
    packages = latest_packages(category=category, limit=20)
    title = f"Latest 20 — {label.capitalize()}"
    print_package_table(packages, title=title, show_desc=True)
    return 0


def _info_local_template(pkg_name: str) -> int:
    info = get_local_template_info(pkg_name)
    if not info["found"]:
        print_warn(
            f"Template '{pkg_name}' not found locally.\n"
            f"  Run 'letx get {pkg_name}' to download it."
        )
        return 1
    print_local_template_info(info)
    return 0


def cmd_list(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    # letx list -p [category]
    if args.package is not None:
        cat = None if args.package == "__all__" else args.package
        try:
            counts = count_packages(category=cat)
        except RuntimeError as e:
            print_error(str(e))
            return 1
        print_package_counts(counts, category=cat)
        return 0

    # letx list -c <category>
    if args.category:
        cat = None if args.category.lower() == "all" else args.category
        try:
            packages = list_packages(category=cat)
        except RuntimeError as e:
            print_error(str(e))
            return 1
        title = f"VUR Packages — {args.category.capitalize()}"
        if not packages:
            cats = available_categories()
            print_warn(f"No packages in category '{args.category}'.")
            print_info(f"Available: {', '.join(cats)}")
            return 1
        print_package_table(packages, title=title)
        return 0

    # letx list all|core|extra|multilib
    if args.scope:
        scope = args.scope.lower()
        cat   = None if scope == "all" else scope
        packages = latest_packages(category=cat, limit=20)
        title = f"Latest 20 — {scope.capitalize()}"
        print_package_table(packages, title=title, show_desc=True)
        return 0

    # letx list (no args)
    return _no_args_error(parser)


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


# ─── Main ─────────────────────────────────────────────────

def main() -> None:
    parser = build_parser()
    args   = parser.parse_args()

    # bare 'letx' with no subcommand
    if args.command is None:
        sys.exit(_no_args_error(parser))

    if args.command == "search":
        sys.exit(cmd_search(args, parser))
    elif args.command == "info":
        sys.exit(cmd_info(args, parser))
    elif args.command == "list":
        sys.exit(cmd_list(args, parser))
    elif args.command == "get":
        sys.exit(cmd_get(args))
    elif args.command == "update":
        sys.exit(cmd_update(args))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
