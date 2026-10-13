# Let-X (VUR Helper) | [ID]()

CLI Tool/VUR-Helper untuk mengakses VUR (Void User Repository) dengan Mudah untuk Void Linux, Dan Turunannya.

## Features
- Search package
- Info Package
- List Package
- List Category
- Get Package

## Tree Project
```markdown
Let-X/
├── letx/
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
│   ├── __init__.py
│   └── test_search.py      → 12 unit test
├── vdocs/
│   └── docs.md
├── xbps-template/
│   └── letx/
│       └── template        → Template XBPS-SRC

├── install.sh              → Script Installation
├── pyproject.toml
└── README.md
```

## Dokumentation

* Dokumentasi.[Disini](./vdocs/docs.md#indonesia)
* Documentation.[Here](./vdocs/docs.md#english)

---

<div align="center">

[@T4n-Labs](https://t4nlabs.web.id/) · [@Gh0sT4n](https://gh0st4n.my.id/)

</div>