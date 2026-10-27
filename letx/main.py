#!/usr/bin/env python3
"""
Let-X (Void User Repository Helper)
A Lightweight CLI Tool official
"""
import os
import sys
import json
import re
import argparse
import urllib.request
import urllib.error
from pathlib import Path

# Import dari src
from letx.src.config import *
from letx.src.utility import *
from letx.src.cmd import *

# Version information
__version__ = "1.0.0"

def main():
    parser = argparse.ArgumentParser(
        prog="letx",
        description="Let-X: Void User Repository(VUR) Helper Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  letx update                 Update database
  letx search browser         Search for packages
  letx info calamares         Show package information
  letx get dinit              Download template
  letx --version              Show version
        """
    )
    
    # Add version argument
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'Let-X {__version__}',
        help='Show program version and exit'
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        metavar='{get,search,update,info}'
    )

    # letx get <pkgname>
    parser_get = subparsers.add_parser(
        "get",
        help="Retrieving package template",
        description="Download Void Linux template for a specific package"
    )
    parser_get.add_argument("pkg_name", help="Package Name")

    # letx search <query>
    parser_search = subparsers.add_parser(
        "search",
        help="Searching for a package (name/description/category)",
        description="Search packages by name, description, or category"
    )
    parser_search.add_argument("query", help="Search keywords")

    # letx update [pkg_name]
    parser_update = subparsers.add_parser(
        "update",
        help="Update database or template package",
        description="Update VUR database or download latest template for a package"
    )
    parser_update.add_argument(
        "pkg_name",
        nargs="?",
        default=None,
        help="Package name (optional, if omitted updates database)"
    )

    # letx info <pkg_name>
    parser_info = subparsers.add_parser(
        "info",
        help="Displaying detailed package information",
        description="Show detailed information about a package including dependencies"
    )
    parser_info.add_argument("pkg_name", help="Package Name")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Ensure directories exist
    ensure_dirs()

    # Execute command
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