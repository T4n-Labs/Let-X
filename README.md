# Let (VUR Helper)

CLI Tool/VUR-Helper untuk mengakses VUR (Void User Repository) dengan Mudah untuk Void Linux, Dan Turunannya.

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
├── vdocs/
│   └── docs.md
├── xbps-template/
│   └── template            → Template XBPS-SRC
├── install.sh              → Script Installation
├── pyproject.toml
└── README.md
```

## Documentation

* Dokumentasi.[Disini](./vdocs/docs.md#indonesia)
* Documentation.[Here](./vdocs/docs.md#english)

---
* @T4n-Labs[https://github.com/T4n-Labs]
* @Gh0sT4n[https://github.com/gh0st4n]
