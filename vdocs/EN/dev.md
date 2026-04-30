# Let-X — Developer Guide

> Technical documentation for contributors and maintainers of **Let-X v0.1.2**.

---

## Table of Contents

- [Project Architecture](#project-architecture)
- [Directory Structure](#directory-structure)
- [Module Reference](#module-reference)
- [Data Flow](#data-flow)
- [Setup Development Environment](#setup-development-environment)
- [Code Conventions](#code-conventions)
- [Adding a New Command](#adding-a-new-command)
- [Running Tests](#running-tests)
- [Building the xbps Package](#building-the-xbps-package)
- [Dependencies](#dependencies)
- [Roadmap](#roadmap)

---

## Project Architecture

Let-X follows a strict **separation of concerns** — each layer has a single, well-defined responsibility:

```
┌──────────────────────────────────────────────┐
│                 CLI (cli.py)                  │  argparse: parse args, route to handlers
├────────────────────┬─────────────────────────┤
│       ops/         │         repo/            │  business logic vs data access
│  search.py         │     index.py             │
│  info.py           │     fetch.py             │
├────────────────────┴─────────────────────────┤
│              utils/print.py                   │  Rich: all terminal output
├──────────────────────────────────────────────┤
│               config.py                       │  constants, paths, URLs
└──────────────────────────────────────────────┘
```

**Key principles:**
- `cli.py` contains no logic — it only orchestrates calls to `ops/` and `repo/`
- `ops/` does not know about HTTP — that is `repo/`'s concern
- `repo/` does not know about display — that is `utils/`'s concern
- `config.py` does not import any other module from the project

---

## Directory Structure

```
Let-X/
├── letx/                         ← Main Python package
│   ├── __init__.py               → Version and app name
│   ├── cli.py                    → CLI entry point (argparse)
│   ├── config.py                 → All constants and paths
│   │
│   ├── repo/                     → Data access layer (GitHub)
│   │   ├── __init__.py
│   │   ├── index.py              → Fetch and cache packages.json
│   │   └── fetch.py              → Download template folders via GitHub API
│   │
│   ├── ops/                      → Business logic layer
│   │   ├── __init__.py
│   │   ├── search.py             → Search, list, count, local template lookup
│   │   └── info.py               → Package detail + local template info
│   │
│   └── utils/
│       ├── __init__.py
│       └── print.py              → All Rich output (tables, panels, colors)
│
├── tests/
│   ├── __init__.py
│   └── test_search.py            → Unit tests
│
├── xbps-template/
│   └── letx/
│       └── template              → xbps-src package template
│
├── setup.py                      → Compatibility shim for xbps-src build style
├── pyproject.toml                → Project metadata and dependencies
├── install.sh                    → Bash installation script
├── LICENSE
└── README.md
```

---

## Module Reference

### `config.py`

Single source of truth for all constants. No other module should hardcode paths or URLs.

```python
# Remote
VUR_REPO     = "T4n-Labs/vur"
VUR_API_BASE = "https://api.github.com/repos/T4n-Labs/vur/contents"
PACKAGES_URL = "https://raw.githubusercontent.com/T4n-Labs/vur/main/packages.json"

# Local paths
CONFIG_DIR = Path.home() / ".config" / "letx"
CACHE_DIR  = Path.home() / ".cache"  / "letx"
TEMPLATE_DIRS = {
    "core":     CONFIG_DIR / "core",
    "extra":    CONFIG_DIR / "extra",
    "multilib": CONFIG_DIR / "multilib",
}

CACHE_TTL = 3600  # seconds (1 hour)
```

---

### `repo/index.py`

Manages fetching and caching of `packages.json`.

| Function | Signature | Description |
|---|---|---|
| `fetch_index` | `(force: bool = False) → list[Package]` | Get all packages (cache or GitHub) |
| `get_package` | `(name: str) → Package \| None` | Find one package by exact name |
| `cache_info` | `() → dict` | Current cache status |

**Cache logic:**
```
fetch_index()
    │
    ├─ Cache exists AND age < TTL AND force=False?
    │   └─ return local cache
    │
    └─ Otherwise:
        ├─ GET packages.json from GitHub
        ├─ Write to ~/.cache/letx/packages.json
        └─ Return fresh data
            │
            └─ If fetch FAILS but old cache exists:
                └─ Return stale cache (graceful degradation)
```

---

### `repo/fetch.py`

Downloads package template folders from GitHub using the **GitHub Contents API** (no `git` or `svn` required).

| Function | Signature | Description |
|---|---|---|
| `download_package` | `(pkg_path, category, pkg_name, progress_cb) → Path` | Download a full package folder |
| `package_exists_locally` | `(category, pkg_name) → bool` | Check if template is already local |
| `local_package_path` | `(category, pkg_name) → Path \| None` | Get local path if it exists |

**Fetch strategy:**
```
GitHub Contents API
GET /repos/T4n-Labs/vur/contents/extra/discord
    │
    └─ Response: list of {type, name, path, ...}
        │
        ├─ type == "file"  → download via raw.githubusercontent.com
        └─ type == "dir"   → recurse into subdirectory
```

**Why GitHub Contents API instead of `git clone` or `svn`?**
- No external tools required (`git`/`svn` not needed)
- Downloads only the files needed, not the entire repo
- More portable and predictable behavior
- Trade-off: more HTTP requests for folders with many files

---

### `ops/search.py`

All search and listing operations. Fully offline after the index is cached.

| Function | Signature | Description |
|---|---|---|
| `search_packages` | `(keyword, category=None) → list[Package]` | Search by name or description |
| `list_packages` | `(category=None) → list[Package]` | List all packages |
| `latest_packages` | `(category=None, limit=20) → list[Package]` | Most recently added packages |
| `count_packages` | `(category=None) → dict[str, int]` | Package counts per category |
| `search_local_template` | `(pkg_name) → LocalTemplateResult` | Search local template dirs |
| `available_categories` | `() → list[str]` | Unique categories in index |

**Search fields (v0.1.2 fix):**
```python
# Only name and description — eliminates false positives from maintainer/homepage
_SEARCH_FIELDS = ("name", "description")
```

**Search result ranking:**
```python
def _rank(pkg) -> int:
    name = pkg["name"].lower()
    if name == keyword:       return 0   # exact match → first
    if name.startswith(kw):   return 1   # prefix match
    if kw in name:            return 2   # contains in name
    return 3                             # matched in description
```

**Local template search — core → extra → multilib:**
```python
search_order = ["core", "extra", "multilib"]
for cat in search_order:
    pkg_dir = TEMPLATE_DIRS[cat] / pkg_name
    if pkg_dir.exists():
        return LocalTemplateResult(found=True, category=cat, path=pkg_dir, files=[...])
return LocalTemplateResult(found=False, pkg_name=pkg_name)
```

**`LocalTemplateResult` attributes:**

| Attribute | Type | Description |
|---|---|---|
| `found` | `bool` | Whether the template was found |
| `pkg_name` | `str` | Package name searched |
| `category` | `str \| None` | Category where it was found |
| `path` | `Path \| None` | Full local path to the template directory |
| `files` | `list[str]` | Relative paths of all files in the template |

---

### `ops/info.py`

| Function | Signature | Description |
|---|---|---|
| `get_info` | `(name: str) → dict \| None` | Package details from index + local status |
| `get_local_template_info` | `(pkg_name: str) → dict` | Local template details enriched with VUR data |

`get_info` return structure:
```python
{
    # all fields from packages.json
    "name": "discord",
    "category": "extra",
    "version": "0.0.134",
    "description": "Chat and VOIP application",
    "homepage": "...",
    "maintainer": "...",
    "path": "extra/discord",
    # plus local status
    "installed_locally": True,
    "local_path": "/home/user/.config/letx/extra/discord",
}
```

---

### `utils/print.py`

All terminal output must go through this module. Never use `print()` directly in other modules.

| Function | Description |
|---|---|
| `print_package_table(packages, title, show_desc)` | Rich table for package lists |
| `print_package_info(info)` | Rich panel for single package detail |
| `print_local_template_info(info)` | Rich panel for local template detail |
| `print_package_counts(counts, category)` | Statistics table |
| `print_success(msg)` | `✔ message` (green) |
| `print_error(msg)` | `✘ message` (red) |
| `print_info(msg)` | `→ message` (cyan) |
| `print_warn(msg)` | `! message` (yellow) |

**`print_package_table` — `show_desc` parameter:**

When `show_desc=True`, a Description column is added to the table. This is automatically set to `True` for description-based searches, `letx info -c`, and `letx list` scope commands.

**Color theme:**
```python
C_NAME    = "bold cyan"     # package name
C_VER     = "green"         # version
C_CAT     = "yellow"        # category
C_DESC    = "dim white"     # description
C_MAINT   = "dim white"     # maintainer
C_LOCAL   = "bold green"    # available locally
C_MISSING = "dim red"       # not fetched yet
C_PATH    = "cyan"          # file path
C_FILE    = "dim cyan"      # file listing
```

---

## Data Flow

### `letx search <keyword>`

```
letx search discord
    │
    ▼
cli.py:cmd_search()
    │
    ├─ args.template set? → _search_local_template(args.template)
    │                           │
    │                           └─ ops/search.py:search_local_template()
    │                           └─ utils/print.py:print_local_template_info()
    │
    ├─ no keyword → [ERROR] No Options
    │
    └─ keyword present:
        print_info("Searching for ...")
        ops/search.py:search_packages(keyword, category)
            │
            └─ repo/index.py:fetch_index()
                    ├─ cache valid → read ~/.cache/letx/packages.json
                    └─ expired     → GET GitHub → write cache → return
            │
            └─ for each pkg: check name + description fields
            └─ sort by _rank()
        │
        └─ utils/print.py:print_package_table(results, show_desc)
```

### `letx info all`

```
letx info all
    │
    ▼
cli.py:cmd_info()
    │
    └─ name in ("all","core","extra","multilib") → _info_top20(cat, label)
            │
            └─ ops/search.py:latest_packages(category, limit=20)
                    │
                    └─ list_packages() → return last 20 (insertion order = newest)
            │
            └─ utils/print.py:print_package_table(packages, show_desc=True)
```

### `letx list -p`

```
letx list -p
    │
    ▼
cli.py:cmd_list()
    │
    └─ args.package is not None → count_packages(cat=None)
            │
            └─ fetch_index() → {total: N, core: N, extra: N, multilib: N}
    │
    └─ utils/print.py:print_package_counts(counts)
```

### `letx get <pkg>`

```
letx get discord
    │
    ▼
cli.py:cmd_get()
    │
    ├─ ops/info.py:get_info("discord")
    │       └─ repo/index.py:get_package() + repo/fetch.py:package_exists_locally()
    │
    ├─ Not found → print_error(), return 1
    ├─ Already local & no --force → print_warn(), return 0
    │
    └─ repo/fetch.py:download_package(path, category, name, progress_cb)
            │
            ├─ clean destination if exists
            └─ _fetch_dir() recursively:
                    ├─ GET GitHub Contents API for directory listing
                    ├─ for files  → GET raw.githubusercontent.com → write bytes
                    └─ for dirs   → recurse
    │
    └─ utils/print.py:print_success(dest)
```

---

## Setup Development Environment

```bash
# 1. Fork and clone the repo
git clone https://github.com/<your-username>/Let-X
cd Let-X

# 2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install in development mode
pip install -e ".[dev]"

# 4. Verify
letx --help
pytest tests/ -v
```

---

## Code Conventions

**Naming:**
- Modules and functions: `snake_case`
- Constants in `config.py`: `SCREAMING_SNAKE_CASE`
- Type hints required on all public functions

**Import order:**
```python
# 1. stdlib
import sys
from pathlib import Path
from typing import Any

# 2. third-party
import httpx
from rich.console import Console

# 3. internal (always absolute imports)
from letx.config import CACHE_DIR
from letx.repo.index import fetch_index
```

**Docstrings — required on all public functions:**
```python
def search_packages(keyword: str, category: str | None = None) -> list[Package]:
    """
    Search packages by keyword (case-insensitive).
    Matches against: name, description.

    Args:
        keyword:  search keyword
        category: optional filter ("core"|"extra"|"multilib")

    Returns:
        Matching packages sorted by relevance (exact name first).

    Raises:
        RuntimeError: If the index fetch fails and no local cache exists.
    """
```

**Error handling pattern:**
```python
# In ops/ and repo/ — raise exceptions
def fetch_index(force: bool = False) -> list[Package]:
    ...
    raise RuntimeError(f"Failed to fetch index: {e}") from e

# In cli.py — catch and convert to exit codes
try:
    results = search_packages(keyword)
except RuntimeError as e:
    print_error(str(e))
    return 1
```

---

## Adding a New Command

1. Add a subparser in `cli.py:build_parser()`
2. Add a handler function `cmd_<name>(args) -> int` in `cli.py`
3. Register it in the `main()` dispatch block
4. Business logic goes in a new `ops/<name>.py` module
5. All output via `utils/print.py`
6. Write tests in `tests/test_<name>.py`

**Full skeleton example — `letx remove`:**

```python
# 1. In build_parser():
p_remove = sub.add_parser(
    "remove",
    help="Remove a locally downloaded template",
)
p_remove.add_argument("name", help="Package name")

# 2. Handler in cli.py:
def cmd_remove(args: argparse.Namespace) -> int:
    from letx.ops.remove import remove_template
    removed = remove_template(args.name)
    if removed:
        print_success(f"Template '{args.name}' removed.")
        return 0
    print_error(f"Template '{args.name}' not found locally.")
    return 1

# 3. In main():
elif args.command == "remove":
    sys.exit(cmd_remove(args))

# 4. New file: letx/ops/remove.py
from letx.config import TEMPLATE_DIRS
import shutil

def remove_template(pkg_name: str) -> bool:
    """Remove a locally stored template. Returns True if removed."""
    for cat, base_dir in TEMPLATE_DIRS.items():
        pkg_dir = base_dir / pkg_name
        if pkg_dir.exists():
            shutil.rmtree(pkg_dir)
            return True
    return False
```

---

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run a specific file
pytest tests/test_search.py -v

# With coverage report
pytest tests/ --cov=letx --cov-report=term-missing
```

Tests use `monkeypatch` — no internet connection required:

```python
@pytest.fixture
def fake_cache(tmp_path, monkeypatch):
    """Replace PACKAGES_CACHE with a temp file containing mock data."""
    cache_file = tmp_path / "packages.json"
    cache_file.write_text(json.dumps(MOCK_PACKAGES))
    monkeypatch.setattr("letx.repo.index.PACKAGES_CACHE", cache_file)
    monkeypatch.setattr("letx.repo.index.CACHE_TTL", 9999)  # always fresh
    return cache_file
```

**Available tests:**

| Test | Description |
|---|---|
| `test_fetch_index_from_cache` | Index is read from local cache |
| `test_get_package_found` | Search for an existing package |
| `test_get_package_case_insensitive` | `DISCORD` == `discord` |
| `test_get_package_not_found` | Missing package → returns `None` |
| `test_search_by_name` | Exact name match |
| `test_search_partial` | Partial name match |
| `test_search_with_category_filter` | Category filtering works |
| `test_search_no_results` | No match → empty list |
| `test_list_all` | List returns all packages |
| `test_list_by_category` | List filtered by category |
| `test_available_categories` | Returns unique category set |

---

## Building the xbps Package

### Setup

```bash
git clone https://github.com/void-linux/void-packages ~/void-packages
cd ~/void-packages
./xbps-src binary-bootstrap

cp -r /path/to/Let-X/xbps-template/letx srcpkgs/letx
```

### xbps-src Template Overview

```bash
pkgname=letx
build_style=            # no build_style — using do_build/do_install manually
hostmakedepends="python3 python3-pip python3-setuptools python3-wheel"
depends="python3 python3-httpx python3-rich"

do_build() {
    # Build wheel from pyproject.toml
    python3 -m pip wheel --no-build-isolation --no-deps --wheel-dir dist .
}

do_install() {
    # Install wheel to DESTDIR — creates /usr/bin/letx automatically
    python3 -m pip install --no-build-isolation --no-deps --no-index \
        --prefix=/usr --root="${DESTDIR}" dist/*.whl
    vlicense LICENSE
    vdoc README.md
}
```

> **Note:** `setup.py` shim is required in the repo root. Without it, `do_build` will fall back to `python3 setup.py build` which fails on `pyproject.toml`-only projects.

### Update Checksum (Required on Every Release)

```bash
cd ~/void-packages
./xbps-src fetch letx
sha256sum $XBPS_SRCDISTDIR/letx-0.1.2.tar.gz
# → copy the hash into the 'checksum' field in srcpkgs/letx/template
```

### Build and Test

```bash
cd ~/void-packages

# Build
./xbps-src pkg letx

# Inspect package contents
./xbps-src show-files letx

# Register and install locally
xbps-rindex -a hostdir/binpkgs/letx-*.xbps
sudo xbps-install --repository=/home/$USER/void-packages/hostdir/binpkgs letx

# Verify
letx --help
letx -v
letx search discord
```

### Pre-submission Checklist

- [ ] `checksum` updated to match the new tarball
- [ ] `revision=1` if `version` changed; increment `revision` only if version unchanged
- [ ] `setup.py` shim is present in the repo root
- [ ] All runtime deps available in Void repo: `python3-httpx`, `python3-rich`
- [ ] `python3-packaging-bootstrap` added to `hostmakedepends` (suppresses packaging warning)
- [ ] `./xbps-src pkg letx` completes without errors
- [ ] `/usr/bin/letx` present in `./xbps-src show-files letx` output
- [ ] Manual test: `letx search`, `letx info`, `letx list`, `letx get` all work correctly

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `httpx` | ≥ 0.27 | HTTP client for GitHub API requests |
| `rich` | ≥ 13.0 | Pretty terminal output (tables, panels, colors) |
| `argparse` | stdlib | CLI argument parsing (no install needed) |

**Build dependencies (xbps-src):**

| Package | Purpose |
|---|---|
| `python3-setuptools` | Build backend |
| `python3-wheel` | Wheel packaging |
| `python3-pip` | Installation into DESTDIR |
| `python3-packaging-bootstrap` | Dependency verification during packaging |

**Dev dependencies:**

| Package | Purpose |
|---|---|
| `pytest` | Test runner |
| `pytest-httpx` | Mock HTTP requests in unit tests |

---

## Roadmap

### v0.1.0 — Core Features ✅
- [x] `letx search` — search by name
- [x] `letx info` — package details
- [x] `letx list` — list all packages
- [x] `letx get` — download template locally
- [x] `letx update` — refresh index cache
- [x] Local cache with 1-hour TTL
- [x] Graceful offline degradation (use stale cache)
- [x] Bash installation script
- [x] xbps-src package template

### v0.1.1 — English Conversion ✅
- [x] All user-facing strings converted from Indonesian to English
- [x] CLI migrated from `typer` to `argparse` (stdlib, no extra deps)
- [x] Build system migrated from `hatchling` to `setuptools`
- [x] `setup.py` shim added for xbps-src compatibility
- [x] Binary renamed from `let` to `letx` (avoid bash builtin conflict)

### v0.1.2 — Enhanced Search & Info ✅
- [x] Fix: search false positives (restrict fields to `name` + `description`)
- [x] `[ERROR] No Options` on bare commands
- [x] `letx search "description"` — search by description field
- [x] `letx search -t <pkg>` — find local templates (core → extra → multilib)
- [x] `letx info all|core|extra|multilib` — top 20 most recently added
- [x] `letx info -c <category>` — full list by category
- [x] `letx info -t <pkg>` — local template detail panel
- [x] `letx list all|core|extra|multilib` — top 20 most recently added
- [x] `letx list -c <category>` — full list by category
- [x] `letx list -p [category]` — package count statistics

### v0.2.0 — xbps-src Integration 🔜
- [ ] `letx build <pkg>` — build via `xbps-src pkg`
- [ ] Auto-symlink template to `void-packages/srcpkgs/`
- [ ] Detect and configure `void-packages` directory
- [ ] Real-time build output streaming
- [ ] `letx search -x <pkg>` — search built `.xbps` files in local binpkgs

### v0.3.0 — Full Install Pipeline 🔜
- [ ] `letx install <pkg>` — build + install via `xbps-install`
- [ ] `letx remove <pkg>` — remove local template
- [ ] Dependency resolution between VUR packages

### v1.0.0 — Polish
- [ ] `letx upgrade` — update all locally fetched templates
- [ ] Shell completion (bash, zsh, fish)
- [ ] Man page (`letx.1`)
- [ ] User config via `~/.config/letx/config.toml`

---

*Let-X v0.1.2 — VUR: [github.com/T4n-Labs/vur](https://github.com/T4n-Labs/vur)*
