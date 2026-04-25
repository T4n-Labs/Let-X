# Let-X — Dokumentasi untuk User

> **Let-X** adalah CLI tool untuk Void Linux yang memudahkan pencarian, pengelolaan, dan pengambilan template package dari **VUR (Void User Repository)** — konsep serupa AUR Helper di Arch Linux.

## Daftar Isi

**Untuk Pengguna Umum**
- [Apa itu Let-X?](#apa-itu-let-x)
- [Persyaratan Sistem](#persyaratan-sistem)
- [Instalasi](#instalasi)
- [Referensi Command](#referensi-command)
- [Contoh Penggunaan](#contoh-penggunaan)
- [Struktur File Lokal](#struktur-file-lokal)
- [Troubleshooting](#troubleshooting)
- [Uninstall](#uninstall)

# Untuk Pengguna Umum

## Apa itu Let-X?

**Let-X** adalah tool CLI (Command Line Interface) yang berjalan di terminal Void Linux. Fungsinya mirip dengan `yay` atau `paru` di Arch Linux, tetapi untuk ekosistem **VUR (Void User Repository)**.

Dengan Let-X kamu bisa:
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
# 1. Clone repo Let-X
git clone https://github.com/T4n-Labs/Let-X
cd let

# 2. Jalankan script instalasi sebagai root
sudo ./install.sh
```

Script ini akan secara otomatis:
- Menyalin source ke `/usr/lib/letx/`
- Menginstall dependensi Python (`typer`, `httpx`, `rich`) ke `/usr/lib/letx/`
- Membuat binary wrapper di `/usr/bin/letx`

Setelah selesai, cek instalasi:
```bash
letx --help
```

### Metode 2 — Instalasi via xbps-src (Paket Resmi)

Jika kamu sudah setup `void-packages`:
```bash
# Salin template ke void-packages
cp -r xbps-template/template ~/void-packages/srcpkgs/letx

# Build dan install
cd ~/void-packages
./xbps-src pkg letx
sudo xbps-install --repository=hostdir/binpkgs letx
```

## Referensi Command

### `letx search`

Mencari package di VUR berdasarkan kata kunci.

```
letx search <keyword> [--category <kategori>]
```

| Argumen / Opsi | Keterangan |
|---|---|
| `<keyword>` | Kata kunci pencarian (wajib) |
| `--category`, `-c` | Filter hasil berdasarkan kategori (`core`, `extra`, `multilib`) |

**Contoh:**
```bash
# Cari semua package yang mengandung kata "browser"
letx search browser

# Cari hanya di kategori extra
letx search browser --category extra

# Cari dengan shorthand -c
letx search discord -c extra
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

### `letx info`

Menampilkan informasi lengkap sebuah package.

```
letx info <nama-package>
```

| Argumen | Keterangan |
|---|---|
| `<nama-package>` | Nama package yang ingin dilihat (wajib, case-insensitive) |

**Contoh:**
```bash
letx info discord
letx info wine
letx info zen-browser
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

### `letx list`

Menampilkan semua package yang tersedia di VUR.

```
letx list [--category <kategori>]
```

| Opsi | Keterangan |
|---|---|
| `--category`, `-c` | Filter berdasarkan kategori (`core`, `extra`, `multilib`) |

**Contoh:**
```bash
# Tampilkan semua package
letx list

# Hanya tampilkan package di kategori multilib
letx list --category multilib

# Shorthand
letx list -c core
```

### `let get`

Mengunduh template package dari VUR ke direktori lokal `~/.config/let/`.

```
letx get <nama-package> [--force]
```

| Argumen / Opsi | Keterangan |
|---|---|
| `<nama-package>` | Nama package yang akan diunduh (wajib) |
| `--force`, `-f` | Paksa re-download meski template sudah ada lokal |

**Contoh:**
```bash
# Download template discord
letx get discord

# Download ulang (update template)
letx get discord --force

# Shorthand force
letx get wine -f
```

**Output:**
```
→ Mengambil template 'discord' (extra) ...
  ↓ extra/discord/template
  ↓ extra/discord/files/zprofile
✔ Template berhasil disimpan ke: /home/user/.config/let/extra/discord
→ Selanjutnya kamu bisa build dengan xbps-src (coming soon).
```

### `letx update`

Memperbarui cache index package dari VUR. Berguna jika ada package baru yang ditambahkan ke VUR.

```
letx update
```

**Contoh:**
```bash
letx update
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
letx update

# 2. Cari package yang kamu inginkan
letx search discord

# 3. Cek detail package
letx info discord

# 4. Download templatenya
letx get discord

# 5. Template sekarang ada di:
ls ~/.config/letx/extra/discord/
```

### Eksplorasi Package Berdasarkan Kategori

```bash
# Lihat semua package core (package sistem dasar)
letx list --category core

# Lihat semua package multilib (untuk kompatibilitas 32-bit / Wine)
letx list --category multilib

# Lihat semua package extra (aplikasi pihak ketiga)
letx list --category extra
```

## Struktur File Lokal

Setelah menggunakan Let-X, berikut file dan direktori yang dibuat di sistem kamu:

```
~/.config/letx/              ← Direktori utama konfigurasi
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

### `letx: command not found`

Binary tidak terpasang di PATH. Coba:
```bash
# Cek apakah file ada
ls -la /usr/bin/letx

# Jika tidak ada, jalankan ulang instalasi
sudo ./install.sh
```

### `Gagal fetch index dari GitHub dan tidak ada cache lokal`

Letx tidak bisa terhubung ke internet dan tidak ada cache lokal tersedia.
```bash
# Cek koneksi internet
ping github.com

# Jika terhubung tapi masih gagal, coba perbarui index secara manual
letx update
```

### `Package 'xxx' tidak ditemukan di VUR`

Kemungkinan package belum ada di VUR, atau nama salah ketik.
```bash
# Cari dengan nama parsial
letx search xxx

# Perbarui index dulu, mungkin package baru ditambahkan
letx update
lext search xxx
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
- `/usr/bin/letx`
- `/usr/lib/letx/`
- `/usr/share/letx/`
- `/usr/share/man/man1/letx.1` (jika ada)

Data cache dan konfigurasi lokal **tidak** dihapus otomatis. Hapus manual jika diperlukan:
```bash
rm -rf ~/.config/let ~/.cache/letx
```

---
* @T4n-Labs
* @Gh0sT4n