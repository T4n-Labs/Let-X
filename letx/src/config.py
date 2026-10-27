#!/usr/bin/env python3

BASE_URL = "https://raw.githubusercontent.com/T4n-Labs/vur/main"
CONFIG_DIR = Path.home() / ".config" / "letx"
DB_DIR = CONFIG_DIR / "db"
CATEGORIES = ["core", "extra", "multilib"]
JSON_FILES = ["packages.json", "search.json", "index.json", "categories.json"]
