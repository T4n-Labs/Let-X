# Let-X (VUR Helper)

A CLI tool / VUR Helper to easily access the VUR (Void User Repository) for Void Linux and its derivatives.

## Features
- Search package
- Package info
- List packages
- List categories
- Get package

## Project Tree
```markdown
Let-X/
├── letx/
│   ├── __init__.py         → App version
│   ├── config.py           → All constants (URL, path, TTL)
│   ├── cli.py              → Typer entry point (5 commands)
│   ├── repo/
│   │   ├── index.py        → Fetch & cache packages.json
│   │   └── fetch.py        → Download template via GitHub API
│   ├── ops/
│   │   ├── search.py       → Filter & sort packages
│   │   └── info.py         → Package details + local status
│   └── utils/
│       └── print.py        → Rich output (tables, panels, colors)
├── tests/
│   ├── __init__.py
│   └── test_search.py      → 12 unit tests
├── vdocs/
│   └── docs.md
├── xbps-template/
│   └── letx/
│       └── template        → XBPS-SRC Template

├── install.sh              → Installation script
├── pyproject.toml
└── README.md

```

## Documentation

* Dokumentasi.[Disini](./vdocs/docs.md#indonesia)
* Documentation.[Here](./vdocs/docs.md#english)
---

<div align="center">

[@T4n-Labs](https://t4nlabs.web.id/) · [@Gh0sT4n](https://gh0st4n.my.id/)

</div>