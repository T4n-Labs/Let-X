# Let — Dokumentasi untuk User

> **Let** adalah CLI tool untuk Void Linux yang memudahkan pencarian, pengelolaan, dan pengambilan template package dari **VUR (Void User Repository)** — konsep serupa AUR Helper di Arch Linux.

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

# Untuk Pengguna Umum

## Apa itu Let?

**Let** adalah tool CLI (Command Line Interface) yang berjalan di terminal Void Linux. Fungsinya mirip dengan `yay` atau `paru` di Arch Linux, tetapi untuk ekosistem **VUR (Void User Repository)**.

Dengan Let kamu bisa:
- 🔍 **Mencari** package yang tersedia di VUR
- 📋 **Melihat** daftar semua package
- ℹ️ **Melihat detail** informasi sebuah package
- 📥 **Mengunduh** template package ke komputer lokal

> **Catatan:** Fitur `build` dan `install` via `xbps-src` sedang dalam pengembangan dan akan hadir di versi berikutnya.

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
* @T4n-Labs
* @Gh0sT4n