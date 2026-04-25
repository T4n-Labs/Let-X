# Let-X — Documentation for Developers

> **Let-X** is a CLI tool for Void Linux that makes it easy to search for, manage, and retrieve package templates from the **VUR (Void User Repository)** — a concept similar to AUR Helper in Arch Linux.

## Table of Contents
**For Developers**
- [Let-X — Documentation for Developers](#let-x--documentation-for-developers)
  - [Table of Contents](#table-of-contents)
- [For Developers](#for-developers)
  - [Project Architecture](#project-architecture)
  - [Directory Structure](#directory-structure)
  - [Module Description](#module-description)
    - [`config.py`](#configpy)
    - [`repo/index.py`](#repoindexpy)
    - [`repo/fetch.py`](#repofetchpy)
    - [`ops/search.py`](#opssearchpy)
    - [`ops/info.py`](#opsinfopy)
    - [`utils/print.py`](#utilsprintpy)
  - [Data Flow](#data-flow)
    - [`let search <keyword>`](#let-search-keyword)
    - [`let get <package>`](#let-get-package)
  - [How to Contribute](#how-to-contribute)
    - [Setting Up the Development Environment](#setting-up-the-development-environment)
    - [Code Conventions](#code-conventions)
    - [Adding a New Command](#adding-a-new-command)
  - [Running Tests](#running-tests)
  - [Build xbps-src Package](#build-xbps-src-package)
    - [Preparation](#preparation)
    - [Update Checksum (Required for Every Release)](#update-checksum-required-for-every-release)
    - [Build and Test](#build-and-test)
    - [Checklist Before Submitting to Void Packages](#checklist-before-submitting-to-void-packages)
  - [Roadmap](#roadmap)
    - [v0.1.0 — Basic Phase](#v010--basic-phase)
    - [v0.2.0 — xbps-src Integration](#v020--xbps-src-integration)
    - [v0.3.0 — Full Installation](#v030--full-installation)
    - [v1.0.0 — Advanced Features](#v100--advanced-features)
  - [Dependencies](#dependencies)
  - [License](#license)

# For Developers

## Project Architecture

Let-X is built on the philosophy of **separation of concerns** — each layer has clear, independent responsibilities:

```
┌─────────────────────────────────────────┐
│              CLI (cli.py)               │  ← Typer: parse arguments, output to user
├────────────────────┬────────────────────┤
│     ops/           │     repo/          │  ← Business logic vs. data access
│  search.py         │  index.py          │
│  info.py           │  fetch.py          │
├────────────────────┴────────────────────┤
│              utils/print.py             │  ← Rich: output presentation
├─────────────────────────────────────────┤
│              config.py                  │  ← Constants, paths, URLs
└─────────────────────────────────────────┘
```

**Key principle:**
- `cli.py` must not contain logic — it only orchestrates calls to `ops/` and `repo/`
- `ops/` knows nothing about HTTP — that’s `repo/`’s job
- `repo/` knows nothing about the UI — that’s `utils/`’s job
- `config.py` does not import any modules from this project

## Directory Structure

```
Let-X/                            ← Project root
├── letx/                        ← Main Python package
│   ├── __init__.py             ← App version (APP_VERSION)
│   ├── cli.py                  ← CLI entry point (Typer)
│   ├── config.py               ← All constants & paths
│   │
│   ├── repo/                   ← Data access layer (GitHub)
│   │   ├── __init__.py
│   │   ├── index.py            ← Fetch & cache packages.json
│   │   └── fetch.py            ← Download template folder via GitHub API
│   │
│   ├── ops/                    ← Business logic layer
│   │   ├── __init__.py
│   │   ├── search.py           ← Filter, sort, list packages
│   │   └── info.py             ← Details of a single package + local status
│   │
│   └── utils/                  ← Utilities
│       ├── __init__.py
│       └── print.py            ← Rich output (tables, panels, colors)
│
├── tests/                      ← Unit tests
│   ├── __init__.py
│   └── test_search.py          ← Test index, search, list
│
├── xbps-template/              ← xbps-src template for packaging
│   ├── let/
│   │   └── template            ← xbps-src template file
│   └── README.md               ← Build guide via xbps-src
│
├── install.sh                  ← Bash installation script
├── pyproject.toml              ← Project & dependency configuration
└── README.md                   ← Brief overview
```

## Module Description

### `config.py`

The only file that defines all global constants. **It must not be imported by other files except via `from let.config import ...`**.

```python
# Remote URL
VUR_REPO     = "T4n-Labs/vur"
VUR_API_BASE = "https://api.github.com/repos/T4n-Labs/vur/contents"
PACKAGES_URL = "https://raw.githubusercontent.com/T4n-Labs/vur/main/packages.json"

# Local path
CONFIG_DIR = Path.home() / ".config" / "letx"
CACHE_DIR  = Path.home() / ".cache" / "letx"
TEMPLATE_DIRS = {
    "core":     CONFIG_DIR / "core",
    "extra":    CONFIG_DIR / "extra",
    "multilib": CONFIG_DIR / "multilib",
}

CACHE_TTL = 3600  # seconds (1 hour)
```

**To change the cache location or TTL**, simply edit `config.py` — all other modules will automatically follow.

### `repo/index.py`

Responsible for fetching and caching `packages.json` from GitHub.

**Public functions:**

| Function | Signature | Description |
|---|---|---|
| `fetch_index` | `(force: bool = False) → list[Package]` | Fetch all packages (from cache or GitHub) |
| `get_package` | `(name: str, force: bool = False) → Package \| None` | Retrieve a single package by name |
| `cache_info` | `() → dict` | Current cache status |

**Cache logic:**
```
fetch_index() is called
    │
    ├─ Is the cache present AND age < TTL AND force=False?
    │   └─ Return data from the local cache
    │
    └─ Otherwise:
        ├─ Fetch from GitHub
        ├─ Write to cache
        └─ return new data
            │
            └─ If fetch FAILS but old cache exists:
                └─ return old cache (graceful degradation)
```

### `repo/fetch.py`

Responsible for downloading the entire package template folder from GitHub using the **GitHub Contents API** (no need to have `git` or `svn` installed).

**Public functions:**

| Function | Signature | Description |
|---|---|---|
| `download_package` | `(pkg_path, category, pkg_name, progress_cb) → Path` | Download the package folder from VUR |
| `package_exists_locally` | `(category, pkg_name) → bool` | Check if the template exists locally |
| `local_package_path` | `(category, pkg_name) → Path \| None` | Local package path if available |

**Fetch strategy:**
```
GitHub Contents API
GET /repos/T4n-Labs/vur/contents/extra/discord
    │
    └─ Response: list of {type, name, path, ...}
        │
        ├─ type == “file”  → download via raw.githubusercontent.com
        └─ type == “dir”   → recursion into subdirectories
```

**Why the GitHub Contents API, not `git clone` or `svn`?**
- Does not require `git` or `svn` to be installed
- Only downloads the necessary files (not the entire repo)
- More portable and predictable
- Trade-off: more HTTP requests for folders with many files

### `ops/search.py`

All search and listing operations are performed here, **completely offline** once the index is cached.

**Public functions:**

| Function | Signature | Description |
|---|---|---|
| `search_packages` | `(keyword, category=None) → list[Package]` | Search for packages, optionally filter by category |
| `list_packages` | `(category=None) → list[Package]` | List all packages |
| `available_categories` | `() → list[str]` | List of available categories |

**Search fields:**
- `name` — package name
- `maintainer` — maintainer’s name/email
- `homepage` — homepage URL

**Search result ranking algorithm:**
```python
def _rank(pkg) -> int:
    name = pkg[“name”].lower()
    if name == keyword:       return 0  # exact match → top of list
    if name.startswith(kw):   return 1  # prefix match
    if kw in name:            return 2  # contains match
    return 3                            # match in other fields
```

### `ops/info.py`

Combines data from the (remote) index with local status.

```python
def get_info(name: str) -> dict | None:
    pkg = get_package(name)          # from index.py
    is_local = package_exists_locally(category, name)   # from fetch.py
    local_path = local_package_path(category, name)     # from fetch.py
    return {**pkg, “installed_locally”: is_local, “local_path”: str(local_path)}
```

### `utils/print.py`

All output to the terminal must go through a function here. **Never `print()` directly from other modules.**

**Available functions:**

| Function | Description |
|---|---|
| `print_package_table(packages, title)` | Rich table for a list of packages |
| `print_package_info(info)` | Rich panel for details of a single package |
| `print_success(msg)` | `✔ message` (green) |
| `print_error(msg)` | `✘ message` (red) to stderr |
| `print_info(msg)` | `→ message` (cyan) |
| `print_warn(msg)` | `! message` (yellow) |

**Theme colors:**
```python
C_NAME  = “bold cyan”    # package name
C_VER   = “green”        # version
C_CAT   = “yellow”       # category
C_MAINT = “dim white”    # maintainer
C_LOCAL = “bold green”   # local availability status
```

## Data Flow

Here is the complete flow for each command:

### `let search <keyword>`

```
cli.py:cmd_search(keyword)
    │
    └─► ops/search.py:search_packages(keyword)
            │
            └─► repo/index.py:fetch_index()
                    │
                    ├─ Is the cache valid? → read ~/.cache/let/packages.json
                    └─ Is the cache expired? → GET packages.json from GitHub
                                         write to cache
            │
            └─ Filter & sort results
    │
    └─► utils/print.py:print_package_table(results)
```

### `let get <package>`

```
cli.py:cmd_get(name)
    │
    ├─► ops/info.py:get_info(name)          ← check index + local status
    │
    ├─ Already exists locally & no --force? → print warning, exit
    │
    └─► repo/fetch.py:download_package(path, category, name)
            │
            └─► GitHub Contents API (recursive)
                    │
                    ├─ Each file → GET raw.githubusercontent.com
                    └─ Write to ~/.config/let/<category>/<name>/
    │
    └─► utils/print.py:print_success(dest)
```

## How to Contribute

### Setting Up the Development Environment

```bash
# 1. Fork and clone the repo
git clone https://github.com/<username>/Let-X
cd Let-X

# 2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install in development mode
pip install -e “.[dev]”

# 4. Verify the installation
letx --help
pytest tests/ -v
```

### Code Conventions

**Naming:**
- Modules and functions: `snake_case`
- Constants in `config.py`: `SCREAMING_SNAKE_CASE`
- Type hints are required for all public functions

**Import order** (follow the `isort` standard):
```python
# 1. stdlib
from pathlib import Path
from typing import Any

# 2. third-party
import httpx
from rich.console import Console

# 3. internal (absolute imports)
from letx.config import CACHE_DIR
from letx.repo.index import fetch_index
```

**Docstring:** All public functions must have a docstring explaining their arguments, return values, and exceptions.

```python
def fetch_index(force: bool = False) -> list[Package]:
    “”"
    Fetch package indexes from VUR.

    Args:
        force: If True, bypass the cache and re-fetch from GitHub.

    Returns:
        List of package dictionaries from packages.json

    Raises:
        RuntimeError: If the fetch fails and there is no local cache.
    “”"
```

### Adding a New Command

1. Add the command function to `cli.py` using the `@app.command(“name”)` decorator
2. Business logic goes into `ops/` (not in `cli.py`)
3. Data access goes into `repo/` (not in `ops/`)
4. Output is always via `utils/print.py`
5. Write unit tests in `tests/`

Example of a new command skeleton:

```python
# cli.py
@app.command(“remove”)
def cmd_remove(
    name: Annotated[str, typer.Argument(help=“Package name”)],
) -> None:
    “”“Remove the package template from the local directory.”“”
    from let.ops.remove import remove_package   # create a new module
    result = remove_package(name)
    if result:
        print_success(f“Template ‘{name}’ removed.”)
    else:
        print_error(f“Template ‘{name}’ not found.”)
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run a specific test
pytest tests/test_search.py -v

# With coverage report
pytest tests/ --cov=let --cov-report=term-missing
```

**Testing using a monkeypatch** — no internet connection during testing:

```python
@pytest.fixture
def fake_cache(tmp_path, monkeypatch):
    “”“Replace PACKAGES_CACHE with a temp file containing mock data.”“”
    cache_file = tmp_path / “packages.json”
    cache_file.write_text(json.dumps(MOCK_PACKAGES))
    monkeypatch.setattr(“let.repo.index.PACKAGES_CACHE”, cache_file)
    monkeypatch.setattr(“let.repo.index.CACHE_TTL”, 9999)
```

**Available tests:**

| Test | Description |
|---|---|
| `test_fetch_index_from_cache` | Index read from local cache |
| `test_get_package_found` | Search for existing package |
| `test_get_package_case_insensitive` | Case-insensitive search |
| `test_get_package_not_found` | Package not found → returns None |
| `test_search_by_name` | Exact name search |
| `test_search_partial` | Partial name search |
| `test_search_with_category_filter` | Filter by category |
| `test_search_no_results` | Keyword does not match → empty list |
| `test_list_all` | List all packages |
| `test_list_by_category` | List filtered by category |
| `test_available_categories` | List of unique categories |

## Build xbps-src Package

To distribute Let as an official `.xbps` package:

### Preparation

```bash
# Setup void-packages
git clone https://github.com/void-linux/void-packages ~/void-packages
cd ~/void-packages
./xbps-src binary-bootstrap

# Copy template
mkdir srcpkgs/letx/
cp /path/to/Let-X/xbps-template/template srcpkgs/letx/
```

### Update Checksum (Required for Every Release)

```bash
# After creating a GitHub Release with tag vX.Y.Z
cd ~/void-packages
./xbps-src fetch letx
sha256sum $XBPS_SRCDISTDIR/let-X.Y.Z.tar.gz
# → Copy the hash to the ‘checksum’ field in srcpkgs/let/template
```

### Build and Test

```bash
cd ~/void-packages

# Build
./xbps-src pkg letx

# Check package contents
./xbps-src show-files letx

# Install locally for testing
sudo xbps-install --repository=hostdir/binpkgs letx

# Verify
letx --help
letx search discord
```

### Checklist Before Submitting to Void Packages

- [ ] `checksum` has been updated to match the latest tarball
- [ ] `revision` is reset to `1` if `version` changes
- [ ] `revision` is incremented if only the template has changed (same version)
- [ ] All Python dependencies (`python3-httpx`, `python3-rich`, `python3-typer`) are available in void-packages
- [ ] `./xbps-src pkg letx` succeeds without errors
- [ ] `./xbps-src show-files letx` shows `/usr/bin/letx` in the output
- [ ] Manual test: `letx search`, `letx info`, `letx list`, `letx get` work

## Roadmap

### v0.1.0 — Basic Phase
- [x] `letx search` — package search
- [x] `letx info` — package details
- [x] `letx list` — list all packages
- [x] `letx list --category` — filter by category
- [x] `letx get` — download local template
- [x] `letx update` — refresh index cache
- [x] Local cache with 1-hour TTL
- [x] Graceful degradation when offline (uses old cache)
- [x] Bash installation script
- [x] xbps-src template

### v0.2.0 — xbps-src Integration
- [ ] `letx build <package>` — build via `xbps-src pkg`
- [ ] Auto-setup symlink to `void-packages/srcpkgs/`
- [ ] Detection and configuration of the `void-packages` directory
- [ ] Real-time build progress output

### v0.3.0 — Full Installation
- [ ] `letx install <package>` — build + install via `xbps-install`
- [ ] `letx remove <package>` — remove local template
- [ ] Dependency management between VUR packages

### v1.0.0 — Advanced Features
- [ ] `letx upgrade` — update all templates that have been fetched
- [ ] Full offline mode
- [ ] User configuration via `~/.config/letx/config.toml`
- [ ] Shell completion (bash, zsh, fish)
- [ ] Man page (`letx.1`)

## Dependencies

| Package | Version | Function |
|---|---|---|
| `typer[all]` | ≥ 0.12 | CLI framework (argument parsing, help text) |
| `httpx` | ≥ 0.27 | HTTP client for fetching GitHub API |
| `rich` | ≥ 13.0 | Pretty terminal output (tables, panels, colors) |

**Dev dependencies:**
| Package | Function |
|---|---|
| `pytest` | Test runner |
| `pytest-httpx` | Mock HTTP requests for unit tests |

## License

Let is released under the **BSD 2-Clause** license. See the `LICENSE` file for full details.

*This documentation is for Let v0.1.0*
*VUR: [github.com/T4n-Labs/vur](https://github.com/T4n-Labs/vur)*

---
* @T4n-Labs
* @Gh0sT4n