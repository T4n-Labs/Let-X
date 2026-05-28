# Let-X — Panduan Pengguna

> **Let-X** adalah CLI tool untuk Void Linux yang memudahkan pencarian, pengelolaan, pengunduhan, dan pembangunan package dari **VUR (Void User Repository)** — mirip seperti `yay` atau `paru` di Arch Linux.

**Binary:** `letx` | **Versi:** 0.2.0 | **Bahasa Pemograman:** Python 3.11+

## Daftar Isi

- [Persyaratan Sistem](#persyaratan-sistem)
- [Instalasi](#instalasi)
- [Perintah Lengkap](#perintah-lengkap)
  - [letx search](#letx-search)
  - [letx info](#letx-info)
  - [letx list](#letx-list)
  - [letx get](#letx-get)
  - [letx update](#letx-update)
  - [letx -x (xbps-src)](#letx--x-xbps-src)
- [Alur Kerja Tipikal](#alur-kerja-tipikal)
- [Struktur File Lokal](#struktur-file-lokal)
- [Troubleshooting](#troubleshooting)
- [Uninstall](#uninstall)

## Persyaratan Sistem

| Komponen         | Persyaratan                         |
|------------------|-------------------------------------|
| Sistem Operasi   | Void Linux (glibc)                  |
| Python           | 3.11 atau lebih baru                |
| Koneksi Internet | Untuk fetch index dan template VUR  |

## Instalasi

```bash
# 1. Clone repo Let-X
git clone https://github.com/T4n-Labs/Let-X
cd Let-X

# 2. Jalankan script instalasi sebagai root
sudo ./install.sh
```

Verifikasi:
```bash
letx --version
letx --help
```

Uninstall:
```bash
sudo ./install.sh uninstall
```

## Perintah Lengkap

### `letx search`

Mencari package di VUR berdasarkan nama atau deskripsi.

```bash
letx search <keyword>
letx search "<deskripsi>"
letx search <keyword> -c <kategori>
letx search -t <nama_package>
```

| Opsi               | Keterangan                                       |
|--------------------|--------------------------------------------------|
| `-c`, `--category` | Filter kategori: `core` \| `extra` \| `multilib` |
| `-t`, `--template` | Cari template yang sudah diunduh di lokal        |

**Contoh:**
```bash
letx search discord
letx search browser -c extra
letx search "Programming Language"
letx search -t discord          # cek apakah sudah diunduh
```

### `letx info`

Menampilkan informasi detail package.

```bash
letx info <nama_package>
letx info all | core | extra | multilib
letx info -c <kategori>
letx info -t <nama_package>
```

| Argumen / Opsi                  | Keterangan                      |
|---------------------------------|---------------------------------|
| `<nama_package>`                | Detail lengkap satu package     |
| `all / core / extra / multilib` | 20 package terbaru per kategori |
| `-c`, `--category`              | List semua package di kategori  |
| `-t`, `--template`              | Detail template lokal           |

**Contoh:**
```bash
letx info discord
letx info all
letx info -c extra
letx info -t discord
```

### `letx list`

Menampilkan daftar package dari VUR.

```bash
letx list all | core | extra | multilib
letx list -c <kategori>
letx list -p [kategori]
```

| Argumen / Opsi                  | Keterangan                         |
|---------------------------------|------------------------------------|
| `all / core / extra / multilib` | 20 package terbaru                 |
| `-c`, `--category`              | Semua package di kategori tertentu |
| `-p`, `--package`               | Statistik jumlah package           |

**Contoh:**
```bash
letx list all
letx list -c core
letx list -p              # statistik semua kategori
letx list -p extra        # statistik satu kategori
```

**Contoh output statistik:**
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

### `letx get`

Mengunduh template package dari VUR ke direktori lokal.

```bash
letx get <nama_package>
letx get <nama_package> --force
```

| Opsi            | Keterangan                           |
|-----------------|--------------------------------------|
| `-f`, `--force` | Re-download meski template sudah ada |

**Contoh:**
```bash
letx get discord
letx get discord --force    # update template
```

Template disimpan di `~/.config/letx/<kategori>/<nama_package>/`.

### `letx update`

Memperbarui cache index package dari VUR.

```bash
letx update
```

> Cache diperbarui otomatis setiap 1 jam. Gunakan perintah ini untuk memperbarui sekarang juga.

### `letx -x` (xbps-src)

Integrasi langsung dengan `xbps-src` untuk build dan install package dari template VUR.

```bash
letx -x <target> [nama_package] [opsi]
```

#### Setup Awal (Wajib Sekali)

Sebelum bisa build package, jalankan `binary-bootstrap` satu kali untuk menyiapkan environment build:

```bash
letx -x binary-bootstrap
```

> Proses ini membutuhkan waktu beberapa menit dan koneksi internet. Hanya perlu dilakukan **sekali**.

#### Build Package

Setelah bootstrap selesai, build package langsung dari template VUR:

```bash
# Download template dulu (jika belum)
letx get <nama_package>

# Build package
letx -x pkg <nama_package>
```

Package hasil build tersimpan di `~/.config/letx/hostdir/binpkgs/`.

#### Install Package Hasil Build

```bash
sudo xbps-install --repository=$HOME/.config/letx/hostdir/binpkgs <nama_package>
```

#### Target Lain yang Tersedia

| Target                   | Keterangan                            |
|--------------------------|---------------------------------------|
| `pkg <nama>`             | Build lengkap + buat file `.xbps`     |
| `fetch <nama>`           | Download source distfile saja         |
| `extract <nama>`         | Extract source                        |
| `build <nama>`           | Kompilasi saja                        |
| `install <nama>`         | Install ke destdir                    |
| `clean <nama>`           | Bersihkan build directory             |
| `show <nama>`            | Tampilkan info template               |
| `show-build-deps <nama>` | Tampilkan build dependencies          |
| `binary-bootstrap`       | Setup environment build (sekali saja) |
| `zap`                    | Reset/bersihkan masterdir             |

**Contoh lengkap:**
```bash
letx -x fetch zig           # download source
letx -x extract zig         # extract
letx -x build zig           # kompilasi
letx -x pkg zig             # build + package sekaligus (paling umum)
letx -x show zig            # cek info template
letx -x clean zig           # bersihkan setelah build
```

## Alur Kerja Tipikal

### Pertama kali menggunakan Let-X

```bash
# 1. Setup environment build (hanya sekali)
letx -x binary-bootstrap

# 2. Perbarui index VUR
letx update
```

### Mencari dan Menginstall Package

```bash
# 1. Cari package
letx search <nama_package>

# 2. Lihat detail
letx info <nama_package>

# 3. Download template
letx get <nama_pacakge>

# 4. Build
letx -x pkg <nama_pacakge>

# 5. Install
sudo xbps-install --repository=$HOME/.config/letx/hostdir/binpkgs <nama_package>
```

### Update Package

```bash
# Update template ke versi terbaru
letx get <nama_package> --force

# Build ulang
letx -x pkg <nama_package>

# Install versi baru
sudo xbps-install --repository=$HOME/.config/letx/hostdir/binpkgs <nama_package>
```

## Struktur File Lokal

```
~/.config/letx/
├── core/                    ← Template kategori core
│   └── <package>/
│       ├── template
│       ├── files/
│       └── patches/
├── extra/                   ← Template kategori extra
│   └── <package>/
├── multilib/                ← Template kategori multilib
│   └── <package>/
├── masterdir/               ← Environment build xbps-src
└── hostdir/
    └── binpkgs/             ← Package .xbps hasil build

~/.cache/letx/
└── packages.json            ← Cache index VUR (auto-refresh 1 jam)
```

## Troubleshooting

### `letx: command not found`
```bash
# Cek apakah file ada
ls -la /usr/bin/letx

# Jika tidak ada, install ulang
sudo ./install.sh
```

### `Failed to fetch index from GitHub`

Koneksi internet bermasalah atau tidak ada cache lokal.
```bash
ping github.com
letx update
```

### `Package 'xxx' not found in VUR`

Package belum ada atau nama salah.
```bash
letx search xxx
letx update && letx search xxx
```

### `Template 'xxx' not found locally`

Template belum diunduh.
```bash
letx get xxx
```

### Build error saat `letx -x pkg`

Pastikan `binary-bootstrap` sudah dijalankan:
```bash
letx -x binary-bootstrap
```

Jika environment build rusak, reset dan ulangi:
```bash
letx -x zap
letx -x binary-bootstrap
```

## Uninstall

```bash
sudo ./install.sh uninstall
```

Untuk menghapus semua data pengguna juga:
```bash
rm -rf ~/.config/letx ~/.cache/letx
```

*Let-X v0.2.0 · VUR: [github.com/T4n-Labs/vur](https://github.com/T4n-Labs/vur)*

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
