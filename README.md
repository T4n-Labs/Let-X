# Let (VUR Helper)

CLI tool untuk mengakses VUR (Void User Repository) pada T4n OS.

## Features
- Search package
- Info Package
- List Package
- List Category
- Get Package

## Tree Project
```markdown
let/
├── let/
│   ├── __init__.py         → versi app
│   ├── config.py           → semua konstanta (URL, path, TTL)
│   ├── cli.py              → entry point Typer (5 command)
│   ├── repo/
│   │   ├── index.py        → fetch & cache packages.json
│   │   └── fetch.py        → download template via GitHub API
│   ├── ops/
│   │   ├── search.py       → filter & sort packages
│   │   └── info.py         → detail package + status lokal
│   └── utils/
│       └── print.py        → output Rich (tabel, panel, warna)
├── tests/
│   └── test_search.py      → 12 unit test
├── pyproject.toml
└── README.md
```

## Usage
```bash
# Installation
$ cd let && pip install -e
$ ./install

# Command
$ let search discord
$ let search zen --category extra
$ let info wine
$ let list
$ let list --category multilib
$ let get discord
$ let get wine --force
$ let update
```
