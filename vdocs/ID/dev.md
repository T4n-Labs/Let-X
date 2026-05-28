# Let-X — Panduan Developer

> Dokumentasi teknis untuk kontributor dan maintainer **Let-X v0.2.0**.

## Daftar Isi

- [Arsitektur Proyek](#arsitektur-proyek)
- [Struktur Direktori](#struktur-direktori)
- [Referensi Modul](#referensi-modul)
- [Perubahan v0.1.2 → v0.2.0](#perubahan-v012--v020)
- [Arsitektur xbps-src Integration](#arsitektur-xbps-src-integration)
- [Alur Data](#alur-data)
- [Setup Development Environment](#setup-development-environment)
- [Konvensi Kode](#konvensi-kode)
- [Menambah Command Baru](#menambah-command-baru)
- [Menjalankan Test](#menjalankan-test)
- [Build Package xbps-src](#build-package-xbps-src)
- [Dependensi](#dependensi)
- [Catatan Pengembangan Selanjutnya](#catatan-pengembangan-selanjutnya)

## Arsitektur Proyek

Let-X mengikuti prinsip **separation of concerns** — setiap lapisan punya satu tanggung jawab yang jelas:

```
┌──────────────────────────────────────────────────────┐
│                    CLI (cli.py)                      │  argparse: parse args, routing handler
├────────────────────┬─────────────────────────────────┤
│       ops/         │          repo/                  │  logika bisnis vs akses data
│  search.py         │      index.py                   │
│  info.py           │      fetch.py                   │
├────────────────────┴─────────────────────────────────┤
│                 utils/print.py                       │  Rich: semua output terminal
│                 utils/xbps.py                        │  xbps-src wrapper (baru di v0.2.0)
├──────────────────────────────────────────────────────┤
│                  config.py                           │  konstanta, path, URL
└──────────────────────────────────────────────────────┘
         ↓
┌──────────────────────────────────────────────────────┐
│               backend/ (xbps-src)                    │  void-packages murni, tidak dimodifikasi
│   srcpkgs/         → base-files, base-chroot         │  (hanya untuk bootstrap/internal)
│   common/          → build-style, hooks, chroot-style│
│   xbps-src         → main script                     │
└──────────────────────────────────────────────────────┘
```

**Prinsip penting:**
- `cli.py` tidak boleh berisi logika — hanya orchestrate ke `ops/` dan `repo/`
- `ops/` tidak tahu soal HTTP — itu urusan `repo/`
- `repo/` tidak tahu soal tampilan — itu urusan `utils/`
- `config.py` tidak mengimport modul manapun dari proyek ini
- `utils/xbps.py` adalah satu-satunya modul yang boleh memanggil subprocess xbps-src

## Struktur Direktori

```
Let-X/
├── letx/
│   ├── __init__.py
│   ├── cli.py                          ← Entry point CLI
│   ├── config.py                       ← Semua konstanta dan path
│   │
│   ├── backend/                        ← xbps-src (void-packages murni)
│   │   ├── xbps-src                    ← Script utama xbps-src
│   │   ├── srcpkgs/                    ← BACKEND ONLY: base-files, base-chroot
│   │   │   ├── base-chroot/
│   │   │   └── base-files/
│   │   ├── common/
│   │   │   ├── build-style/            ← Build system scripts (cmake, cargo, dll)
│   │   │   ├── chroot-style/           ← Chroot scripts
│   │   │   │   ├── uunshare.sh         ← Default (tidak dimodifikasi)
│   │   │   │   ├── bwrap.sh
│   │   │   │   ├── letx.sh             ← BARU: custom chroot untuk VUR builds
│   │   │   │   └── ...
│   │   │   ├── environment/
│   │   │   ├── hooks/
│   │   │   └── ...
│   │   ├── etc/
│   │   └── root-git/                   ← .git/ yang di-rename (GIT_DIR fix)
│   │
│   ├── ops/
│   │   ├── search.py                   ← Search, list, count packages
│   │   └── info.py                     ← Get package detail + local template
│   │
│   ├── repo/
│   │   ├── index.py                    ← Fetch & cache packages.json dari VUR
│   │   └── fetch.py                    ← Download template via GitHub API
│   │
│   └── utils/
│       ├── print.py                    ← Semua output Rich
│       └── xbps.py                     ← xbps-src wrapper (BARU di v0.2.0)
│
├── install.sh
├── pyproject.toml
└── tests/
```

## Referensi Modul

### `config.py`

Semua konstanta dan path. **Tidak boleh diimport dari modul lain** — hanya `config.py` yang boleh mengimport stdlib.

```python
# Path penting
BACKEND_DIR          # letx/backend/
XBPS_SRC_PATH        # letx/backend/xbps-src
BACKEND_GIT_DIR      # letx/backend/root-git/ (GIT_DIR fix)
BACKEND_SRCPKGS_DIR  # letx/backend/srcpkgs/ (base-files, base-chroot ONLY)

CONFIG_DIR           # ~/.config/letx/
CACHE_DIR            # ~/.cache/letx/
TEMPLATE_DIRS        # {"core": ..., "extra": ..., "multilib": ...}
LETX_MASTERDIR       # ~/.config/letx/masterdir/
LETX_CHROOT_SRCPKGS  # ~/.config/letx/masterdir/letx-srcpkgs/
LETX_HOSTDIR         # ~/.config/letx/hostdir/
LETX_SRCPKGS_DIR     # ~/.config/letx/srcpkgs/ (legacy, dipertahankan untuk kompatibilitas)
```

### `utils/xbps.py`

Wrapper xbps-src. Bertanggung jawab atas seluruh interaksi dengan xbps-src.

| Fungsi                                 | Tugas                                                 |
|----------------------------------------|-------------------------------------------------------|
| `run(args)`                            | Entry point utama dari `cli.py`                       |
| `find_template(pkgname)`               | Loop `core → extra → multilib`, return `(cat, path)`  |
| `stage_vur_template(pkgname, pkg_dir)` | Copy + patch template ke `masterdir/letx-srcpkgs/`    |
| `build_xbps_env(...)`                  | Bangun environment untuk subprocess xbps-src          |
| `_run_with_template(...)`              | Jalankan xbps-src untuk `CMDS_NEED_PKG`               |
| `_run_xbps_raw(...)`                   | Forward args langsung ke xbps-src untuk `CMDS_NO_PKG` |
| `_parse_args(args)`                    | Identifikasi target, pkgname, xbps_options            |

## Perubahan v0.1.2 → v0.2.0

### 1. Penambahan Backend (`letx/backend/`)

**v0.1.2:** Tidak ada backend. `letx -x` belum ada.

**v0.2.0:** xbps-src (void-packages murni) di-bundle di `letx/backend/`. Perubahan dari upstream void-packages:
- `backend/srcpkgs/` **hanya berisi** `base-files/` dan `base-chroot/` — tidak ada template package biasa
- `.git/` di-rename menjadi `root-git/` agar tidak bentrok dengan `.git/` proyek Let-X sendiri
- `common/chroot-style/letx.sh` **ditambahkan** (lihat bagian berikutnya)

`pyproject.toml` diupdate untuk bundle file backend:
```toml
[tool.setuptools.package-data]
letx = [
    "backend/xbps-src",
    "backend/srcpkgs/**/*",
    "backend/common/**/*",
    "backend/common/*",
    "backend/etc/**/*",
    "backend/root-git/**/*",
    "backend/root-git/*",
]
```

### 2. Script Shell `letx.sh` — Custom Chroot Style

**File:** `letx/backend/common/chroot-style/letx.sh`

**Masalah yang diselesaikan:**

xbps-src default menggunakan `uunshare.sh` untuk setup chroot namespace. Template VUR tersimpan di `~/.config/letx/extra/<pkg>/` yang **tidak ter-mount** di dalam chroot. Chroot hanya mount dua path:
```
LETX_MASTERDIR  →  /               (root chroot)
BACKEND_DIR     →  /void-packages/ (backend xbps-src)
```

`uunshare.sh` original:
```bash
exec xbps-uunshare $EXTRA_ARGS -b $DISTDIR:/void-packages ...
#                  ^^^^^^^^^^^
#                  EXTRA_ARGS di sini → tertimpa oleh DISTDIR mount
```

Mount order bermasalah: `EXTRA_ARGS` (bind mount VUR srcpkgs) diproses **sebelum** DISTDIR. Di Linux mount namespace, mount DISTDIR ke `/void-packages/` kemudian menutup seluruh subtree termasuk mount yang sudah ada di `/void-packages/srcpkgs/`.

**`letx.sh` membalik urutan:**
```bash
exec xbps-uunshare \
    -b $DISTDIR:/void-packages \   ← DISTDIR dulu
    ${HOSTDIR:+-b $HOSTDIR:/host} \
    $EXTRA_ARGS \                  ← EXTRA_ARGS sesudah (overlay di atas DISTDIR)
    -- $MASTERDIR $CMD $@
```

**Diaktifkan** di `xbps.py` via:
```python
env["XBPS_CHROOT_CMD"] = "letx"
env["XBPS_CHROOT_CMD_ARGS"] = f"-b {LETX_CHROOT_SRCPKGS}:void-packages/srcpkgs"
```

### 3. VUR Template Staging System

**Problem:** VUR template di `~/.config/letx/extra/zig/` tidak bisa diakses dari dalam chroot. Solusi menggunakan `masterdir/letx-srcpkgs/` sebagai staging area yang **selalu accessible** di dalam chroot sebagai `/letx-srcpkgs/`.

**Alur staging:**
```
SOURCE: ~/.config/letx/extra/zig/template     (tidak pernah dimodifikasi)
           ↓  stage_vur_template()
STAGED: ~/.config/letx/masterdir/letx-srcpkgs/zig/template  (patched copy)
           ↓  bind-mount via letx.sh EXTRA_ARGS
CHROOT: /void-packages/srcpkgs/zig/template   (xbps-src baca dari sini)
```

**Patch yang diterapkan saat staging:**

xbps-src memanggil `${pkgname}_package()` untuk semua package di `xbps-src-doinstall.sh`. Template VUR yang mengikuti standar xbps-src void-packages tidak wajib mendefinisikan fungsi ini untuk single-package template. Let-X menginjeksikan default no-op secara otomatis:

```bash
# Auto-injected by Let-X
zig_package() { :; }
```

**Template asli tidak pernah dimodifikasi.** Patch hanya ada di staged copy di `masterdir/letx-srcpkgs/`.

### 4. GIT_DIR Fix

`root-git/` adalah `.git/` yang di-rename. xbps-src memanggil `git symbolic-ref` untuk detect branch info. Tanpa fix ini, error `fatal: not a git repository` muncul setelah wheel install karena `.git/` di-exclude dari wheel secara default.

```python
# Di build_xbps_env():
if BACKEND_GIT_DIR.is_dir():
    env["GIT_DIR"]       = str(BACKEND_GIT_DIR)
    env["GIT_WORK_TREE"] = str(BACKEND_DIR)
else:
    # Wheel install: root-git tidak ada, unset agar git tidak salah baca
    env.pop("GIT_DIR",       None)
    env.pop("GIT_WORK_TREE", None)
```

### 5. Pemisahan XBPS_SRCPKGDIR

**v0.1.2:** Satu srcpkgs untuk semua kebutuhan.

**v0.2.0:** Dua srcpkgs dengan peran berbeda:

| Path                                              | Digunakan untuk                                             |
|---------------------------------------------------|-------------------------------------------------------------|
| `BACKEND_SRCPKGS_DIR` (`backend/srcpkgs/`)        | Bootstrap only: `binary-bootstrap`, `zap`, `bootstrap`, dll |
| `LETX_CHROOT_SRCPKGS` (`masterdir/letx-srcpkgs/`) | VUR package builds: `pkg`, `build`, `fetch`, dll            |

## Arsitektur xbps-src Integration

### Dua Instance xbps-src

Setiap `letx -x pkg <nama>` menjalankan **dua instance xbps-src** yang perlu konfigurasi berbeda:

```
[HOST] outer xbps-src
  ├── Baca XBPS_SRCPKGDIR dari env var Python
  │   → LETX_CHROOT_SRCPKGS (host path)
  ├── setup_pkg() → source template
  └── chroot_handler()
        ↓ uunshare via letx.sh
        ↓ bind mounts:
        │   BACKEND_DIR      → /void-packages/
        │   LETX_MASTERDIR   → /
        │   LETX_CHROOT_SRCPKGS → /void-packages/srcpkgs/  ← overlay
        ↓
[CHROOT] inner xbps-src (IN_CHROOT=1)
  ├── Env di-clear oleh env -i
  ├── XBPS_SRCPKGDIR = /void-packages/srcpkgs/ (default dari XBPS_DISTDIR)
  └── /void-packages/srcpkgs/zig/template → accessible ✓
```

### Routing Command

```python
CMDS_NEED_PKG  →  _run_with_template()
  # 1. find_template(): loop core → extra → multilib
  # 2. stage_vur_template(): copy + inject _package()
  # 3. env["XBPS_CHROOT_CMD"] = "letx"
  # 4. env["XBPS_CHROOT_CMD_ARGS"] = bind mount command
  # 5. subprocess: BACKEND_DIR/xbps-src pkg <nama>

CMDS_NO_PKG    →  _run_xbps_raw()
  # XBPS_SRCPKGDIR = BACKEND_SRCPKGS_DIR (base-files, base-chroot)
  # subprocess: BACKEND_DIR/xbps-src <target>
```

## Alur Data

### `letx search <keyword>`

```
cli.py:cmd_search()
    │
    ├─ ops/search.py:search_packages()
    │       │
    │       └─ repo/index.py:fetch_index()
    │               ├─ cache valid → baca ~/.cache/letx/packages.json
    │               └─ expired     → GET GitHub raw → tulis cache
    │
    └─ utils/print.py:print_package_table()
```

### `letx get <pkg>`

```
cli.py:cmd_get()
    │
    ├─ ops/info.py:get_info()           → cek index + status lokal
    ├─ Sudah lokal & tidak --force?     → print_warn(), exit 0
    └─ repo/fetch.py:download_package()
            │
            └─ GitHub Contents API (rekursif)
                    ├─ tiap file → GET raw.githubusercontent.com
                    └─ tulis ke ~/.config/letx/<kategori>/<pkg>/
```

### `letx -x pkg <nama>`

```
cli.py:cmd_xbps()
    │
    └─ utils/xbps.py:run()
            │
            └─ _run_with_template()
                    │
                    ├─ find_template()          → loop core/extra/multilib
                    ├─ stage_vur_template()     → masterdir/letx-srcpkgs/<pkg>/
                    ├─ build_xbps_env()         → set XBPS_CHROOT_CMD=letx
                    │                              set XBPS_CHROOT_CMD_ARGS
                    └─ subprocess: backend/xbps-src pkg <nama>
                            │
                            └─ chroot via letx.sh
                                    │
                                    └─ inner xbps-src
                                            └─ /void-packages/srcpkgs/<pkg>/ ✓
```

## Setup Development Environment

```bash
# 1. Clone repo
git clone https://github.com/T4n-Labs/Let-X
cd Let-X

# 2. Install dalam mode editable
pip install -e ".[dev]"

# 3. Verifikasi
letx --version
letx --help

# 4. Setup build environment (untuk test letx -x)
letx -x binary-bootstrap
```

> **Catatan editable install:** `BACKEND_DIR` menunjuk ke `letx/backend/` di source tree (writable). Perubahan pada `letx.sh` atau file backend lain langsung berlaku tanpa reinstall.

## Konvensi Kode

**Penamaan:**
- Modul dan fungsi: `snake_case`
- Konstanta di `config.py`: `SCREAMING_SNAKE_CASE`
- Type hints wajib untuk semua fungsi publik

**Import order:**
```python
# 1. stdlib
import os
import sys
from pathlib import Path

# 2. third-party
import httpx
from rich.console import Console

# 3. internal (selalu absolute imports)
from letx.config import CACHE_DIR
from letx.repo.index import fetch_index
```

**Docstring — semua fungsi publik wajib:**
```python
def find_template(pkgname: str) -> tuple[str, Path] | None:
    """
    Cari template VUR di tiga kategori.

    Loop: core → extra → multilib

    Args:
        pkgname: nama package, contoh 'zig'

    Returns:
        (category, pkg_dir) jika ditemukan, None jika tidak.
    """
```

## Menambah Command Baru

1. Tambah subparser di `cli.py:build_parser()`
2. Tambah handler `cmd_<nama>()` di `cli.py`
3. Daftarkan di blok dispatch `main()`
4. Logika bisnis masuk ke `ops/` (bukan di `cli.py`)
5. Akses data masuk ke `repo/` (bukan di `ops/`)
6. Output selalu via `utils/print.py`

**Skeleton:**
```python
# Di build_parser():
p_remove = sub.add_parser("remove", help="Remove a local template")
p_remove.add_argument("name", help="Package name")

# Handler di cli.py:
def cmd_remove(args: argparse.Namespace) -> int:
    from letx.ops.remove import remove_template
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

## Menjalankan Test

```bash
pytest tests/ -v
pytest tests/test_search.py -v
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

## Build Package xbps-src

Let-X sekarang bisa build dirinya sendiri via `letx -x`:

```bash
# Dari direktori Let-X
letx get letx            # download template VUR letx
letx -x pkg letx         # build

# Install
sudo xbps-install \
    --repository=$HOME/.config/letx/hostdir/binpkgs letx
```

Untuk release baru, update `checksum` di template VUR setelah source tarball berubah:
```bash
sha256sum letx-0.2.0.tar.gz
# → update di VUR template
```

## Dependensi

**Runtime:**

| Package    | Versi  | Fungsi                       |
|------------|--------|------------------------------|
| `httpx`    | ≥ 0.27 | HTTP client untuk GitHub API |
| `rich`     | ≥ 13.0 | Pretty terminal output       |
| `argparse` | stdlib | Parsing argumen CLI          |

**Dev:**

| Package        | Fungsi            |
|----------------|-------------------|
| `pytest`       | Test runner       |
| `pytest-httpx` | Mock HTTP request |

**Sistem (untuk `letx -x`):**

| Binary          | Fungsi                                 |
|-----------------|----------------------------------------|
| `xbps-uunshare` | User namespace chroot (via xbps-tools) |
| `xbps-create`   | Buat binary package                    |
| `xbps-rindex`   | Register package ke repo               |

## Catatan Pengembangan Selanjutnya

Beberapa hal yang perlu diperhatikan untuk pengembangan v0.3.0+:

### 1. Staging Cleanup

Saat ini `masterdir/letx-srcpkgs/<pkgname>/` **tidak dihapus** setelah build selesai. Untuk build yang banyak, direktori ini akan terus bertambah. Pertimbangkan cleanup otomatis setelah `proc.returncode == 0` di `_run_with_template()`.

### 2. letx.sh — Kompatibilitas Chroot Style Lain

`letx.sh` ditulis khusus untuk `xbps-uunshare`. Jika sistem menggunakan `bwrap` atau `uchroot` (lihat `common/chroot-style/`), perlu dibuat script padanan:
- `letx-bwrap.sh` untuk sistem yang menggunakan bwrap
- Deteksi otomatis chroot style yang tersedia di `build_xbps_env()`

### 3. `_package()` Injection — Edge Cases

Saat ini injeksi `${pkgname}_package() { :; }` dilakukan dengan cek string sederhana (`f"{func_name}()" not in content`). Ini bisa false-positive jika ada komentar yang menyebut nama fungsi. Pertimbangkan parsing bash yang lebih robust jika diperlukan.

### 4. `LETX_SRCPKGS_DIR` (Legacy)

`~/.config/letx/srcpkgs/` masih ada di `config.py` dan `ensure_dirs()` sebagai legacy. Bisa dihapus di versi berikutnya jika tidak ada yang bergantung padanya.

### 5. Multi-package Template (Subpackage)

Template dengan `$subpackages` (contoh: `discord` + `discord-devel`) belum ditest dengan sistem staging saat ini. `stage_vur_template()` hanya copy satu `pkgname/` — subpackage templates perlu di-handle juga.

*Let-X v0.2.0 · VUR: [github.com/T4n-Labs/vur](https://github.com/T4n-Labs/vur)*

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
