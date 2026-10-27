# Let-X

**Let-X** is a lightweight and fast CLI (Command Line Interface) tool designed to manage the **Void User Repository (VUR)**. Built using pure Python (without any third-party dependencies), Let-X makes it easy for users to search, retrieve, update, and view detailed package information from the VUR repository.

## ✨ Features

- 🚀 **Fast & Lightweight**: Uses only the **Python Standard Library** (`urllib`, `json`, `re`, `argparse`, `pathlib`), meaning no external `pip install` dependencies are required.
- 🔍 **Flexible Search**: Search for packages by name, description, or category.
- 📦 **Template Management**: Automatically download and update Void Linux `template` files to your local configuration directory.
- 📊 **Formatted Detailed Information**: Display package metadata and dependencies (`hostmakedepends`, `makedepends`, `depends`) in a clean, easy-to-read 4-column grid format.
- 💾 **Local Caching**: The JSON database is stored locally in `~/.config/letx/db/` for fast offline access after the initial sync.

## 📦 Installation

### Prerequisites
- Python 3.10 or newer
- [`uv`](https://docs.astral.sh/uv/) (Recommended for fast package management and building)

### Method 1: Using `uv` (Recommended)

1. **Clone this repository:**
   ```bash
   git clone https://github.com/T4n-Labs/letx.git
   cd letx
   ```

2. **Install using `uv` (Global/Tool):**
   ```bash
   uv tool install .
   ```
   *Alternatively, for development (editable) mode:*
   ```bash
   uv pip install -e .
   ```

3. **Verify the installation:**
   ```bash
   letx --help
   ```

### Method 2: Using the Setup Script (`setup.sh`)

For a quick and automated installation (including system-wide or user-local setups), you can use the provided `setup.sh` script.

1. **Make the script executable:**
   ```bash
   chmod +x setup.sh
   ```

2. **Run the installation:**
   *For system-wide installation (requires sudo):*
   ```bash
   sudo ./setup.sh --install
   ```
   *For user-only installation (no sudo required):*
   ```bash
   ./setup.sh --install user
   ```

> **Note:** The `setup.sh` script is maintained exclusively by **Gh0sT4n**.

## 🚀 Usage

### 1. Update the Database
Before using other features, sync your local database with the latest VUR repository:
```bash
letx update
```
*Output:*
```text
🔄 Updating VUR database...
    Downloading packages.json...
   ⤓ Downloading search.json...
   ⤓ Downloading index.json...
   ⤓ Downloading categories.json...
✔ Database successfully updated!
```

### 2. Search for a Package
Search for packages by name, description, or category (e.g., "browser", "dinit", "core"):
```bash
letx search browser
```
*Output:*
```text
🔍 Found 5 package(s) for 'browser':

PACKAGE NAME                   | CATEGORY   | DESCRIPTION
--------------------------------------------------------------------------------
brave                          | extra      | Web browser that blocks ads and t...
brave-origin                   | extra      | Minimalist browser from the maker...
floorp                         | extra      | Firefox fork seeking balance betw...
helium-browser                 | extra      | Private, fast, and honest web bro...
zen-browser                    | extra      | Performance oriented Firefox-base...
```

### 3. Retrieve a Package Template
Download the Void Linux `template` file for a specific package to your local configuration directory:
```bash
letx get calamares
```

### 4. Update a Package Template
If a maintainer releases a new revision for a template, update that specific template without re-downloading the entire database:
```bash
letx update calamares
```

### 5. View Detailed Package Information
Display complete package metadata, including dependencies formatted in a 4-column grid:
```bash
letx info calamares
```
*Output:*
```text
Name Package    : calamares
Version         : 3.4.2
Revision        : 3
Archs           : aarch64, x86_64, x86_64-musl, ...
Description     : Distribution-independent installer framework
Maintainer      : Naz <ndpm13@ch-naseem.com>
Distributor     : Gh0sT4n <darskevoid@gmail.com>
License         : BSD-2-Clause, GPL-3.0-or-later, ...
Homepage        : https://calamares.io
Build Style     : cmake
Hostmakedepends :
-) git                   -) extra-cmake-modules -) pkg-config          -) gettext            
-) ckbcomp               -) kcoreaddons           -) python3-QtPy        -) libpwquality       
-) python3-yaml          -) python3-jsonschema  
Makedepends     :
-) python3-devel         -) python3-jsonschema  -) yaml-cpp-devel      -) python3-yaml       
-) boost-devel           -) qt6-base-devel      -) python3-devel       -) kpmcore-devel      
-) qt6-tools             -) qt6-translations    -) boost               -) boost-python3      
-) python3-QtPy          -) qt6-svg-devel       -) libpwquality        -) qt6-webengine      
-) plasma-framework-devel -) qt6-webengine     
Depends         :
-) kconfig               -) kcoreaddons         -) kiconthemes         -) ki18n              
-) kio                   -) ksolid              -) boost               -) ckbcomp            
-) polkit-qt6            -) gtk-update-icon-cache -) plasma-framework  -) squashfs-tools     
-) libpwquality        -) icu                 -) rsync               
```

## 📂 Directory & Configuration Structure

Let-X stores cached data and templates in the user's configuration directory (`~/.config/letx/`):

```text
~/.config/letx/
├── db/                  # Local JSON database cache
│   ├── packages.json
│   ├── search.json
│   ├── index.json
│   └── categories.json
├── core/                # Templates for 'core' category packages
│   ── calamares/
│       └── template
├── extra/               # Templates for 'extra' category packages
└── multilib/            # Templates for 'multilib' category packages
```

## 🏗️ Project Structure

```text
letx/
├── letx/
│   ├── __init__.py
│   ├── main.py          # CLI entry point and argument parsing
│   └── src/
│       ├── __init__.py
│       ├── config.py    # URL constants and directory paths
│       ├── cmd.py       # Command logic (get, search, update, info)
│       └── utility.py   # Utility functions (fetch, parse template, format grid)
├── tests/
│   ├── __init__.py
│   ├── test_utility.py
│   └── test_cmd.py
├── pyproject.toml       # Build configuration and project metadata
├── LICENSE              # Project license
└── README.md            # This documentation
```

## 🛠️ Development & Testing

If you want to contribute or modify the code, follow these steps:

1. **Clone the repository and navigate to the project directory:**
   ```bash
   git clone https://github.com/T4n-Labs/letx.git
   cd letx
   ```

2. **Sync the development environment with testing tools:**
   ```bash
   uv sync --extra dev
   ```

3. **Run the test suite:**
   ```bash
   uv run pytest tests/ -v
   ```

4. **Run directly without installing:**
   ```bash
   uv run letx --help
   ```

### 🧪 Writing Tests
All new features or bug fixes should include corresponding tests in the `tests/` directory. We use `pytest` as the testing framework. Ensure all tests pass before submitting a Pull Request.

## 📜 License

This project is distributed under the same license as the parent repository. Please see the [`LICENSE`](LICENSE) file for more details.

## 👥 Maintainer

- **Gh0sT4n** - *Lead Developer, Distributor & Sole Maintainer* ([darskevoid@gmail.com](mailto:darskevoid@gmail.com))