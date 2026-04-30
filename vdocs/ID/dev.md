# Let-X — Panduan Developer

> Dokumentasi teknis untuk kontributor dan maintainer **Let-X v0.1.2**.

---

## Daftar Isi

- [Arsitektur Proyek](#arsitektur-proyek)
- [Struktur Direktori](#struktur-direktori)
- [Referensi Modul](#referensi-modul)
- [Alur Data](#alur-data)
- [Setup Development Environment](#setup-development-environment)
- [Konvensi Kode](#konvensi-kode)
- [Menambah Command Baru](#menambah-command-baru)
- [Menjalankan Test](#menjalankan-test)
- [Build Package xbps-src](#build-package-xbps-src)
- [Dependensi](#dependensi)
- [Roadmap](#roadmap)

---

## Arsitektur Proyek

Let-X mengikuti prinsip **separation of concerns** — setiap lapisan punya satu tanggung jawab yang jelas:

```
┌──────────────────────────────────────────────┐
│               CLI (cli.py)                    │  argparse: parse args, routing ke handler
├────────────────────┬─────────────────────────┤
│       ops/         │         repo/            │  logika bisnis vs akses data
│  search.py         │     index.py             │
│  info.py           │     fetch.py             │
├────────────────────┴─────────────────────────┤
│              utils/print.py                   │  Rich: semua output terminal
├──────────────────────────────────────────────┤
│               config.py                       │  konstanta, path, URL
└──────────────────────────────────────────────┘
```

**Prinsip penting:**
- `cli.py` tidak boleh berisi logika — hanya orchestrate ke `ops/` dan `repo/`
- `ops/` tidak tahu soal HTTP — itu urusan `repo/`
- `repo/` tidak tahu soal tampilan — itu urusan `utils/`
- `config.py` tidak mengimport modul manapun dari proyek ini

---

## Struktur Direktori

```
Let-X/
├── letx/                         ← Python package utama
│   ├── __init__.py               → Versi dan nama app
│   ├── cli.py                    → Entry point CLI (argparse)
│   ├── config.py                 → Semua konstanta dan path
│   │
│   ├── repo/                     → Layer akses data (GitHub)
│   │   ├── __init__.py
│   │   ├── index.py              → Fetch dan cache packages.json
│   │   └── fetch.py              → Download folder template via GitHub API
│   │
│   ├── ops/                      → Layer logika bisnis
│   │   ├── __init__.py
│   │   ├── search.py             → Search, list, count, pencarian template lokal
│   │   └── info.py               → Detail package + info template lokal
│   │
│   └── utils/
│       ├── __init__.py
│       └── print.py              → Semua output Rich (tabel, panel, warna)
│
├── tests/
│   ├── __init__.py
│   └── test_search.py            → Unit tests
│
├── xbps-template/
│   └── letx/
│       └── template              → Template xbps-src
│
├── setup.py                      → Compatibility shim untuk xbps-src
├── pyproject.toml                → Metadata proyek dan dependensi
├── install.sh                    → Script instalasi bash
├── LICENSE
└── README.md
```

---

## Referensi Modul

### `config.py`

Satu-satunya tempat untuk semua konstanta. Modul lain tidak boleh hardcode path atau URL.

```python
# Remote
VUR_REPO     = "T4n-Labs/vur"
VUR_API_BASE = "https://api.github.com/repos/T4n-Labs/vur/contents"
PACKAGES_URL = "https://raw.githubusercontent.com/T4n-Labs/vur/main/packages.json"

# Path lokal
CONFIG_DIR = Path.home() / ".config" / "letx"
CACHE_DIR  = Path.home() / ".cache"  / "letx"
TEMPLATE_DIRS = {
    "core":     CONFIG_DIR / "core",
    "extra":    CONFIG_DIR / "extra",
    "multilib": CONFIG_DIR / "multilib",
}

CACHE_TTL = 3600  # detik (1 jam)
```

---

### `repo/index.py`

Mengelola fetch dan cache `packages.json`.

| Fungsi | Signature | Keterangan |
|---|---|---|
| `fetch_index` | `(force: bool = False) → list[Package]` | Ambil semua package (dari cache atau GitHub) |
| `get_package` | `(name: str) → Package \| None` | Cari satu package by nama eksak |
| `cache_info` | `() → dict` | Status cache saat ini |

**Logika cache:**
```
fetch_index()
    │
    ├─ Cache ada DAN umur < TTL DAN force=False?
    │   └─ return cache lokal
    │
    └─ Sebaliknya:
        ├─ GET packages.json dari GitHub
        ├─ Tulis ke ~/.cache/letx/packages.json
        └─ Return data baru
            │
            └─ Jika fetch GAGAL tapi ada cache lama:
                └─ Return cache lama (graceful degradation)
```

---

### `repo/fetch.py`

Mengunduh folder template dari GitHub menggunakan **GitHub Contents API** — tidak butuh `git` atau `svn`.

| Fungsi | Signature | Keterangan |
|---|---|---|
| `download_package` | `(pkg_path, category, pkg_name, progress_cb) → Path` | Download folder package dari VUR |
| `package_exists_locally` | `(category, pkg_name) → bool` | Cek apakah template sudah ada lokal |
| `local_package_path` | `(category, pkg_name) → Path \| None` | Path lokal package jika ada |

**Strategi fetch:**
```
GitHub Contents API
GET /repos/T4n-Labs/vur/contents/extra/discord
    │
    └─ Response: list of {type, name, path, ...}
        │
        ├─ type == "file"  → download via raw.githubusercontent.com
        └─ type == "dir"   → rekursi ke subdirektori
```

---

### `ops/search.py`

Semua operasi pencarian dan listing. Sepenuhnya offline setelah index di-cache.

| Fungsi | Signature | Keterangan |
|---|---|---|
| `search_packages` | `(keyword, category=None) → list[Package]` | Cari by nama atau deskripsi |
| `list_packages` | `(category=None) → list[Package]` | List semua package |
| `latest_packages` | `(category=None, limit=20) → list[Package]` | Package yang terakhir ditambahkan |
| `count_packages` | `(category=None) → dict[str, int]` | Jumlah package per kategori |
| `search_local_template` | `(pkg_name) → LocalTemplateResult` | Cari template di direktori lokal |
| `available_categories` | `() → list[str]` | Kategori unik di index |

**Search fields (fix v0.1.2):**
```python
# Hanya name dan description — tidak ada false positive dari maintainer/homepage
_SEARCH_FIELDS = ("name", "description")
```

**Ranking hasil search:**
```python
def _rank(pkg) -> int:
    name = pkg["name"].lower()
    if name == keyword:       return 0   # exact match → paling atas
    if name.startswith(kw):   return 1   # prefix match
    if kw in name:            return 2   # contains match
    return 3                             # cocok di description
```

**Pencarian template lokal — core → extra → multilib:**
```python
search_order = ["core", "extra", "multilib"]
for cat in search_order:
    pkg_dir = TEMPLATE_DIRS[cat] / pkg_name
    if pkg_dir.exists():
        return LocalTemplateResult(found=True, category=cat, path=pkg_dir, ...)
return LocalTemplateResult(found=False, ...)
```

---

### `ops/info.py`

| Fungsi | Signature | Keterangan |
|---|---|---|
| `get_info` | `(name: str) → dict \| None` | Detail package + status lokal |
| `get_local_template_info` | `(pkg_name: str) → dict` | Detail template lokal + data VUR |

---

### `utils/print.py`

Semua output ke terminal harus melalui modul ini. **Jangan pernah `print()` langsung dari modul lain.**

| Fungsi | Keterangan |
|---|---|
| `print_package_table(packages, title, show_desc)` | Tabel Rich untuk list package |
| `print_package_info(info)` | Panel Rich untuk detail satu package |
| `print_local_template_info(info)` | Panel Rich untuk template lokal |
| `print_package_counts(counts, category)` | Tabel statistik |
| `print_success(msg)` | `✔ pesan` (hijau) |
| `print_error(msg)` | `✘ pesan` (merah) |
| `print_info(msg)` | `→ pesan` (cyan) |
| `print_warn(msg)` | `! pesan` (kuning) |

**Tema warna:**
```python
C_NAME    = "bold cyan"     # nama package
C_VER     = "green"         # versi
C_CAT     = "yellow"        # kategori
C_DESC    = "dim white"     # deskripsi
C_MAINT   = "dim white"     # maintainer
C_LOCAL   = "bold green"    # tersedia lokal
C_MISSING = "dim red"       # belum diunduh
C_PATH    = "cyan"          # path file
C_FILE    = "dim cyan"      # listing file
```

---

## Alur Data

### `letx search <keyword>`

```
letx search discord
    │
    ▼
cli.py:cmd_search()
    │
    ├─ args.template? → _search_local_template()
    │                       → ops/search.py:search_local_template()
    │                       → utils/print.py:print_local_template_info()
    │
    └─ keyword ada → ops/search.py:search_packages()
                         │
                         └─ repo/index.py:fetch_index()
                                 │
                                 ├─ cache valid → baca file
                                 └─ expired     → GET GitHub → tulis cache
                         │
                         └─ filter (name + description) → sort by rank
    │
    └─ utils/print.py:print_package_table()
```

### `letx list -p`

```
letx list -p
    │
    ▼
cli.py:cmd_list()
    │
    └─ ops/search.py:count_packages()
            │
            └─ fetch_index() → hitung per kategori
    │
    └─ utils/print.py:print_package_counts()
```

### `letx get <pkg>`

```
letx get discord
    │
    ▼
cli.py:cmd_get()
    │
    ├─ ops/info.py:get_info()            → cek index + status lokal
    │
    ├─ Sudah lokal & tidak --force?      → print_warn(), exit 0
    │
    └─ repo/fetch.py:download_package()
            │
            └─ GitHub Contents API (rekursif)
                    ├─ tiap file → GET raw.githubusercontent.com
                    └─ tulis ke ~/.config/letx/<category>/<pkg>/
    │
    └─ utils/print.py:print_success()
```

---

## Setup Development Environment

```bash
# 1. Fork dan clone repo
git clone https://github.com/<username>/Let-X
cd Let-X

# 2. Buat virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dalam mode development
pip install -e ".[dev]"

# 4. Verifikasi
letx --help
pytest tests/ -v
```

---

## Konvensi Kode

**Penamaan:**
- Modul dan fungsi: `snake_case`
- Konstanta di `config.py`: `SCREAMING_SNAKE_CASE`
- Type hints wajib untuk semua fungsi publik

**Import order:**
```python
# 1. stdlib
import sys
from pathlib import Path
from typing import Any

# 2. third-party
import httpx
from rich.console import Console

# 3. internal (selalu absolute imports)
from letx.config import CACHE_DIR
from letx.repo.index import fetch_index
```

**Docstring — semua fungsi publik wajib:**
```python
def search_packages(keyword: str, category: str | None = None) -> list[Package]:
    """
    Search packages by keyword (case-insensitive).
    Matches against: name, description.

    Args:
        keyword:  search keyword
        category: optional filter ("core"|"extra"|"multilib")

    Returns:
        Matching packages sorted by relevance.
    """
```

---

## Menambah Command Baru

1. Tambah subparser di `cli.py:build_parser()`
2. Tambah handler `cmd_<nama>()` di `cli.py`
3. Daftarkan di blok dispatch `main()`
4. Logika bisnis masuk ke `ops/` (bukan di `cli.py`)
5. Akses data masuk ke `repo/` (bukan di `ops/`)
6. Output selalu via `utils/print.py`
7. Tulis test di `tests/`

**Skeleton command baru:**
```python
# Di build_parser():
p_remove = sub.add_parser("remove", help="Remove a local template")
p_remove.add_argument("name", help="Package name")

# Handler:
def cmd_remove(args: argparse.Namespace) -> int:
    from letx.ops.remove import remove_template   # modul baru
    removed = remove_template(args.name)
    if removed:
        print_success(f"Template '{args.name}' removed.")
        return 0
    print_error(f"Template '{args.name}' not found locally.")
    return 1

# Di main():
elif args.command == "remove":
    sys.exit(cmd_remove(args))
```

---

## Menjalankan Test

```bash
# Semua test
pytest tests/ -v

# File tertentu
pytest tests/test_search.py -v

# Dengan coverage report
pytest tests/ --cov=letx --cov-report=term-missing
```

Test menggunakan `monkeypatch` — tidak butuh koneksi internet:

```python
@pytest.fixture
def fake_cache(tmp_path, monkeypatch):
    cache_file = tmp_path / "packages.json"
    cache_file.write_text(json.dumps(MOCK_PACKAGES))
    monkeypatch.setattr("letx.repo.index.PACKAGES_CACHE", cache_file)
    monkeypatch.setattr("letx.repo.index.CACHE_TTL", 9999)
```

**Test yang tersedia:**

| Test | Keterangan |
|---|---|
| `test_fetch_index_from_cache` | Index dibaca dari cache lokal |
| `test_get_package_found` | Cari package yang ada |
| `test_get_package_case_insensitive` | `DISCORD` == `discord` |
| `test_get_package_not_found` | Package tidak ada → return `None` |
| `test_search_by_name` | Pencarian nama exact |
| `test_search_partial` | Pencarian nama parsial |
| `test_search_with_category_filter` | Filter by kategori |
| `test_search_no_results` | Tidak ada hasil → list kosong |
| `test_list_all` | List semua package |
| `test_list_by_category` | List filter by kategori |
| `test_available_categories` | Return set kategori unik |

---

## Build Package xbps-src

### Persiapan

```bash
git clone https://github.com/void-linux/void-packages ~/void-packages
cd ~/void-packages
./xbps-src binary-bootstrap

cp -r /path/to/Let-X/xbps-template/letx srcpkgs/letx
```

### Update Checksum (Wajib Setiap Rilis)

```bash
cd ~/void-packages
./xbps-src fetch letx
sha256sum $XBPS_SRCDISTDIR/letx-0.1.2.tar.gz
# → salin hash ke field 'checksum' di srcpkgs/letx/template
```

### Build dan Test

```bash
cd ~/void-packages

# Build
./xbps-src pkg letx

# Cek isi package
./xbps-src show-files letx

# Install lokal
xbps-rindex -a hostdir/binpkgs/letx-*.xbps
sudo xbps-install --repository=/home/$USER/void-packages/hostdir/binpkgs letx

# Verifikasi
letx --help
letx -v
letx search discord
```

### Checklist Sebelum Rilis

- [ ] `checksum` sudah diupdate sesuai tarball terbaru
- [ ] `revision=1` jika `version` berubah; naikkan `revision` saja jika versi sama
- [ ] `setup.py` shim ada di root repo (diperlukan untuk kompatibilitas build style xbps-src)
- [ ] Semua runtime deps tersedia di Void repo: `python3-httpx`, `python3-rich`
- [ ] `./xbps-src pkg letx` selesai tanpa error
- [ ] `/usr/bin/letx` ada di output `./xbps-src show-files letx`
- [ ] Test manual: `letx search`, `letx info`, `letx list`, `letx get` semua berfungsi

---

## Dependensi

| Package | Versi | Fungsi |
|---|---|---|
| `httpx` | ≥ 0.27 | HTTP client untuk GitHub API |
| `rich` | ≥ 13.0 | Pretty terminal output (tabel, panel, warna) |
| `argparse` | stdlib | Parsing argumen CLI (tidak perlu install) |

**Build dependencies (xbps-src):**

| Package | Fungsi |
|---|---|
| `python3-setuptools` | Build backend |
| `python3-wheel` | Packaging wheel |
| `python3-pip` | Instalasi |

**Dev dependencies:**

| Package | Fungsi |
|---|---|
| `pytest` | Test runner |
| `pytest-httpx` | Mock HTTP request untuk test |

---

## Roadmap

### v0.1.0 — Fitur Dasar ✅
- [x] `letx search` — pencarian by nama
- [x] `letx info` — detail package
- [x] `letx list` — list semua package
- [x] `letx get` — download template lokal
- [x] `letx update` — refresh cache index
- [x] Cache lokal TTL 1 jam
- [x] Graceful degradation offline
- [x] Script instalasi bash
- [x] Template xbps-src

### v0.1.1 — Konversi Bahasa ✅
- [x] Semua string user-facing dikonversi ke Bahasa Inggris
- [x] CLI migrasi dari `typer` ke `argparse` (stdlib)
- [x] Build system migrasi dari `hatchling` ke `setuptools`
- [x] `setup.py` shim ditambahkan untuk kompatibilitas xbps-src
- [x] Binary diubah dari `let` ke `letx` (hindari konflik bash builtin)

### v0.1.2 — Enhanced Search & Info ✅
- [x] Fix: false positive pada search (dibatasi ke `name` + `description`)
- [x] `[ERROR] No Options` pada `letx`, `letx search`, `letx info`, `letx list` tanpa argumen
- [x] `letx search "deskripsi"` — pencarian by deskripsi
- [x] `letx search -t <pkg>` — cari template lokal (core → extra → multilib)
- [x] `letx info all|core|extra|multilib` — 20 package terbaru
- [x] `letx info -c <category>` — list lengkap per kategori
- [x] `letx info -t <pkg>` — panel detail template lokal
- [x] `letx list all|core|extra|multilib` — 20 package terbaru
- [x] `letx list -c <category>` — list lengkap per kategori
- [x] `letx list -p [category]` — statistik jumlah package

### v0.2.0 — Integrasi xbps-src 🔜
- [ ] `letx build <pkg>` — build via `xbps-src pkg`
- [ ] Auto-symlink template ke `void-packages/srcpkgs/`
- [ ] Deteksi dan konfigurasi direktori `void-packages`
- [ ] Streaming output build secara real-time
- [ ] `letx search -x <pkg>` — cari file `.xbps` di binpkgs lokal

### v0.3.0 — Pipeline Instalasi Penuh 🔜
- [ ] `letx install <pkg>` — build + install via `xbps-install`
- [ ] `letx remove <pkg>` — hapus template lokal
- [ ] Resolusi dependensi antar package VUR

### v1.0.0 — Polish
- [ ] `letx upgrade` — update semua template yang sudah di-get
- [ ] Shell completion (bash, zsh, fish)
- [ ] Man page (`letx.1`)
- [ ] Konfigurasi user via `~/.config/letx/config.toml`

---

*Let-X v0.1.2 — VUR: [github.com/T4n-Labs/vur](https://github.com/T4n-Labs/vur)*
