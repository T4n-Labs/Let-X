# Let-X — User Guide

> **Let-X** is a CLI tool for Void Linux that simplifies searching, managing, and downloading package templates from the **VUR (Void User Repository)** — a concept similar to an AUR Helper in Arch Linux.

**Binary:** `letx` | **Version:** 0.2.0 | **Language:** Python 3.11+

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

## What is Let-X?

**Let-X** is a CLI (Command Line Interface) tool that runs in the Void Linux terminal. Its function is similar to `yay` or `paru` in Arch Linux, but tailored for the **VUR (Void User Repository)** ecosystem.

With Let-X you can:
- **Search** for packages available in VUR by name or description
- **View lists** of packages per category along with their statistics
- **View detailed** information about a package, including its local status
- **Locate** templates that have already been downloaded to your system
- **Download** package templates to your local machine

> **Note:** The `build` and `install` features via `xbps-src` are planned for v0.2.0.

## System Requirements

| Component           | Minimum Requirement                     |
|---------------------|-----------------------------------------|
| Operating System    | Void Linux (glibc)                      |
| Python              | 3.11 or newer                           |
| Internet Connection | Required to fetch the index & templates |

Check your Python version:
```bash
python3 --version

```

## Installation

### Method 1 — Automated Script (Recommended)

```bash
# 1. Clone the Let-X repository
git clone https://github.com/T4n-Labs/Let-X
cd Let-X

# 2. Run the installation script as root
sudo ./install.sh

```

The script will automatically perform the following actions:

1. Clean up any old installation at `/usr/lib/letx/`
2. Build the Python wheel from source (`letx-*.whl`)
3. Install the wheel to `/usr`
4. Install runtime dependencies (`httpx`, `rich`) into `/usr/lib/letx/`
5. Create a wrapper at `/usr/bin/letx` with the proper `PYTHONPATH`

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

If you have already set up `void-packages`:

```bash
# Copy the template
cp -r xbps-template/letx /path/to/void-packages/srcpkgs/letx

# Build and install
cd ~/void-packages
./xbps-src pkg letx
sudo xbps-install --repository=/path/to/void-packages/hostdir/binpkgs letx

```

## Command Reference

### `letx search`

Searches for packages in the VUR based on name or description.

```
letx search <keyword> [-c CATEGORY]
letx search "<description>" [-c CATEGORY]
letx search -t <pkg_name>

```

| Argument / Option           | Description                                        |
|-----------------------------|----------------------------------------------------|
| `<keyword>`                 | Package name or keyword to look for                |
| `"<description>"`           | Description phrase (use quotes for multiple words) |
| `-c`, `--category CATEGORY` | Filter by category: `core` | `extra` | `multilib`  |
| `-t`, `--template PKG_NAME` | Search for templates already downloaded locally    |

**Search by name:**

```bash
letx search discord
letx search browser
letx search zen -c extra

```

**Search by description:**

```bash
# Searches within the 'description' field in packages.json
letx search "Programming Language"
letx search "web browser"
letx search "Windows" -c multilib

```

**Search local templates (`-t`):**

Checks directories sequentially in this order: `core → extra → multilib`

```bash
letx search -t discord
letx search -t wine

```

Example of `-t` output (template found):

```
╭────────── discord (local template) ───────────╮
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

Example of `-t` output (template not found):

```
! Template 'discord' not found locally.
  Checked: core → extra → multilib
  Run 'letx get discord' to download it.

```

### `letx info`

Displays detailed information about a package, or explores the latest packages per category.

```
letx info <pkg_name>
letx info <all|core|extra|multilib>
letx info -c <CATEGORY>
letx info -t <pkg_name>

```

| Argument / Option           | Description                                                       |
|-----------------------------|-------------------------------------------------------------------|
| `<pkg_name>`                | Display full details of a specific package                        |
| `all`                       | Display the 20 latest added packages (all categories)             |
| `core`                      | Display the 20 latest packages in the `core` category             |
| `extra`                     | Display the 20 latest packages in the `extra` category            |
| `multilib`                  | Display the 20 latest packages in the `multilib` category         |
| `-c`, `--category CATEGORY` | List all packages in a category (`all`|`core`|`extra`|`multilib`) |
| `-t`, `--template PKG_NAME` | Display details of a local template                               |

**Usage examples:**

```bash
# Detail of a specific package
letx info discord
letx info wine

# 20 latest packages
letx info all
letx info extra
letx info multilib

# List all packages in a category
letx info -c core
letx info -c all

# Local template info
letx info -t discord

```

**Example of package detail output:**

```
╭────────────────── discord ───────────────────╮
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

If `letx info` is run without arguments:

```
[ERROR] No Options
usage: letx info [-h] [-c CATEGORY] [-t PKG_NAME] [name]
...

```

### `letx list`

Displays a list of packages from the VUR. Requires at least one argument or option.

```
letx list <all|core|extra|multilib>
letx list -c <CATEGORY>
letx list -p [CATEGORY]

```

