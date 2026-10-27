#!/usr/bin/env python3
import sys
import json
import re
import urllib.request
import urllib.error
from pathlib import Path
from letx.src.config import DB_DIR, CONFIG_DIR, CATEGORIES

def ensure_dirs():
    """Ensure that the configuration directory and categories are available."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    for cat in CATEGORIES:
        (CONFIG_DIR / cat).mkdir(parents=True, exist_ok=True)

def fetch_url(url):
    """Getting data from URL."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'LetX/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(f"[ERROR]: Failed to retrieve data from {url}\n   Details: {e.reason}")
        sys.exit(1)

def load_json(filename):
    """Loading JSON file from local cache."""
    filepath = DB_DIR / filename
    if not filepath.exists():
        print(f"⚠ Database '{filename}' not found. Run 'letx update' first.")
        sys.exit(1)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Clean up keys with trailing spaces
            return [{k.strip(): v.strip() if isinstance(v, str) else v for k, v in item.items()} for item in data]
    except json.JSONDecodeError:
        print(f"[ERROR]: File {filename} Broken or Invalid.")
        sys.exit(1)

def find_package(pkg_name):
    """Retrieving package metadata from packages.json."""
    packages = load_json("packages.json")
    for pkg in packages:
        if pkg.get("name") == pkg_name:
            return pkg
    return None

def parse_template(content):
    """Extracting variables from Void Linux template files."""
    data = {}
    fields = ['revision', 'build_style', 'hostmakedepends', 'makedepends', 'depends', 'license']
    for field in fields:
        pattern = rf'^{field}\s*=\s*(.*?)(?=\n[a-z_]+\s*=|$)'
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        if match:
            val = match.group(1).strip()
            # Remove quotation marks if present
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            data[field] = val
        else:
            data[field] = "N/A"
    return data

def format_dependencies(dep_string):
    """Format the dependency string into a 4-column grid."""
    if not dep_string or dep_string == "N/A":
        return "N/A"
    
    deps = [d.strip() for d in dep_string.replace('\n', ' ').split() if d.strip()]
    if not deps:
        return "N/A"
    
    result = []
    for i in range(0, len(deps), 4):
        chunk = deps[i:i+4]
        chunk += [""] * (4 - len(chunk))
        line = f"-) {chunk[0]:<20} -) {chunk[1]:<20} -) {chunk[2]:<20} -) {chunk[3]:<20}"
        result.append(line.rstrip())
    return "\n".join(result)