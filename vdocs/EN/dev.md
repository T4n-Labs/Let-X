# Let-X — Developer Guide

> Technical documentation for contributors and maintainers of **Let-X v0.2.0**.

## Table of Contents

- [Project Architecture](#project-architecture)
- [Directory Structure](#directory-structure)
- [Core Package](#core-package)
- [Module Reference](#module-reference)
- [Changes v0.1.2 → v0.2.0](#changes-v012--v020)
- [xbps-src Integration Architecture](#xbps-src-integration-architecture)
- [Data Flow](#data-flow)
- [Setting Up a Development Environment](#setting-up-a-development-environment)
- [Code Conventions](#code-conventions)
- [Adding a New Command](#adding-a-new-command)
- [Running Tests](#running-tests)
- [Building via xbps-src](#building-via-xbps-src)
- [Dependencies](#dependencies)
- [Notes for Future Development](#notes-for-future-development)

## Project Architecture

Let-X follows a strict **separation of concerns** — each layer has one clear responsibility:

```
┌──────────────────────────────────────────────────────┐
│                    CLI (cli.py)                      │  argparse: parse args, route to handlers
├────────────────────┬─────────────────────────────────┤
│       ops/         │          repo/                  │  business logic vs data access
│  search.py         │      index.py                   │
│  info.py           │      fetch.py                   │
├────────────────────┴─────────────────────────────────┤
│                 utils/print.py                       │  Rich: all terminal output
│                 utils/xbps.py                        │  xbps-src wrapper (new in v0.2.0)
├──────────────────────────────────────────────────────┤
│                  config.py                           │  constants, paths, URLs
└──────────────────────────────────────────────────────┘
         ↓
┌──────────────────────────────────────────────────────┐
│               backend/ (xbps-src)                    │  vanilla void-packages, unmodified
│   srcpkgs/         → base-files, base-chroot         │  (bootstrap/internal use only)
│   common/          → build-style, hooks, chroot-style│
│   xbps-src         → main script                     │
└──────────────────────────────────────────────────────┘
```

**Key principles:**
- `cli.py` contains no logic — it only orchestrates calls to `ops/` and `repo/`
- `ops/` has no knowledge of HTTP — that belongs to `repo/`
- `repo/` has no knowledge of display — that belongs to `utils/`
- `config.py` does not import any other module from this project
- `utils/xbps.py` is the only module allowed to call xbps-src subprocesses

## Directory Structure

```
Let-X/
├── letx/
│   ├── __init__.py
│   ├── cli.py                          ← CLI entry point
│   ├── config.py                       ← All constants and paths
│   │
│   ├── backend/                        ← xbps-src (vanilla void-packages)
│   │   ├── xbps-src                    ← Main xbps-src script
│   │   ├── srcpkgs/                    ← BACKEND ONLY: base-files, base-chroot
│   │   │   ├── base-chroot/
│   │   │   └── base-files/
│   │   ├── common/
│   │   │   ├── build-style/            ← Build system scripts (cmake, cargo, etc.)
│   │   │   ├── chroot-style/           ← Chroot scripts
│   │   │   │   ├── uunshare.sh         ← Default (unmodified)
│   │   │   │   ├── bwrap.sh
│   │   │   │   ├── letx.sh             ← NEW: custom chroot for VUR builds
│   │   │   │   └── ...
│   │   │   ├── environment/
│   │   │   ├── hooks/
│   │   │   └── ...
│   │   ├── etc/
│   │   └── root-git/                   ← Renamed .git/ (GIT_DIR fix)
│   │
│   ├── ops/
│   │   ├── search.py                   ← Search, list, count packages
│   │   └── info.py                     ← Package detail + local template info
│   │
│   ├── repo/
│   │   ├── index.py                    ← Fetch & cache packages.json from VUR
│   │   └── fetch.py                    ← Download templates via GitHub API
│   │
│   └── utils/
│       ├── print.py                    ← All Rich output
│       └── xbps.py                     ← xbps-src wrapper (NEW in v0.2.0)
│
├── install.sh
├── pyproject.toml
└── tests/
```


## Core Package
Information : https://github.com/T4n-Labs/Let-X/tree/core

## Module Reference

### `config.py`

All constants and paths. **No other module should be imported here** — only stdlib.

```python
# Key paths
BACKEND_DIR          # letx/backend/
XBPS_SRC_PATH        # letx/backend/xbps-src
BACKEND_GIT_DIR      # letx/backend/root-git/ (GIT_DIR fix)
BACKEND_SRCPKGS_DIR  # letx/backend/srcpkgs/ (base-files, base-chroot ONLY)

CONFIG_DIR           # ~/.config/letx/
CACHE_DIR            # ~/.cache/letx/
TEMPLATE_DIRS        # {"core": ..., "extra": ..., "multilib": ...}
LETX_MASTERDIR       # ~/.config/letx/masterdir/
LETX_CHROOT_SRCPKGS  # ~/.config/letx/masterdir/letx-srcpkgs/
LETX_HOSTDIR         # ~/.config/letx/hostdir/
LETX_SRCPKGS_DIR     # ~/.config/letx/srcpkgs/ (legacy, kept for compatibility)
```

### `utils/xbps.py`

The xbps-src wrapper. Responsible for all interactions with xbps-src.

| Function                               | Responsibility                                       |
|----------------------------------------|------------------------------------------------------|
| `run(args)`                            | Main entry point called from `cli.py`                |
| `find_template(pkgname)`               | Loop `core → extra → multilib`, return `(cat, path)` |
| `stage_vur_template(pkgname, pkg_dir)` | Copy + patch template to `masterdir/letx-srcpkgs/`   |
| `build_xbps_env(...)`                  | Build environment dict for xbps-src subprocess       |
| `_run_with_template(...)`              | Run xbps-src for `CMDS_NEED_PKG`                     |
| `_run_xbps_raw(...)`                   | Forward args directly to xbps-src for `CMDS_NO_PKG`  |
| `_parse_args(args)`                    | Identify target, pkgname, and xbps_options           |

## Changes v0.1.2 → v0.2.0

### 1. Backend Added (`letx/backend/`)

**v0.1.2:** No backend. `letx -x` did not exist.

**v0.2.0:** xbps-src (vanilla void-packages) is bundled at `letx/backend/`. Changes from upstream void-packages:
- `backend/srcpkgs/` **only contains** `base-files/` and `base-chroot/` — no regular package templates
- `.git/` is renamed to `root-git/` to avoid conflicts with Let-X's own `.git/`
- `common/chroot-style/letx.sh` **added** (see next section)

`pyproject.toml` updated to bundle backend files:
```toml
[tool.setuptools.package-data]
letx = [
    "backend/xbps-src",
    "backend/srcpkgs/**/*",
    "backend/common/**/*",
    "backend/common/*",
    "backend/etc/**/*",
    "backend/root-git/**/*",
    "backend/root-git/*",
]
```

### 2. Shell Script `letx.sh` — Custom Chroot Style

**File:** `letx/backend/common/chroot-style/letx.sh`

**Problem it solves:**

xbps-src uses `uunshare.sh` by default to set up the chroot namespace. VUR templates live at `~/.config/letx/extra/<pkg>/` which is **not mounted** inside the chroot. The chroot only mounts two paths:
```
LETX_MASTERDIR  →  /               (chroot root)
BACKEND_DIR     →  /void-packages/ (xbps-src backend)
```

The original `uunshare.sh`:
```bash
exec xbps-uunshare $EXTRA_ARGS -b $DISTDIR:/void-packages ...
#                  ^^^^^^^^^^^
#                  EXTRA_ARGS here → overwritten by DISTDIR mount
```

The mount order is broken: `EXTRA_ARGS` (our VUR srcpkgs bind mount) is processed **before** DISTDIR. In a Linux mount namespace, mounting DISTDIR onto `/void-packages/` replaces the entire subtree, including any mounts already applied under `/void-packages/srcpkgs/`.

**`letx.sh` reverses the order:**
```bash
exec xbps-uunshare \
    -b $DISTDIR:/void-packages \   ← DISTDIR first
    ${HOSTDIR:+-b $HOSTDIR:/host} \
    $EXTRA_ARGS \                  ← EXTRA_ARGS after (overlays on top of DISTDIR)
    -- $MASTERDIR $CMD $@
```

**Activated** in `xbps.py` via:
```python
env["XBPS_CHROOT_CMD"] = "letx"
env["XBPS_CHROOT_CMD_ARGS"] = f"-b {LETX_CHROOT_SRCPKGS}:void-packages/srcpkgs"
```

### 3. VUR Template Staging System

**Problem:** VUR templates at `~/.config/letx/extra/zig/` are not accessible from inside the chroot. The solution uses `masterdir/letx-srcpkgs/` as a staging area that is **always accessible** inside the chroot as `/letx-srcpkgs/`.

**Staging flow:**
```
SOURCE: ~/.config/letx/extra/zig/template     (never modified)
           ↓  stage_vur_template()
STAGED: ~/.config/letx/masterdir/letx-srcpkgs/zig/template  (patched copy)
           ↓  bind-mount via letx.sh EXTRA_ARGS
CHROOT: /void-packages/srcpkgs/zig/template   (xbps-src reads from here)
```

**Patch applied during staging:**

xbps-src calls `${pkgname}_package()` for all packages in `xbps-src-doinstall.sh`. VUR templates following the standard void-packages convention are not required to define this function for single-package templates. Let-X automatically injects a default no-op:

```bash
# Auto-injected by Let-X
zig_package() { :; }
```

**The original template is never modified.** The patch only exists in the staged copy at `masterdir/letx-srcpkgs/`.

### 4. GIT_DIR Fix

`root-git/` is `.git/` renamed. xbps-src calls `git symbolic-ref` to detect branch info. Without this fix, `fatal: not a git repository` appears after a wheel install because `.git/` is excluded from Python wheels by default.

```python
# In build_xbps_env():
if BACKEND_GIT_DIR.is_dir():
    env["GIT_DIR"]       = str(BACKEND_GIT_DIR)
    env["GIT_WORK_TREE"] = str(BACKEND_DIR)
else:
    # Wheel install: root-git not present, unset to avoid inheriting wrong GIT_DIR
    env.pop("GIT_DIR",       None)
    env.pop("GIT_WORK_TREE", None)
```

### 5. XBPS_SRCPKGDIR Split

**v0.1.2:** Single srcpkgs directory for all purposes.

**v0.2.0:** Two srcpkgs directories with distinct roles:

| Path                                              | Used for                                                     |
|---------------------------------------------------|--------------------------------------------------------------|
| `BACKEND_SRCPKGS_DIR` (`backend/srcpkgs/`)        | Bootstrap only: `binary-bootstrap`, `zap`, `bootstrap`, etc. |
| `LETX_CHROOT_SRCPKGS` (`masterdir/letx-srcpkgs/`) | VUR package builds: `pkg`, `build`, `fetch`, etc.            |

---

## xbps-src Integration Architecture

### Two xbps-src Instances

Every `letx -x pkg <name>` runs **two xbps-src instances** that each require different configuration:

```
[HOST] outer xbps-src
  ├── Reads XBPS_SRCPKGDIR from Python env var
  │   → LETX_CHROOT_SRCPKGS (host absolute path)
  ├── setup_pkg() → sources the template
  └── chroot_handler()
        ↓ uunshare via letx.sh
        ↓ bind mounts applied:
        │   BACKEND_DIR          → /void-packages/
        │   LETX_MASTERDIR       → /
        │   LETX_CHROOT_SRCPKGS  → /void-packages/srcpkgs/  ← overlay
        ↓
[CHROOT] inner xbps-src (IN_CHROOT=1)
  ├── Environment cleared by env -i
  ├── XBPS_SRCPKGDIR = /void-packages/srcpkgs/ (default from XBPS_DISTDIR)
  └── /void-packages/srcpkgs/zig/template → accessible ✓
```

### Command Routing

```python
CMDS_NEED_PKG  →  _run_with_template()
  # 1. find_template(): loop core → extra → multilib
  # 2. stage_vur_template(): copy + inject _package()
  # 3. env["XBPS_CHROOT_CMD"] = "letx"
  # 4. env["XBPS_CHROOT_CMD_ARGS"] = bind mount command
  # 5. subprocess: BACKEND_DIR/xbps-src pkg <name>

CMDS_NO_PKG    →  _run_xbps_raw()
  # XBPS_SRCPKGDIR = BACKEND_SRCPKGS_DIR (base-files, base-chroot)
  # subprocess: BACKEND_DIR/xbps-src <target>
```

## Data Flow

### `letx search <keyword>`

```
cli.py:cmd_search()
    │
    ├─ ops/search.py:search_packages()
    │       │
    │       └─ repo/index.py:fetch_index()
    │               ├─ cache valid → read ~/.cache/letx/packages.json
    │               └─ expired     → GET GitHub raw → write cache
    │
    └─ utils/print.py:print_package_table()
```

### `letx get <pkg>`

```
cli.py:cmd_get()
    │
    ├─ ops/info.py:get_info()           → check index + local status
    ├─ Already local & no --force?      → print_warn(), exit 0
    └─ repo/fetch.py:download_package()
            │
            └─ GitHub Contents API (recursive)
                    ├─ each file → GET raw.githubusercontent.com
                    └─ write to ~/.config/letx/<category>/<pkg>/
```

### `letx -x pkg <name>`

```
cli.py:cmd_xbps()
    │
    └─ utils/xbps.py:run()
            │
            └─ _run_with_template()
                    │
                    ├─ find_template()          → loop core/extra/multilib
                    ├─ stage_vur_template()     → masterdir/letx-srcpkgs/<pkg>/
                    ├─ build_xbps_env()         → set XBPS_CHROOT_CMD=letx
                    │                              set XBPS_CHROOT_CMD_ARGS
                    └─ subprocess: backend/xbps-src pkg <name>
                            │
                            └─ chroot via letx.sh
                                    │
                                    └─ inner xbps-src
                                            └─ /void-packages/srcpkgs/<pkg>/ ✓
```

## Setting Up a Development Environment

```bash
# 1. Clone the repository
git clone https://github.com/T4n-Labs/Let-X
cd Let-X

# 2. Install in editable mode
pip install -e ".[dev]"

# 3. Verify
letx --version
letx --help

# 4. Set up the build environment (for testing letx -x)
letx -x binary-bootstrap
```

> **Note on editable installs:** `BACKEND_DIR` points to `letx/backend/` inside the source tree (writable). Changes to `letx.sh` or any other backend file take effect immediately without reinstalling.

## Code Conventions

**Naming:**
- Modules and functions: `snake_case`
- Constants in `config.py`: `SCREAMING_SNAKE_CASE`
- Type hints are required for all public functions

**Import order:**
```python
# 1. stdlib
import os
import sys
from pathlib import Path

# 2. third-party
import httpx
from rich.console import Console

# 3. internal (always absolute imports)
from letx.config import CACHE_DIR
from letx.repo.index import fetch_index
```

**Docstrings — required for all public functions:**
```python
def find_template(pkgname: str) -> tuple[str, Path] | None:
    """
    Search for a VUR template across all three categories.

    Loop order: core → extra → multilib

    Args:
        pkgname: package name, e.g. 'zig'

    Returns:
        (category, pkg_dir) if found, None otherwise.
    """
```

## Adding a New Command

1. Add a subparser in `cli.py:build_parser()`
2. Add a `cmd_<name>()` handler in `cli.py`
3. Register it in the dispatch block inside `main()`
4. Business logic goes into `ops/` (not `cli.py`)
5. Data access goes into `repo/` (not `ops/`)
6. All output goes through `utils/print.py`

**Skeleton:**
```python
# In build_parser():
p_remove = sub.add_parser("remove", help="Remove a local template")
p_remove.add_argument("name", help="Package name")

# Handler in cli.py:
def cmd_remove(args: argparse.Namespace) -> int:
    from letx.ops.remove import remove_template
    removed = remove_template(args.name)
    if removed:
        print_success(f"Template '{args.name}' removed.")
        return 0
    print_error(f"Template '{args.name}' not found locally.")
    return 1

# In main():
elif args.command == "remove":
    sys.exit(cmd_remove(args))
```

## Running Tests

```bash
pytest tests/ -v
pytest tests/test_search.py -v
pytest tests/ --cov=letx --cov-report=term-missing
```

Tests use `monkeypatch` — no internet connection required:

```python
@pytest.fixture
def fake_cache(tmp_path, monkeypatch):
    cache_file = tmp_path / "packages.json"
    cache_file.write_text(json.dumps(MOCK_PACKAGES))
    monkeypatch.setattr("letx.repo.index.PACKAGES_CACHE", cache_file)
    monkeypatch.setattr("letx.repo.index.CACHE_TTL", 9999)
```

## Building via xbps-src

Let-X can now build itself using `letx -x`:

```bash
# From the Let-X directory
letx get letx            # download the VUR letx template
letx -x pkg letx         # build

# Install
sudo xbps-install \
    --repository=$HOME/.config/letx/hostdir/binpkgs letx
```

For a new release, update the `checksum` in the VUR template after the source tarball changes:
```bash
sha256sum letx-0.2.0.tar.gz
# → update in the VUR template
```

## Dependencies

**Runtime:**

| Package    | Version | Purpose                    |
|------------|---------|----------------------------|
| `httpx`    | ≥ 0.27  | HTTP client for GitHub API |
| `rich`     | ≥ 13.0  | Pretty terminal output     |
| `argparse` | stdlib  | CLI argument parsing       |

**Dev:**

| Package        | Purpose            |
|----------------|--------------------|
| `pytest`       | Test runner        |
| `pytest-httpx` | Mock HTTP requests |

**System (for `letx -x`):**

| Binary          | Purpose                                 |
|-----------------|-----------------------------------------|
| `xbps-uunshare` | User namespace chroot (via xbps-tools)  |
| `xbps-create`   | Create binary packages                  |
| `xbps-rindex`   | Register packages to a local repository |

## Notes for Future Development

Several things to keep in mind for v0.3.0 and beyond:

### 1. Staging Cleanup

Currently `masterdir/letx-srcpkgs/<pkgname>/` is **never deleted** after a build completes. With many builds over time this directory will grow. Consider adding automatic cleanup after `proc.returncode == 0` in `_run_with_template()`.

### 2. `letx.sh` — Compatibility with Other Chroot Styles

`letx.sh` is written specifically for `xbps-uunshare`. If the system uses `bwrap` or `uchroot` (see `common/chroot-style/`), equivalent scripts are needed:
- `letx-bwrap.sh` for systems using bwrap
- Auto-detection of the available chroot style in `build_xbps_env()`

### 3. `_package()` Injection — Edge Cases

The current injection of `${pkgname}_package() { :; }` uses a simple string check (`f"{func_name}()" not in content`). This could produce a false positive if a comment in the template mentions the function name. Consider more robust bash parsing if this becomes an issue.

### 4. `LETX_SRCPKGS_DIR` (Legacy)

`~/.config/letx/srcpkgs/` still exists in `config.py` and `ensure_dirs()` as a legacy path. It can be removed in a future version if nothing depends on it.

### 5. Multi-package Templates (Subpackages)

Templates that define `$subpackages` (e.g. `discord` + `discord-devel`) have not been tested with the current staging system. `stage_vur_template()` only copies a single `pkgname/` directory — subpackage templates need to be handled as well.

*Let-X v0.2.0 · VUR: [github.com/T4n-Labs/vur](https://github.com/T4n-Labs/vur)*

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
