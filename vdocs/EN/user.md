# Let — User Documentation

> **Let** is a CLI tool for Void Linux that makes it easy to search for, manage, and retrieve package templates from the **VUR (Void User Repository)** — a concept similar to AUR Helper in Arch Linux.

## Table of Contents

**For General Users**
- [Let — User Documentation](#let--user-documentation)
  - [Table of Contents](#table-of-contents)
- [For General Users](#for-general-users)
  - [What is Let?](#what-is-let)
  - [System Requirements](#system-requirements)
  - [Installation](#installation)
    - [Method 1 — Automated Script (Recommended)](#method-1--automated-script-recommended)
    - [Method 2 — Installation via xbps-src (Official Package)](#method-2--installation-via-xbps-src-official-package)
  - [Command Reference](#command-reference)
    - [`let search`](#let-search)
    - [`let info`](#let-info)
    - [`let list`](#let-list)
    - [`let get`](#let-get)
    - [`let update`](#let-update)
  - [Usage Examples](#usage-examples)
    - [Typical Workflow](#typical-workflow)
    - [Explore Packages by Category](#explore-packages-by-category)
  - [Local File Structure](#local-file-structure)
  - [Troubleshooting](#troubleshooting)
    - [`let: command not found`](#let-command-not-found)
    - [`Failed to fetch index from GitHub and no local cache available`](#failed-to-fetch-index-from-github-and-no-local-cache-available)
    - [`Package ‘xxx’ not found in VUR`](#package-xxx-not-found-in-vur)
    - [`Python >= 3.11 required`](#python--311-required)
  - [Uninstall](#uninstall)

# For General Users

## What is Let?

**Let** is a CLI (Command Line Interface) tool that runs in the Void Linux terminal. Its functionality is similar to `yay` or `paru` in Arch Linux, but for the **VUR (Void User Repository)** ecosystem.

With Let, you can:
- 🔍 **Search** for packages available in VUR
- 📋 **View** a list of all packages
- ℹ️ **View details** of a package
- 📥 **Download** package templates to your local computer

> **Note:** The `build` and `install` features via `xbps-src` are currently under development and will be available in the next version.

## System Requirements

| Component | Minimum Version |
|---|---|
| Operating System | Void Linux (glibc or musl) |
| Python | 3.11 or newer |
| Internet Connection | Required to fetch index & template |

Check your Python version:
```bash
python3 --version
```

## Installation

### Method 1 — Automated Script (Recommended)

```bash
# 1. Clone the Let repository
git clone https://github.com/T4n-Labs/let
cd let

# 2. Run the installation script as root
sudo ./install.sh
```

This script will automatically:
- Copy the source to `/usr/lib/let/`
- Install Python dependencies (`typer`, `httpx`, `rich`) to `/usr/lib/let/`
- Create a binary wrapper in `/usr/bin/let`

Once finished, verify the installation:
```bash
let --help
```

### Method 2 — Installation via xbps-src (Official Package)

If you have already set up `void-packages`:
```bash
# Copy the template to void-packages
cp -r xbps-template/let ~/void-packages/srcpkgs/let

# Build and install
cd ~/void-packages
./xbps-src pkg let
sudo xbps-install --repository=hostdir/binpkgs let
```

## Command Reference

### `let search`

Searches for packages in VUR based on a keyword.

```
let search <keyword> [--category <category>]
```

| Argument / Option | Description |
|---|---|
| `<keyword>` | Search keyword (required) |
| `--category`, `-c` | Filter results by category (`core`, `extra`, `multilib`) |

**Example:**
```bash
# Search for all packages containing the word “browser”
let search browser

# Search only in the extra category
let search browser --category extra

# Search using the shorthand -c
let search discord -c extra
```

**Output:**
```
→ Searching for ‘browser’ ...

╭──────────────────┬─────────┬──────────┬─────────────╮
│ Name             │ Version   │ Category │ Maintainer  │
├──────────────────┼─────────┼──────────┼─────────────┤
│ zen-browser      │ 1.19.8b │ extra    │ Naz         │
│ firefox          │ 127.0   │ extra    │ Gh0sT4n     │
╰──────────────────┴─────────┴──────────┴─────────────╯

  Total: 2 packages
```

### `let info`

Displays complete information about a package.

```
let info <package-name>
```

| Argument | Description |
|---|---|
| `<package-name>` | The name of the package to view (required, case-insensitive) |

**Example:**
```bash
let info discord
let info wine
let info zen-browser
```

**Output:**
```
╭─────────────── discord ───────────────╮
│ Name       : discord                  │
│ Version   : 0.0.134                  │
│ Category  : extra                    │
│ Repo Path : extra/discord            │
│ Homepage   : https://discord.com      │
│ Maintainer : Gh0sT4n                  │
╰───────────────────────────────────────╯

  Status     : ✘ Not yet fetched
```

### `let list`

Displays all packages available in VUR.

```
let list [--category <category>]
```

| Option | Description |
|---|---|
| `--category`, `-c` | Filter by category (`core`, `extra`, `multilib`) |

**Example:**
```bash
# Display all packages
let list

# Display only packages in the multilib category
let list --category multilib

# Shorthand
let list -c core
```

### `let get`

Downloads package templates from VUR to the local directory `~/.config/let/`.

```
let get <package-name> [--force]
```

| Argument / Option | Description |
|---|---|
| `<package-name>` | Name of the package to download (required) |
| `--force`, `-f` | Force a re-download even if the template already exists locally |

**Example:**
```bash
# Download the Discord template
let get discord

# Redownload (update the template)
let get discord --force

# Shorthand force
let get wine -f
```

**Output:**
```
→ Retrieving ‘discord’ template (extra) ...
  ↓ extra/discord/template
  ↓ extra/discord/files/zprofile
✔ Template successfully saved to: /home/user/.config/let/extra/discord
→ Next, you can build with xbps-src (coming soon).
```

### `let update`

Updates the VUR package index cache. Useful when new packages are added to VUR.

```
let update
```

**Example:**
```bash
let update
```

**Output:**
```
→ Updating the VUR index ...
✔ Index updated — 47 packages available.
```

> **Note:** The cache is automatically updated every hour while you're using Let. `let update` is used to force an immediate update.

## Usage Examples

### Typical Workflow

```bash
# 1. Update the index first (optional; can be skipped if newly installed)
let update

# 2. Search for the package you want
let search discord

# 3. Check package details
let info discord

# 4. Download the template
let get discord

# 5. The template is now located at:
ls ~/.config/let/extra/discord/
```

### Explore Packages by Category

```bash
# View all core packages (basic system packages)
let list --category core

# View all multilib packages (for 32-bit compatibility / Wine)
let list --category multilib

# View all extra packages (third-party applications)
let list --category extra
```

## Local File Structure

After using Let, the following files and directories are created on your system:

```
~/.config/let/              ← Main configuration directory
├── core/                   ← Templates from the core category
│   └── <package-name>/
│       ├── template        ← Main xbps-src template file
│       ├── files/          ← Additional files (if any)
│       └── patches/        ← Patch files (if any)
├── extra/                  ← Templates from the extra category
│   └── <package-name>/
└── multilib/               ← Templates from the multilib category
    └── <package-name>/

~/.cache/let/               ← Cache index
└── packages.json           ← Local copy of the VUR index (updated every hour)
```


## Troubleshooting

### `let: command not found`

The binary is not installed in the PATH. Try:
```bash
# Check if the file exists
ls -la /usr/bin/let

# If it’s not there, re-run the installation
sudo ./install.sh
```

### `Failed to fetch index from GitHub and no local cache available`

Let cannot connect to the internet and no local cache is available.
```bash
# Check internet connection
ping github.com

# If connected but still failing, try updating the index manually
let update
```

### `Package ‘xxx’ not found in VUR`

The package may not yet be in VUR, or the name was misspelled.
```bash
# Search by partial name
let search xxx

# Update the index first; the package may have been recently added
let update
let search xxx
```

### `Python >= 3.11 required`

The Python version is too old. Update Python via xbps:
```bash
sudo xbps-install -Su python3
python3 --version
```

## Uninstall

```bash
# In the Let repo directory
sudo ./install.sh uninstall
```

The script will remove:
- `/usr/bin/let`
- `/usr/lib/let/`
- `/usr/share/let/`
- `/usr/share/man/man1/let.1` (if present)

Cache data and local configuration are **not** automatically deleted. Delete manually if necessary:
```bash
rm -rf ~/.config/let ~/.cache/let
```

---
* @T4n-Labs
* @Gh0sT4n