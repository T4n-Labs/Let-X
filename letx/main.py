#!/usr/bin/env python3
"""
Let-X (Void User Repository Helper)
A Lightweight CLI Tool official
"""
import sys
import argparse
from letx.src.utility import ensure_dirs
from letx.src.cmd import cmd_get, cmd_search, cmd_update_pkg, cmd_update_db, cmd_info

def main():
    parser = argparse.ArgumentParser(
        prog="letx",
        description="Let-X: Void User Repository(VUR) Helper Tool"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # letx get <pkgname>
    parser_get = subparsers.add_parser("get", help="Retrieving package template")
    parser_get.add_argument("pkg_name", help="Package Name")

    # letx search <query>
    parser_search = subparsers.add_parser("search", help="Searching for a package (name/description/category)")
    parser_search.add_argument("query", help="Search keywords")

    # letx update [pkg_name]
    parser_update = subparsers.add_parser("update", help="Update database or template package")
    parser_update.add_argument("pkg_name", nargs="?", default=None, help="Package name (optional)")

    # letx info <pkg_name>
    parser_info = subparsers.add_parser("info", help="Displaying detailed package information")
    parser_info.add_argument("pkg_name", help="Package Name")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    ensure_dirs()

    if args.command == "get":
        cmd_get(args.pkg_name)
    elif args.command == "search":
        cmd_search(args.query)
    elif args.command == "update":
        if args.pkg_name:
            cmd_update_pkg(args.pkg_name)
        else:
            cmd_update_db()
    elif args.command == "info":
        cmd_info(args.pkg_name)

if __name__ == "__main__":
    main()