| Argument / Option | Description |
|------------------------------|----------------------------------------------|
| `all`                        | Display the 20 latest added packages         |
| `core`                       | Display the 20 latest packages in `core`     |
| `extra`                      | Display the 20 latest packages in `extra`    |
| `multilib`                   | Display the 20 latest packages in `multilib` |
| `-c`, `--category CATEGORY`  | List **all** packages in a specific category |
| `-p`, `--package [CATEGORY]` |Show statistics on the number of packages     |

**Usage examples:**

```bash
# 20 latest packages
letx list all
letx list extra

# All packages in a specific category
letx list -c core
letx list -c multilib

# Package count statistics
letx list -p            # all categories
letx list -p extra      # specific category
letx list -p core

```

**Example of statistics output (`-p`):**

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

If `letx list` is run without arguments:

```
[ERROR] No Options
usage: letx list [-h] [-c CATEGORY] [-p [CATEGORY]] [scope]
...

```

### `letx get`

Downloads a package template from the VUR to your local directory.

```
letx get <pkg_name> [-f]

```

| Argument / Option | Description                                                |
|-------------------|------------------------------------------------------------|
| `<pkg_name>`      | Name of the package to download (required)                 |
| `-f`, `--force`   | Re-download the template even if it already exists locally |

**Usage examples:**

```bash
# Download template
letx get discord
letx get wine

# Force re-download (update template)
letx get discord --force
letx get wine -f

```

**Example output:**

```
→ Fetching template 'discord' (extra) ...
  ↓ extra/discord/template
  ↓ extra/discord/files/zprofile
✔ Template saved to: /home/user/.config/letx/extra/discord
→ You can now build it with xbps-src (coming soon).

```

Templates are saved in:

* **core** packages → `~/.config/letx/core/<pkg>/`
* **extra** packages → `~/.config/letx/extra/<pkg>/`
* **multilib** packages → `~/.config/letx/multilib/<pkg>/`

### `letx update`

Updates the local package index cache from the VUR.

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

> The cache at `~/.cache/letx/packages.json` is automatically updated every hour. Use `letx update` to trigger a manual refresh right away.

## Usage Examples

### Typical Workflow

```bash
# 1. Update index (optional on first run)
letx update

# 2. Search for a package
letx search discord

# 3. View full details
letx info discord

# 4. Download the template
letx get discord

# 5. Template is now available at:
ls ~/.config/letx/extra/discord/
letx search -t discord    # verification

```

### Browsing the Repository

```bash
# View recently added packages
letx list all
letx list extra

# Explore a specific category
letx list -c core
letx list -c multilib

# Check total package count
letx list -p

# Search for gaming packages
letx search "games"
letx search "Windows" -c multilib

# Search for browsers
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

# Update an existing template
letx get discord --force

```

## Local File Structure

After using Let-X, the following directories and files are created on your system:

```
~/.config/letx/                   ← Main configuration directory
├── core/                         ← Templates from the core category
│   └── <package-name>/
│       ├── template              ← Main xbps-src template file
│       ├── files/                ← Additional files (if any)
│       └── patches/              ← Patch files (if any)
├── extra/                        ← Templates from the extra category
│   └── <package-name>/
└── multilib/                     ← Templates from the multilib category
    └── <package-name>/

~/.cache/letx/                    ← Cache directory
└── packages.json                 ← Local copy of the VUR index (updated every 1 hour)

/usr/bin/letx                     ← Binary wrapper
/usr/lib/letx/                    ← Python source + runtime deps
/usr/share/letx/MANIFEST          ← Installation metadata

```

## Troubleshooting

### `letx: command not found`

The binary is either not installed or not present in your PATH.

```bash
# Check if the file exists
ls -la /usr/bin/letx

# If it is missing, rerun the installer
sudo ./install.sh reinstall

```

### `Failed to fetch index from GitHub and no local cache found`

Let-X cannot connect to the internet and no local cache is available.

```bash
# Check connection
ping github.com

# Force refresh cache
letx update

```

### `Package 'xxx' not found in VUR`

The package might not exist in VUR yet, or the name is misspelled.

```bash
# Search using a partial name
letx search xxx

# Update the index first (there might be new packages available)
letx update
letx search xxx

```

### `Template 'xxx' not found locally`

The template hasn't been downloaded yet.

```bash
letx get xxx

```

### `Python >= 3.11 required`

Your Python version is too old. Update via xbps:

```bash
sudo xbps-install -Su python3
python3 --version

```

### `Target directory already exists` warning during installation

This occurs when reinstalling over an older installation path. The latest `install.sh` handles this automatically by cleaning up `/usr/lib/letx/` before writing files.

If it still happens, clear it manually:

```bash
sudo rm -rf /usr/lib/letx
sudo ./install.sh

```

## Uninstall

```bash
# From the Let-X repository directory
sudo ./install.sh uninstall

```

The script will clean up:

* `/usr/bin/letx`
* `/usr/lib/letx/`
* `/usr/share/letx/`
* `/usr/share/man/man1/letx.1` (if any)

User data is **not** deleted automatically. To clear out everything:

```bash
rm -rf ~/.config/letx ~/.cache/letx

```

*Let-X v0.2.0 — VUR: [github.com/T4n-Labs/vur](https://github.com/T4n-Labs/vur)*

---

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)