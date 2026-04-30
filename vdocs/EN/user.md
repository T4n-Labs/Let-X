# Let-X — User Guide

> **Let-X** is a CLI tool for Void Linux that makes it easy to search, explore, and download package templates from **VUR (Void User Repository)** — similar in concept to AUR Helpers on Arch Linux.

**Binary:** `letx` | **Version:** 0.1.2 | **Language:** Python 3.11+

---

## Table of Contents

- [What is Let-X?](#what-is-let-x)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Command Reference](#command-reference)
  - [letx search](#letx-search)
  - [letx info](#letx-info)
  - [letx list](#letx-list)
  - [letx get](#letx-get)
  - [letx update](#letx-update)
- [Usage Examples](#usage-examples)
- [Local File Structure](#local-file-structure)
- [Troubleshooting](#troubleshooting)
- [Uninstall](#uninstall)

---

## What is Let-X?

**Let-X** is a command-line tool that runs in the Void Linux terminal. It works similarly to `yay` or `paru` on Arch Linux, but for the **VUR (Void User Repository)** ecosystem.

With Let-X you can:
- 🔍 **Search** packages available in VUR by name or description
- 📋 **List** packages by category with statistics
- ℹ️ **View details** of any package including local template status
- 📁 **Find** locally downloaded templates
- 📥 **Download** package templates to your local machine

> **Note:** `build` and `install` via `xbps-src` are planned for v0.2.0.

---

## System Requirements

| Component | Minimum Version |
|---|---|
| Operating System | Void Linux (glibc or musl) |
| Python | 3.11 or newer |
| Internet Connection | Required for fetching index and templates |

Check your Python version:
```bash
python3 --version
```

---

## Installation

### Method 1 — Automated Script (Recommended)

```bash
# 1. Clone the Let-X repo
git clone https://github.com/T4n-Labs/Let-X
cd Let-X

# 2. Run the install script as root
sudo ./install.sh
```

The script will automatically:
1. Clean any previous installation at `/usr/lib/letx/`
2. Build a Python wheel from source (`letx-*.whl`)
3. Install the wheel to `/usr`
4. Install runtime dependencies (`httpx`, `rich`) to `/usr/lib/letx/`
5. Create the `/usr/bin/letx` wrapper with correct `PYTHONPATH`

Verify the installation:
```bash
letx --help
letx -v
```

To uninstall:
```bash
sudo ./install.sh uninstall
```

### Method 2 — via xbps-src

If you have `void-packages` set up:
```bash
# Copy the template
cp -r xbps-template/letx ~/void-packages/srcpkgs/letx

# Build and install
cd ~/void-packages
./xbps-src pkg letx
sudo xbps-install --repository=/home/$USER/.config/xbps-src/hostdir/binpkgs letx
```

---

## Command Reference

### `letx search`

Search for packages in VUR by name or description.

```
letx search <keyword> [-c CATEGORY]
letx search "<description>" [-c CATEGORY]
letx search -t <pkg_name>
```

| Argument / Option | Description |
|---|---|
| `<keyword>` | Package name or word to search |
| `"<description>"` | Description phrase (quote multi-word queries) |
| `-c`, `--category CATEGORY` | Filter by category: `core` \| `extra` \| `multilib` |
| `-t`, `--template PKG_NAME` | Search for a locally downloaded template |

**Search by name:**
```bash
letx search discord
letx search browser
letx search zen -c extra
```

**Search by description:**
```bash
# Searches the 'description' field in packages.json
letx search "Programming Language"
letx search "web browser"
letx search "Windows" -c multilib
```

**Search local templates (`-t`):**

Checks directories in order: `core → extra → multilib`
```bash
letx search -t discord
letx search -t wine
```

Output when template is found:
```
╭────────── discord (local template) ──────────╮
│ Package     : discord                         │
│ Category    : extra                           │
│ Location    : ~/.config/letx/extra/discord    │
│ Version     : 0.0.134                         │
│ Description : Chat and VOIP application       │
│ Homepage    : https://discord.com             │
│ Maintainer  : Gh0sT4n                         │
│                                               │
│ Files:                                        │
│   • files/zprofile                            │
│   • template                                  │
╰───────────────────────────────────────────────╯
```

Output when template is not found:
```
! Template 'discord' not found locally.
  Checked: core → extra → multilib
  Run 'letx get discord' to download it.
```

Running `letx search` with no arguments:
```
[ERROR] No Options
usage: letx search [-h] [-c CATEGORY] [-t PKG_NAME] [keyword]
...
```

---

### `letx info`

Show detailed package information, or browse recent packages by category.

```
letx info <pkg_name>
letx info <all|core|extra|multilib>
letx info -c <CATEGORY>
letx info -t <pkg_name>
```

| Argument / Option | Description |
|---|---|
| `<pkg_name>` | Show full details for a specific package |
| `all` | Show the 20 most recently added packages (all categories) |
| `core` | Show the 20 most recently added packages in `core` |
| `extra` | Show the 20 most recently added packages in `extra` |
| `multilib` | Show the 20 most recently added packages in `multilib` |
| `-c`, `--category CATEGORY` | List all packages in a category (`all`\|`core`\|`extra`\|`multilib`) |
| `-t`, `--template PKG_NAME` | Show local template details |

**Examples:**
```bash
# Full details for a specific package
letx info discord
letx info wine

# Browse latest 20 packages
letx info all
letx info extra
letx info multilib

# List all packages in a category
letx info -c core
letx info -c all

# Show local template info
letx info -t discord
```

**Package detail output:**
```
╭────────────────── discord ──────────────────╮
│ Name        : discord                        │
│ Version     : 0.0.134                        │
│ Category    : extra                          │
│ Description : Chat and VOIP application      │
│ Repo Path   : extra/discord                  │
│ Homepage    : https://discord.com            │
│ Maintainer  : Gh0sT4n                        │
╰──────────────────────────────────────────────╯
  Status      : ✘ Not fetched yet
```

Running `letx info` with no arguments:
```
[ERROR] No Options
usage: letx info [-h] [-c CATEGORY] [-t PKG_NAME] [name]
...
```

---

### `letx list`

List packages from VUR. Requires at least one argument or option.

```
letx list <all|core|extra|multilib>
letx list -c <CATEGORY>
letx list -p [CATEGORY]
```

| Argument / Option | Description |
|---|---|
| `all` | Show the 20 most recently added packages |
| `core` | Show the 20 most recently added packages in `core` |
| `extra` | Show the 20 most recently added packages in `extra` |
| `multilib` | Show the 20 most recently added packages in `multilib` |
| `-c`, `--category CATEGORY` | List **all** packages in a category |
| `-p`, `--package [CATEGORY]` | Show package count statistics |

**Examples:**
```bash
# Browse latest 20 packages
letx list all
letx list extra

# List ALL packages in a category
letx list -c core
letx list -c multilib

# Package count statistics
letx list -p           # all categories
letx list -p extra     # specific category
letx list -p core
```

**Statistics output (`-p`):**
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

Running `letx list` with no arguments:
```
[ERROR] No Options
usage: letx list [-h] [-c CATEGORY] [-p [CATEGORY]] [scope]
...
```

---

### `letx get`

Download a package template from VUR to your local machine.

```
letx get <pkg_name> [-f]
```

| Argument / Option | Description |
|---|---|
| `<pkg_name>` | Name of the package to download (required) |
| `-f`, `--force` | Re-download even if the template already exists locally |

**Examples:**
```bash
# Download a template
letx get discord
letx get wine

# Force re-download (update)
letx get discord --force
letx get wine -f
```

**Output:**
```
→ Fetching template 'discord' (extra) ...
  ↓ extra/discord/template
  ↓ extra/discord/files/zprofile
✔ Template saved to: /home/user/.config/letx/extra/discord
→ You can now build it with xbps-src (coming soon).
```

Templates are saved to:
- **core** packages → `~/.config/letx/core/<pkg>/`
- **extra** packages → `~/.config/letx/extra/<pkg>/`
- **multilib** packages → `~/.config/letx/multilib/<pkg>/`

---

### `letx update`

Refresh the local package index cache from VUR.

```
letx update
```

```bash
letx update
```

```
→ Refreshing package index from VUR ...
✔ Index updated — 23 packages available.
```

> The cache at `~/.cache/letx/packages.json` is automatically refreshed every hour. Use `letx update` to force an immediate refresh.

---

## Usage Examples

### Typical Workflow

```bash
# 1. Refresh the index (optional on first run)
letx update

# 2. Search for a package
letx search discord

# 3. View full details
letx info discord

# 4. Download the template
letx get discord

# 5. Template is now available at:
ls ~/.config/letx/extra/discord/
letx search -t discord    # verify it's there
```

### Exploring the Repository

```bash
# See what's been added recently
letx list all
letx list extra

# Browse a specific category
letx list -c core
letx list -c multilib

# Check package counts
letx list -p

# Search for gaming-related packages
letx search "games"
letx search "Windows" -c multilib

# Find a browser
letx search browser -c extra
```

### Managing Local Templates

```bash
# Check if a template is already downloaded
letx search -t discord
letx info -t wine

# Download multiple templates
letx get discord
letx get wine
letx get zen-browser

# Re-download (update) a template
letx get discord --force
```

---

## Local File Structure

After using Let-X, these directories and files are created on your system:

```
~/.config/letx/                   ← Main config directory
├── core/                         ← Templates from the core category
│   └── <pkg-name>/
│       ├── template              ← Main xbps-src template file
│       ├── files/                ← Additional files (if any)
│       └── patches/              ← Patch files (if any)
├── extra/                        ← Templates from the extra category
│   └── <pkg-name>/
└── multilib/                     ← Templates from the multilib category
    └── <pkg-name>/

~/.cache/letx/                    ← Cache directory
└── packages.json                 ← Local copy of VUR index (refreshed hourly)

/usr/bin/letx                     ← Binary wrapper
/usr/lib/letx/                    ← Python source + runtime deps
/usr/share/letx/MANIFEST          ← Installation metadata
```

---

## Troubleshooting

### `letx: command not found`

The binary is not installed or not in PATH.
```bash
# Check if the file exists
ls -la /usr/bin/letx

# If missing, re-run the installer
sudo ./install.sh
```

### `Failed to fetch index from GitHub and no local cache found`

Let-X cannot reach the internet and has no local cache.
```bash
# Check connectivity
ping github.com

# Force a cache refresh once connected
letx update
```

### `Package 'xxx' not found in VUR`

The package may not exist in VUR yet, or the name is misspelled.
```bash
# Search with a partial name
letx search xxx

# Refresh the index first (a new package may have been added)
letx update
letx search xxx
```

### `Template 'xxx' not found locally`

The template has not been downloaded yet.
```bash
letx get xxx
```

### `Python >= 3.11 required`

Your Python version is too old. Update via xbps:
```bash
sudo xbps-install -Su python3
python3 --version
```

### Warning: `Target directory already exists` during install

This happens when reinstalling over an existing copy. The updated `install.sh` handles this automatically by cleaning `/usr/lib/letx/` before installing.

If it still occurs, clean manually:
```bash
sudo rm -rf /usr/lib/letx
sudo ./install.sh
```

---

## Uninstall

```bash
# From the Let-X repo directory
sudo ./install.sh uninstall
```

This removes:
- `/usr/bin/letx`
- `/usr/lib/letx/`
- `/usr/share/letx/`
- `/usr/share/man/man1/letx.1` (if present)

User data is **not** removed automatically. To clean everything:
```bash
rm -rf ~/.config/letx ~/.cache/letx
```

---

*Let-X v0.1.2 — VUR: [github.com/T4n-Labs/vur](https://github.com/T4n-Labs/vur)*
