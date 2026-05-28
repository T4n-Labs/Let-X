# Let-X — User Guide

> **Let-X** is a CLI tool for Void Linux that makes it easy to search, manage, download, and build packages from **VUR (Void User Repository)** — similar to `yay` or `paru` on Arch Linux.

**Binary:** `letx` | **Version:** 0.2.0 | **Programming Language:** Python 3.11+

## Table of Contents

- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Commands](#commands)
  - [letx search](#letx-search)
  - [letx info](#letx-info)
  - [letx list](#letx-list)
  - [letx get](#letx-get)
  - [letx update](#letx-update)
  - [letx -x (xbps-src)](#letx--x-xbps-src)
- [Typical Workflow](#typical-workflow)
- [Local File Structure](#local-file-structure)
- [Troubleshooting](#troubleshooting)
- [Uninstall](#uninstall)

## System Requirements

| Component        | Requirement                          |
|------------------|--------------------------------------|
| Operating System | Void Linux (glibc)                   |
| Python           | 3.11 or newer                        |
| Internet         | Required to fetch index and templates|

## Installation

```bash
# 1. Clone the Let-X repository
git clone https://github.com/T4n-Labs/Let-X
cd Let-X

# 2. Run the install script as root
sudo ./install.sh
```

Verify the installation:
```bash
letx --version
letx --help
```

To uninstall:
```bash
sudo ./install.sh uninstall
```

## Commands

### `letx search`

Search for packages in VUR by name or description.

```bash
letx search <keyword>
letx search "<description>"
letx search <keyword> -c <category>
letx search -t <package_name>
```

| Option             | Description                                         |
|--------------------|-----------------------------------------------------|
| `-c`, `--category` | Filter by category: `core` \| `extra` \| `multilib` |
| `-t`, `--template` | Search for a template already downloaded locally    |

**Examples:**
```bash
letx search discord
letx search browser -c extra
letx search "Programming Language"
letx search -t discord          # check if already downloaded
```

### `letx info`

Show detailed package information.

```bash
letx info <package_name>
letx info all | core | extra | multilib
letx info -c <category>
letx info -t <package_name>
```

| Argument / Option | Description |
|-------------------|-------------|
| `<package_name>` | Full details for a specific package |
| `all / core / extra / multilib` | 20 most recently added packages |
| `-c`, `--category` | List all packages in a category |
| `-t`, `--template` | Show details of a local template |

**Examples:**
```bash
letx info discord
letx info all
letx info -c extra
letx info -t discord
```

### `letx list`

List packages from VUR.

```bash
letx list all | core | extra | multilib
letx list -c <category>
letx list -p [category]
```

| Argument / Option | Description |
|-------------------|-------------|
| `all / core / extra / multilib` | 20 most recently added packages |
| `-c`, `--category` | All packages in a specific category |
| `-p`, `--package` | Show package count statistics |

**Examples:**
```bash
letx list all
letx list -c core
letx list -p              # stats for all categories
letx list -p extra        # stats for one category
```

**Example statistics output:**
```
  VUR Package Statistics
 ──────────────────────
  Category   Packages
  core              3
  extra            17
  multilib          3
 ──────────────────────
  total            23
```

### `letx get`

Download a package template from VUR to your local machine.

```bash
letx get <package_name>
letx get <package_name> --force
```

| Option | Description |
|--------|-------------|
| `-f`, `--force` | Re-download even if the template already exists |

**Examples:**
```bash
letx get discord
letx get discord --force    # update template
```

Templates are saved to `~/.config/letx/<category>/<package_name>/`.

### `letx update`

Refresh the VUR package index cache.

```bash
letx update
```

> The cache refreshes automatically every hour. Use this command to force an immediate update.

---

### `letx -x` (xbps-src)

Direct integration with `xbps-src` to build and install packages from VUR templates.

```bash
letx -x <target> [package_name] [options]
```

#### First-time Setup (Required Once)

Before building any package, run `binary-bootstrap` once to prepare the build environment:

```bash
letx -x binary-bootstrap
```

> This process takes a few minutes and requires an internet connection. It only needs to be done **once**.

#### Building a Package

Once bootstrap is complete, build packages directly from VUR templates:

```bash
# Download the template first (if not already done)
letx get zig

# Build the package
letx -x pkg zig
```

Built packages are saved to `~/.config/letx/hostdir/binpkgs/`.

#### Installing a Built Package

```bash
sudo xbps-install --repository=$HOME/.config/letx/hostdir/binpkgs zig
```

#### Available Targets

| Target | Description |
|--------|-------------|
| `pkg <name>` | Full build + create `.xbps` package file |
| `fetch <name>` | Download source distfile only |
| `extract <name>` | Extract source archive |
| `build <name>` | Compile only |
| `install <name>` | Install to destdir |
| `clean <name>` | Clean build directory |
| `show <name>` | Show template info |
| `show-build-deps <name>` | Show build dependencies |
| `binary-bootstrap` | Set up build environment (once only) |
| `zap` | Reset/clean the masterdir |

**Examples:**
```bash
letx -x fetch zig           # download source
letx -x extract zig         # extract
letx -x build zig           # compile
letx -x pkg zig             # full build + package (most common)
letx -x show zig            # check template info
letx -x clean zig           # clean up after build
```

## Typical Workflow

### First Time Setup

```bash
# 1. Set up the build environment (once only)
letx -x binary-bootstrap

# 2. Refresh the VUR index
letx update
```

### Finding and Installing a Package

```bash
# 1. Search for a package
letx search discord

# 2. View details
letx info discord

# 3. Download the template
letx get discord

# 4. Build
letx -x pkg discord

# 5. Install
sudo xbps-install --repository=$HOME/.config/letx/hostdir/binpkgs discord
```

### Updating a Package

```bash
# Update the template to the latest version
letx get discord --force

# Rebuild
letx -x pkg discord

# Install the new version
sudo xbps-install --repository=$HOME/.config/letx/hostdir/binpkgs discord
```

## Local File Structure

```
~/.config/letx/
├── core/                    ← Templates from the core category
│   └── <package>/
│       ├── template
│       ├── files/
│       └── patches/
├── extra/                   ← Templates from the extra category
│   └── <package>/
├── multilib/                ← Templates from the multilib category
│   └── <package>/
├── masterdir/               ← xbps-src build environment
└── hostdir/
    └── binpkgs/             ← Built .xbps packages

~/.cache/letx/
└── packages.json            ← VUR index cache (auto-refreshed every hour)
```

## Troubleshooting

### `letx: command not found`
```bash
# Check if the file exists
ls -la /usr/bin/letx

# If missing, reinstall
sudo ./install.sh
```

### `Failed to fetch index from GitHub`

Internet connection issue or no local cache available.
```bash
ping github.com
letx update
```

### `Package 'xxx' not found in VUR`

The package may not exist yet, or the name is misspelled.
```bash
letx search xxx
letx update && letx search xxx
```

### `Template 'xxx' not found locally`

The template hasn't been downloaded yet.
```bash
letx get xxx
```

### Build error when running `letx -x pkg`

Make sure `binary-bootstrap` has been run:
```bash
letx -x binary-bootstrap
```

If the build environment is broken, reset and try again:
```bash
letx -x zap
letx -x binary-bootstrap
```

## Uninstall

```bash
sudo ./install.sh uninstall
```

To also remove all user data:
```bash
rm -rf ~/.config/letx ~/.cache/letx
```

*Let-X v0.2.0 · VUR: [github.com/T4n-Labs/vur](https://github.com/T4n-Labs/vur)*

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
