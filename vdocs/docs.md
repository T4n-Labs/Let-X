# Let — Dokumentasi Lengkap

> **Let** adalah CLI tool untuk Void Linux yang memudahkan pencarian, pengelolaan, dan pengambilan template package dari **VUR (Void User Repository)** — konsep serupa AUR Helper di Arch Linux.

---

## Daftar Isi

**Untuk Pengguna Umum**
- [Apa itu Let?](#apa-itu-let)
- [Persyaratan Sistem](#persyaratan-sistem)
- [Instalasi](#instalasi)
- [Referensi Command](#referensi-command)
- [Contoh Penggunaan](#contoh-penggunaan)
- [Struktur File Lokal](#struktur-file-lokal)
- [Troubleshooting](#troubleshooting)
- [Uninstall](#uninstall)

**Untuk Developer**
- [Arsitektur Proyek](#arsitektur-proyek)
- [Struktur Direktori](#struktur-direktori)
- [Penjelasan Modul](#penjelasan-modul)
- [Alur Data](#alur-data)
- [Cara Berkontribusi](#cara-berkontribusi)
- [Menjalankan Test](#menjalankan-test)
- [Build Package xbps-src](#build-package-xbps-src)
- [Roadmap](#roadmap)

---

# Untuk Pengguna Umum

## Apa itu Let?

**Let** adalah tool CLI (Command Line Interface) yang berjalan di terminal Void Linux. Fungsinya mirip dengan `yay` atau `paru` di Arch Linux, tetapi untuk ekosistem **VUR (Void User Repository)**.

Dengan Let kamu bisa:
- 🔍 **Mencari** package yang tersedia di VUR
- 📋 **Melihat** daftar semua package
- ℹ️ **Melihat detail** informasi sebuah package
- 📥 **Mengunduh** template package ke komputer lokal

> **Catatan:** Fitur `build` dan `install` via `xbps-src` sedang dalam pengembangan dan akan hadir di versi berikutnya.

---

## Persyaratan Sistem

| Komponen | Versi Minimum |
|---|---|
| Sistem Operasi | Void Linux (glibc atau musl) |
| Python | 3.11 atau lebih baru |
| Koneksi Internet | Diperlukan untuk fetch index & template |

Cek versi Python kamu:
```bash
python3 --version
```

---

## Instalasi

### Metode 1 — Script Otomatis (Direkomendasikan)

```bash
# 1. Clone repo Let
git clone https://github.com/T4n-Labs/let
cd let

# 2. Jalankan script instalasi sebagai root
sudo ./install.sh
```

Script ini akan secara otomatis:
- Menyalin source ke `/usr/lib/let/`
- Menginstall dependensi Python (`typer`, `httpx`, `rich`) ke `/usr/lib/let/`
- Membuat binary wrapper di `/usr/bin/let`

Setelah selesai, cek instalasi:
```bash
let --help
```

### Metode 2 — Instalasi via xbps-src (Paket Resmi)

Jika kamu sudah setup `void-packages`:
```bash
# Salin template ke void-packages
cp -r xbps-template/let ~/void-packages/srcpkgs/let

# Build dan install
cd ~/void-packages
./xbps-src pkg let
sudo xbps-install --repository=hostdir/binpkgs let
```

---

## Referensi Command

### `let search`

Mencari package di VUR berdasarkan kata kunci.

```
let search <keyword> [--category <kategori>]
```

| Argumen / Opsi | Keterangan |
|---|---|
| `<keyword>` | Kata kunci pencarian (wajib) |
| `--category`, `-c` | Filter hasil berdasarkan kategori (`core`, `extra`, `multilib`) |

**Contoh:**
```bash
# Cari semua package yang mengandung kata "browser"
let search browser

# Cari hanya di kategori extra
let search browser --category extra

# Cari dengan shorthand -c
let search discord -c extra
```

**Output:**
```
→ Mencari 'browser' ...

╭──────────────────┬─────────┬──────────┬─────────────╮
│ Nama             │ Versi   │ Kategori │ Maintainer  │
├──────────────────┼─────────┼──────────┼─────────────┤
│ zen-browser      │ 1.19.8b │ extra    │ Naz         │
│ firefox          │ 127.0   │ extra    │ Gh0sT4n     │
╰──────────────────┴─────────┴──────────┴─────────────╯

  Total: 2 package
```

---

### `let info`

Menampilkan informasi lengkap sebuah package.

```
let info <nama-package>
```

| Argumen | Keterangan |
|---|---|
| `<nama-package>` | Nama package yang ingin dilihat (wajib, case-insensitive) |

**Contoh:**
```bash
let info discord
let info wine
let info zen-browser
```

**Output:**
```
╭─────────────── discord ───────────────╮
│ Nama       : discord                  │
│ Versi      : 0.0.134                  │
│ Kategori   : extra                    │
│ Path Repo  : extra/discord            │
│ Homepage   : https://discord.com      │
│ Maintainer : Gh0sT4n                  │
╰───────────────────────────────────────╯

  Status     : ✘ Belum di-get
```

---

### `let list`

Menampilkan semua package yang tersedia di VUR.

```
let list [--category <kategori>]
```

| Opsi | Keterangan |
|---|---|
| `--category`, `-c` | Filter berdasarkan kategori (`core`, `extra`, `multilib`) |

**Contoh:**
```bash
# Tampilkan semua package
let list

# Hanya tampilkan package di kategori multilib
let list --category multilib

# Shorthand
let list -c core
```

---

### `let get`

Mengunduh template package dari VUR ke direktori lokal `~/.config/let/`.

```
let get <nama-package> [--force]
```

| Argumen / Opsi | Keterangan |
|---|---|
| `<nama-package>` | Nama package yang akan diunduh (wajib) |
| `--force`, `-f` | Paksa re-download meski template sudah ada lokal |

**Contoh:**
```bash
# Download template discord
let get discord

# Download ulang (update template)
let get discord --force

# Shorthand force
let get wine -f
```

**Output:**
```
→ Mengambil template 'discord' (extra) ...
  ↓ extra/discord/template
  ↓ extra/discord/files/zprofile
✔ Template berhasil disimpan ke: /home/user/.config/let/extra/discord
→ Selanjutnya kamu bisa build dengan xbps-src (coming soon).
```

---

### `let update`

Memperbarui cache index package dari VUR. Berguna jika ada package baru yang ditambahkan ke VUR.

```
let update
```

**Contoh:**
```bash
let update
```

**Output:**
```
→ Memperbarui index dari VUR ...
✔ Index diperbarui — 47 package tersedia.
```

> **Catatan:** Cache otomatis diperbarui setiap 1 jam saat kamu menggunakan Let. `let update` digunakan untuk memaksanya diperbarui sekarang juga.

---

## Contoh Penggunaan

### Alur Kerja Tipikal

```bash
# 1. Perbarui index dulu (opsional, bisa skip jika baru install)
let update

# 2. Cari package yang kamu inginkan
let search discord

# 3. Cek detail package
let info discord

# 4. Download templatenya
let get discord

# 5. Template sekarang ada di:
ls ~/.config/let/extra/discord/
```

### Eksplorasi Package Berdasarkan Kategori

```bash
# Lihat semua package core (package sistem dasar)
let list --category core

# Lihat semua package multilib (untuk kompatibilitas 32-bit / Wine)
let list --category multilib

# Lihat semua package extra (aplikasi pihak ketiga)
let list --category extra
```

---

## Struktur File Lokal

Setelah menggunakan Let, berikut file dan direktori yang dibuat di sistem kamu:

```
~/.config/let/              ← Direktori utama konfigurasi
├── core/                   ← Template dari kategori core
│   └── <nama-package>/
│       ├── template        ← File template utama xbps-src
│       ├── files/          ← File tambahan (jika ada)
│       └── patches/        ← Patch files (jika ada)
├── extra/                  ← Template dari kategori extra
│   └── <nama-package>/
└── multilib/               ← Template dari kategori multilib
    └── <nama-package>/

~/.cache/let/               ← Cache index
└── packages.json           ← Salinan lokal index VUR (diperbarui tiap 1 jam)
```

---

## Troubleshooting

### `let: command not found`

Binary tidak terpasang di PATH. Coba:
```bash
# Cek apakah file ada
ls -la /usr/bin/let

# Jika tidak ada, jalankan ulang instalasi
sudo ./install.sh
```

### `Gagal fetch index dari GitHub dan tidak ada cache lokal`

Let tidak bisa terhubung ke internet dan tidak ada cache lokal tersedia.
```bash
# Cek koneksi internet
ping github.com

# Jika terhubung tapi masih gagal, coba perbarui index secara manual
let update
```

### `Package 'xxx' tidak ditemukan di VUR`

Kemungkinan package belum ada di VUR, atau nama salah ketik.
```bash
# Cari dengan nama parsial
let search xxx

# Perbarui index dulu, mungkin package baru ditambahkan
let update
let search xxx
```

### `Python >= 3.11 diperlukan`

Versi Python terlalu lama. Update Python via xbps:
```bash
sudo xbps-install -Su python3
python3 --version
```

---

## Uninstall

```bash
# Di direktori repo Let
sudo ./install.sh uninstall
```

Script akan menghapus:
- `/usr/bin/let`
- `/usr/lib/let/`
- `/usr/share/let/`
- `/usr/share/man/man1/let.1` (jika ada)

Data cache dan konfigurasi lokal **tidak** dihapus otomatis. Hapus manual jika diperlukan:
```bash
rm -rf ~/.config/let ~/.cache/let
```

---

---

# Untuk Developer

## Arsitektur Proyek

Let dibangun dengan filosofi **separation of concerns** — setiap lapisan punya tanggung jawab yang jelas dan berdiri sendiri:

```
┌─────────────────────────────────────────┐
│              CLI (cli.py)               │  ← Typer: parse args, output ke user
├────────────────────┬────────────────────┤
│     ops/           │     repo/          │  ← Logika bisnis vs akses data
│  search.py         │  index.py          │
│  info.py           │  fetch.py          │
├────────────────────┴────────────────────┤
│              utils/print.py             │  ← Rich: presentasi output
├─────────────────────────────────────────┤
│              config.py                  │  ← Konstanta, paths, URL
└─────────────────────────────────────────┘
```

**Prinsip penting:**
- `cli.py` tidak boleh berisi logika — hanya orchestrate calls ke `ops/` dan `repo/`
- `ops/` tidak tahu soal HTTP — itu urusan `repo/`
- `repo/` tidak tahu soal tampilan — itu urusan `utils/`
- `config.py` tidak mengimport modul manapun dari proyek ini

---

## Struktur Direktori

```
let/                            ← Root proyek
├── let/                        ← Package Python utama
│   ├── __init__.py             ← Versi app (APP_VERSION)
│   ├── cli.py                  ← Entry point CLI (Typer)
│   ├── config.py               ← Semua konstanta & path
│   │
│   ├── repo/                   ← Layer akses data (GitHub)
│   │   ├── __init__.py
│   │   ├── index.py            ← Fetch & cache packages.json
│   │   └── fetch.py            ← Download folder template via GitHub API
│   │
│   ├── ops/                    ← Layer logika bisnis
│   │   ├── __init__.py
│   │   ├── search.py           ← Filter, sort, list packages
│   │   └── info.py             ← Detail satu package + status lokal
│   │
│   └── utils/                  ← Utilities
│       ├── __init__.py
│       └── print.py            ← Rich output (tabel, panel, warna)
│
├── tests/                      ← Unit tests
│   ├── __init__.py
│   └── test_search.py          ← Test index, search, list
│
├── xbps-template/              ← Template xbps-src untuk packaging
│   ├── let/
│   │   └── template            ← Template file xbps-src
│   └── README.md               ← Panduan build via xbps-src
│
├── install.sh                  ← Script instalasi bash
├── pyproject.toml              ← Konfigurasi proyek & dependensi
└── README.md                   ← Overview singkat
```

---

## Penjelasan Modul

### `config.py`

Satu-satunya file yang mendefinisikan semua konstanta global. **Tidak boleh diimport oleh file lain selain via `from let.config import ...`**.

```python
# URL remote
VUR_REPO     = "T4n-Labs/vur"
VUR_API_BASE = "https://api.github.com/repos/T4n-Labs/vur/contents"
PACKAGES_URL = "https://raw.githubusercontent.com/T4n-Labs/vur/main/packages.json"

# Path lokal
CONFIG_DIR = Path.home() / ".config" / "let"
CACHE_DIR  = Path.home() / ".cache" / "let"
TEMPLATE_DIRS = {
    "core":     CONFIG_DIR / "core",
    "extra":    CONFIG_DIR / "extra",
    "multilib": CONFIG_DIR / "multilib",
}

CACHE_TTL = 3600  # detik (1 jam)
```

**Untuk mengubah lokasi cache atau TTL**, cukup edit `config.py` — semua modul lain akan otomatis ikut.

---

### `repo/index.py`

Bertanggung jawab atas fetch dan cache `packages.json` dari GitHub.

**Fungsi publik:**

| Fungsi | Signature | Keterangan |
|---|---|---|
| `fetch_index` | `(force: bool = False) → list[Package]` | Ambil semua package (dari cache atau GitHub) |
| `get_package` | `(name: str, force: bool = False) → Package \| None` | Cari satu package by nama |
| `cache_info` | `() → dict` | Status cache saat ini |

**Logika cache:**
```
fetch_index() dipanggil
    │
    ├─ cache ada DAN umur < TTL DAN force=False?
    │   └─ return data dari cache lokal
    │
    └─ Sebaliknya:
        ├─ Fetch dari GitHub
        ├─ Tulis ke cache
        └─ return data baru
            │
            └─ Jika fetch GAGAL tapi cache lama ada:
                └─ return cache lama (graceful degradation)
```

---

### `repo/fetch.py`

Bertanggung jawab mengunduh seluruh folder template package dari GitHub menggunakan **GitHub Contents API** (tidak butuh `git` atau `svn` terinstall).

**Fungsi publik:**

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

**Kenapa GitHub Contents API, bukan `git clone` atau `svn`?**
- Tidak membutuhkan `git` atau `svn` terinstall
- Hanya mengunduh file yang dibutuhkan (bukan seluruh repo)
- Lebih portable dan predictable
- Trade-off: lebih banyak HTTP requests untuk folder dengan banyak file

---

### `ops/search.py`

Semua operasi pencarian dan listing dilakukan di sini, **sepenuhnya offline** setelah index di-cache.

**Fungsi publik:**

| Fungsi | Signature | Keterangan |
|---|---|---|
| `search_packages` | `(keyword, category=None) → list[Package]` | Cari packages, opsional filter by category |
| `list_packages` | `(category=None) → list[Package]` | List semua packages |
| `available_categories` | `() → list[str]` | Daftar kategori yang tersedia |

**Field yang dicari saat `search`:**
- `name` — nama package
- `maintainer` — nama/email maintainer
- `homepage` — URL homepage

**Algoritma ranking hasil search:**
```python
def _rank(pkg) -> int:
    name = pkg["name"].lower()
    if name == keyword:       return 0  # exact match → paling atas
    if name.startswith(kw):   return 1  # prefix match
    if kw in name:            return 2  # contains match
    return 3                            # cocok di field lain
```

---

### `ops/info.py`

Menggabungkan data dari index (remote) dengan status lokal.

```python
def get_info(name: str) -> dict | None:
    pkg = get_package(name)          # dari index.py
    is_local = package_exists_locally(category, name)   # dari fetch.py
    local_path = local_package_path(category, name)     # dari fetch.py
    return {**pkg, "installed_locally": is_local, "local_path": str(local_path)}
```

---

### `utils/print.py`

Semua output ke terminal harus melalui fungsi di sini. **Jangan pernah `print()` langsung dari modul lain.**

**Fungsi yang tersedia:**

| Fungsi | Keterangan |
|---|---|
| `print_package_table(packages, title)` | Tabel Rich untuk list packages |
| `print_package_info(info)` | Panel Rich untuk detail satu package |
| `print_success(msg)` | `✔ pesan` (hijau) |
| `print_error(msg)` | `✘ pesan` (merah) ke stderr |
| `print_info(msg)` | `→ pesan` (cyan) |
| `print_warn(msg)` | `! pesan` (kuning) |

**Warna tema:**
```python
C_NAME  = "bold cyan"    # nama package
C_VER   = "green"        # versi
C_CAT   = "yellow"       # kategori
C_MAINT = "dim white"    # maintainer
C_LOCAL = "bold green"   # status tersedia lokal
```

---

## Alur Data

Berikut alur lengkap untuk setiap command:

### `let search <keyword>`

```
cli.py:cmd_search(keyword)
    │
    └─► ops/search.py:search_packages(keyword)
            │
            └─► repo/index.py:fetch_index()
                    │
                    ├─ Cache valid? → baca ~/.cache/let/packages.json
                    └─ Cache expired? → GET packages.json dari GitHub
                                         tulis ke cache
            │
            └─ Filter & sort hasil
    │
    └─► utils/print.py:print_package_table(results)
```

### `let get <package>`

```
cli.py:cmd_get(name)
    │
    ├─► ops/info.py:get_info(name)          ← cek index + status lokal
    │
    ├─ Sudah ada lokal & tidak --force? → print warning, exit
    │
    └─► repo/fetch.py:download_package(path, category, name)
            │
            └─► GitHub Contents API (rekursif)
                    │
                    ├─ Setiap file → GET raw.githubusercontent.com
                    └─ Tulis ke ~/.config/let/<category>/<name>/
    │
    └─► utils/print.py:print_success(dest)
```

---

## Cara Berkontribusi

### Setup Development Environment

```bash
# 1. Fork dan clone repo
git clone https://github.com/<username>/let
cd let

# 2. Buat virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dalam mode development
pip install -e ".[dev]"

# 4. Verifikasi instalasi
let --help
pytest tests/ -v
```

### Konvensi Kode

**Penamaan:**
- Modul dan fungsi: `snake_case`
- Konstanta di `config.py`: `SCREAMING_SNAKE_CASE`
- Type hints wajib untuk semua fungsi publik

**Import order** (ikuti standar `isort`):
```python
# 1. stdlib
from pathlib import Path
from typing import Any

# 2. third-party
import httpx
from rich.console import Console

# 3. internal (absolute imports)
from let.config import CACHE_DIR
from let.repo.index import fetch_index
```

**Docstring:** Semua fungsi publik wajib punya docstring yang menjelaskan args, return, dan exceptions.

```python
def fetch_index(force: bool = False) -> list[Package]:
    """
    Ambil index packages dari VUR.

    Args:
        force: Jika True, abaikan cache dan fetch ulang dari GitHub.

    Returns:
        List of package dicts dari packages.json

    Raises:
        RuntimeError: Jika fetch gagal dan tidak ada cache lokal.
    """
```

### Menambah Command Baru

1. Tambah fungsi command di `cli.py` dengan decorator `@app.command("nama")`
2. Logika bisnis masuk ke `ops/` (bukan di `cli.py`)
3. Akses data masuk ke `repo/` (bukan di `ops/`)
4. Output selalu via `utils/print.py`
5. Tulis unit test di `tests/`

Contoh skeleton command baru:

```python
# cli.py
@app.command("remove")
def cmd_remove(
    name: Annotated[str, typer.Argument(help="Nama package")],
) -> None:
    """Hapus template package dari lokal."""
    from let.ops.remove import remove_package   # buat modul baru
    result = remove_package(name)
    if result:
        print_success(f"Template '{name}' dihapus.")
    else:
        print_error(f"Template '{name}' tidak ditemukan.")
```

---

## Menjalankan Test

```bash
# Jalankan semua test
pytest tests/ -v

# Jalankan test tertentu
pytest tests/test_search.py -v

# Dengan coverage report
pytest tests/ --cov=let --cov-report=term-missing
```

**Test menggunakan monkeypatch** — tidak ada koneksi internet saat testing:

```python
@pytest.fixture
def fake_cache(tmp_path, monkeypatch):
    """Ganti PACKAGES_CACHE dengan file temp berisi mock data."""
    cache_file = tmp_path / "packages.json"
    cache_file.write_text(json.dumps(MOCK_PACKAGES))
    monkeypatch.setattr("let.repo.index.PACKAGES_CACHE", cache_file)
    monkeypatch.setattr("let.repo.index.CACHE_TTL", 9999)
```

**Test yang tersedia:**

| Test | Keterangan |
|---|---|
| `test_fetch_index_from_cache` | Index dibaca dari cache lokal |
| `test_get_package_found` | Cari package yang ada |
| `test_get_package_case_insensitive` | Pencarian tidak case-sensitive |
| `test_get_package_not_found` | Package tidak ada → return None |
| `test_search_by_name` | Pencarian by nama exact |
| `test_search_partial` | Pencarian nama parsial |
| `test_search_with_category_filter` | Filter by kategori |
| `test_search_no_results` | Keyword tidak cocok → list kosong |
| `test_list_all` | List semua package |
| `test_list_by_category` | List filter by kategori |
| `test_available_categories` | Daftar kategori unik |

---

## Build Package xbps-src

Untuk mendistribusikan Let sebagai package `.xbps` resmi:

### Persiapan

```bash
# Setup void-packages
git clone https://github.com/void-linux/void-packages ~/void-packages
cd ~/void-packages
./xbps-src binary-bootstrap

# Copy template
cp -r /path/to/let/xbps-template/let srcpkgs/let
```

### Update Checksum (Wajib Setiap Rilis)

```bash
# Setelah membuat GitHub Release dengan tag vX.Y.Z
cd ~/void-packages
./xbps-src fetch let
sha256sum $XBPS_SRCDISTDIR/let-X.Y.Z.tar.gz
# → salin hash ke field 'checksum' di srcpkgs/let/template
```

### Build dan Test

```bash
cd ~/void-packages

# Build
./xbps-src pkg let

# Cek isi package
./xbps-src show-files let

# Install lokal untuk test
sudo xbps-install --repository=hostdir/binpkgs let

# Verifikasi
let --help
let search discord
```

### Checklist Sebelum Submit ke Void Packages

- [ ] `checksum` sudah diupdate sesuai tarball terbaru
- [ ] `revision` di-reset ke `1` jika `version` berubah
- [ ] `revision` dinaikkan jika hanya template yang berubah (versi sama)
- [ ] Semua dependensi Python (`python3-httpx`, `python3-rich`, `python3-typer`) tersedia di void-packages
- [ ] `./xbps-src pkg let` berhasil tanpa error
- [ ] `./xbps-src show-files let` menunjukkan `/usr/bin/let` ada di output
- [ ] Test manual: `let search`, `let info`, `let list`, `let get` berfungsi

---

## Roadmap

### v0.1.0 — Fase Dasar ✅
- [x] `let search` — pencarian package
- [x] `let info` — detail package
- [x] `let list` — daftar semua package
- [x] `let list --category` — filter by kategori
- [x] `let get` — download template lokal
- [x] `let update` — refresh cache index
- [x] Cache lokal dengan TTL 1 jam
- [x] Graceful degradation saat offline (pakai cache lama)
- [x] Script instalasi bash
- [x] Template xbps-src

### v0.2.0 — Integrasi xbps-src 🔜
- [ ] `let build <package>` — build via `xbps-src pkg`
- [ ] Auto-setup symlink ke `void-packages/srcpkgs/`
- [ ] Deteksi dan konfigurasi `void-packages` directory
- [ ] Progress build output real-time

### v0.3.0 — Instalasi Penuh 🔜
- [ ] `let install <package>` — build + install via `xbps-install`
- [ ] `let remove <package>` — hapus template lokal
- [ ] Manajemen dependensi antar package VUR

### v1.0.0 — Fitur Lanjutan
- [ ] `let upgrade` — update semua template yang sudah di-get
- [ ] Offline mode penuh
- [ ] Konfigurasi user via `~/.config/let/config.toml`
- [ ] Shell completion (bash, zsh, fish)
- [ ] Man page (`let.1`)

---

## Dependensi

| Package | Versi | Fungsi |
|---|---|---|
| `typer[all]` | ≥ 0.12 | CLI framework (argument parsing, help text) |
| `httpx` | ≥ 0.27 | HTTP client untuk fetch GitHub API |
| `rich` | ≥ 13.0 | Pretty terminal output (tabel, panel, warna) |

**Dev dependencies:**
| Package | Fungsi |
|---|---|
| `pytest` | Test runner |
| `pytest-httpx` | Mock HTTP requests untuk unit test |

---

## Lisensi

Let dirilis di bawah lisensi **MIT**. Lihat file `LICENSE` untuk detail lengkap.

---

*Dokumentasi ini dibuat untuk Let v0.1.0*
*VUR: [github.com/T4n-Labs/vur](https://github.com/T4n-Labs/vur)*
