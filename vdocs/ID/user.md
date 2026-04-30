# Let-X — Panduan Pengguna

> **Let-X** adalah CLI tool untuk Void Linux yang memudahkan pencarian, pengelolaan, dan pengunduhan template package dari **VUR (Void User Repository)** — konsep serupa AUR Helper di Arch Linux.

**Binary:** `letx` | **Versi:** 0.1.2 | **Bahasa:** Python 3.11+

---

## Daftar Isi

- [Apa itu Let-X?](#apa-itu-let-x)
- [Persyaratan Sistem](#persyaratan-sistem)
- [Instalasi](#instalasi)
- [Referensi Command](#referensi-command)
  - [letx search](#letx-search)
  - [letx info](#letx-info)
  - [letx list](#letx-list)
  - [letx get](#letx-get)
  - [letx update](#letx-update)
- [Contoh Penggunaan](#contoh-penggunaan)
- [Struktur File Lokal](#struktur-file-lokal)
- [Troubleshooting](#troubleshooting)
- [Uninstall](#uninstall)

---

## Apa itu Let-X?

**Let-X** adalah tool CLI (Command Line Interface) yang berjalan di terminal Void Linux. Fungsinya mirip dengan `yay` atau `paru` di Arch Linux, tetapi untuk ekosistem **VUR (Void User Repository)**.

Dengan Let-X kamu bisa:
- 🔍 **Mencari** package yang tersedia di VUR berdasarkan nama atau deskripsi
- 📋 **Melihat daftar** package per kategori beserta statistiknya
- ℹ️ **Melihat detail** informasi sebuah package termasuk status lokal
- 📁 **Menemukan** template yang sudah diunduh di sistem
- 📥 **Mengunduh** template package ke komputer lokal

> **Catatan:** Fitur `build` dan `install` via `xbps-src` direncanakan untuk v0.2.0.

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
# 1. Clone repo Let-X
git clone https://github.com/T4n-Labs/Let-X
cd Let-X

# 2. Jalankan script instalasi sebagai root
sudo ./install.sh
```

Script akan otomatis melakukan:
1. Membersihkan instalasi lama di `/usr/lib/letx/`
2. Build Python wheel dari source (`letx-*.whl`)
3. Install wheel ke `/usr`
4. Install runtime dependencies (`httpx`, `rich`) ke `/usr/lib/letx/`
5. Membuat wrapper `/usr/bin/letx` dengan `PYTHONPATH` yang benar

Verifikasi instalasi:
```bash
letx --help
letx -v
```

Untuk uninstall:
```bash
sudo ./install.sh uninstall
```

### Metode 2 — via xbps-src

Jika kamu sudah setup `void-packages`:
```bash
# Salin template
cp -r xbps-template/letx ~/void-packages/srcpkgs/letx

# Build dan install
cd ~/void-packages
./xbps-src pkg letx
sudo xbps-install --repository=/home/$USER/.config/xbps-src/hostdir/binpkgs letx
```

---

## Referensi Command

### `letx search`

Mencari package di VUR berdasarkan nama atau deskripsi.

```
letx search <keyword> [-c CATEGORY]
letx search "<deskripsi>" [-c CATEGORY]
letx search -t <pkg_name>
```

| Argumen / Opsi | Keterangan |
|---|---|
| `<keyword>` | Nama package atau kata yang dicari |
| `"<deskripsi>"` | Frasa deskripsi (gunakan tanda kutip untuk multi-kata) |
| `-c`, `--category CATEGORY` | Filter by kategori: `core` \| `extra` \| `multilib` |
| `-t`, `--template PKG_NAME` | Cari template yang sudah diunduh di lokal |

**Cari berdasarkan nama:**
```bash
letx search discord
letx search browser
letx search zen -c extra
```

**Cari berdasarkan deskripsi:**
```bash
# Mencari di field 'description' pada packages.json
letx search "Programming Language"
letx search "web browser"
letx search "Windows" -c multilib
```

**Cari template lokal (`-t`):**

Mengecek direktori secara berurutan: `core → extra → multilib`
```bash
letx search -t discord
letx search -t wine
```

Contoh output `-t` (template ditemukan):
```
╭────────── discord (local template) ──────────╮
│ Package     : discord                         │
│ Category    : extra                           │
│ Location    : ~/.config/letx/extra/discord    │
│ Version     : 0.0.134                         │
│ Description : Chat and VOIP application       │
│ Homepage    : https://discord.com             │
│ Maintainer  : Gh0sT4n                         │
│                                               │
│ Files:                                        │
│   • files/zprofile                            │
│   • template                                  │
╰───────────────────────────────────────────────╯
```

Contoh output `-t` (template tidak ditemukan):
```
! Template 'discord' not found locally.
  Checked: core → extra → multilib
  Run 'letx get discord' to download it.
```

---

### `letx info`

Menampilkan informasi detail package, atau menjelajahi package terbaru per kategori.

```
letx info <pkg_name>
letx info <all|core|extra|multilib>
letx info -c <CATEGORY>
letx info -t <pkg_name>
```

| Argumen / Opsi | Keterangan |
|---|---|
| `<pkg_name>` | Tampilkan detail lengkap package tertentu |
| `all` | Tampilkan 20 package yang terakhir ditambahkan (semua kategori) |
| `core` | Tampilkan 20 package terbaru di kategori `core` |
| `extra` | Tampilkan 20 package terbaru di kategori `extra` |
| `multilib` | Tampilkan 20 package terbaru di kategori `multilib` |
| `-c`, `--category CATEGORY` | List semua package di kategori (`all`\|`core`\|`extra`\|`multilib`) |
| `-t`, `--template PKG_NAME` | Tampilkan detail template lokal |

**Contoh penggunaan:**
```bash
# Detail package tertentu
letx info discord
letx info wine

# 20 package terbaru
letx info all
letx info extra
letx info multilib

# List semua package di kategori
letx info -c core
letx info -c all

# Info template lokal
letx info -t discord
```

**Contoh output detail package:**
```
╭────────────────── discord ──────────────────╮
│ Name        : discord                        │
│ Version     : 0.0.134                        │
│ Category    : extra                          │
│ Description : Chat and VOIP application      │
│ Repo Path   : extra/discord                  │
│ Homepage    : https://discord.com            │
│ Maintainer  : Gh0sT4n                        │
╰──────────────────────────────────────────────╯
  Status      : ✘ Not fetched yet
```

Jika `letx info` dijalankan tanpa argumen:
```
[ERROR] No Options
usage: letx info [-h] [-c CATEGORY] [-t PKG_NAME] [name]
...
```

---

### `letx list`

Menampilkan daftar package dari VUR. Membutuhkan minimal satu argumen atau opsi.

```
letx list <all|core|extra|multilib>
letx list -c <CATEGORY>
letx list -p [CATEGORY]
```

| Argumen / Opsi | Keterangan |
|---|---|
| `all` | Tampilkan 20 package yang terakhir ditambahkan |
| `core` | Tampilkan 20 package terbaru di `core` |
| `extra` | Tampilkan 20 package terbaru di `extra` |
| `multilib` | Tampilkan 20 package terbaru di `multilib` |
| `-c`, `--category CATEGORY` | List **semua** package di kategori tertentu |
| `-p`, `--package [CATEGORY]` | Tampilkan statistik jumlah package |

**Contoh penggunaan:**
```bash
# 20 package terbaru
letx list all
letx list extra

# Semua package di kategori tertentu
letx list -c core
letx list -c multilib

# Statistik jumlah package
letx list -p            # semua kategori
letx list -p extra      # kategori tertentu
letx list -p core
```

**Contoh output statistik (`-p`):**
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

Jika `letx list` dijalankan tanpa argumen:
```
[ERROR] No Options
usage: letx list [-h] [-c CATEGORY] [-p [CATEGORY]] [scope]
...
```

---

### `letx get`

Mengunduh template package dari VUR ke direktori lokal.

```
letx get <pkg_name> [-f]
```

| Argumen / Opsi | Keterangan |
|---|---|
| `<pkg_name>` | Nama package yang akan diunduh (wajib) |
| `-f`, `--force` | Re-download meski template sudah ada di lokal |

**Contoh penggunaan:**
```bash
# Unduh template
letx get discord
letx get wine

# Paksa re-download (update template)
letx get discord --force
letx get wine -f
```

**Contoh output:**
```
→ Fetching template 'discord' (extra) ...
  ↓ extra/discord/template
  ↓ extra/discord/files/zprofile
✔ Template saved to: /home/user/.config/letx/extra/discord
→ You can now build it with xbps-src (coming soon).
```

Template disimpan di:
- Package **core** → `~/.config/letx/core/<pkg>/`
- Package **extra** → `~/.config/letx/extra/<pkg>/`
- Package **multilib** → `~/.config/letx/multilib/<pkg>/`

---

### `letx update`

Memperbarui cache index package dari VUR.

```
letx update
```

```bash
letx update
```

```
→ Refreshing package index from VUR ...
✔ Index updated — 23 packages available.
```

> Cache di `~/.cache/letx/packages.json` otomatis diperbarui setiap 1 jam. Gunakan `letx update` untuk memperbarui sekarang juga.

---

## Contoh Penggunaan

### Alur Kerja Tipikal

```bash
# 1. Perbarui index (opsional pada pertama kali)
letx update

# 2. Cari package
letx search discord

# 3. Lihat detail lengkap
letx info discord

# 4. Unduh template
letx get discord

# 5. Template sudah tersedia di:
ls ~/.config/letx/extra/discord/
letx search -t discord    # verifikasi
```

### Menjelajahi Repository

```bash
# Lihat package yang baru ditambahkan
letx list all
letx list extra

# Jelajahi kategori tertentu
letx list -c core
letx list -c multilib

# Cek jumlah package
letx list -p

# Cari package gaming
letx search "games"
letx search "Windows" -c multilib

# Cari browser
letx search browser -c extra
```

### Mengelola Template Lokal

```bash
# Cek apakah template sudah diunduh
letx search -t discord
letx info -t wine

# Unduh beberapa template
letx get discord
letx get wine
letx get zen-browser

# Update template yang sudah ada
letx get discord --force
```

---

## Struktur File Lokal

Setelah menggunakan Let-X, berikut direktori dan file yang dibuat di sistem:

```
~/.config/letx/                   ← Direktori konfigurasi utama
├── core/                         ← Template dari kategori core
│   └── <nama-package>/
│       ├── template              ← File template utama xbps-src
│       ├── files/                ← File tambahan (jika ada)
│       └── patches/              ← File patch (jika ada)
├── extra/                        ← Template dari kategori extra
│   └── <nama-package>/
└── multilib/                     ← Template dari kategori multilib
    └── <nama-package>/

~/.cache/letx/                    ← Direktori cache
└── packages.json                 ← Salinan lokal index VUR (diperbarui tiap 1 jam)

/usr/bin/letx                     ← Binary wrapper
/usr/lib/letx/                    ← Source Python + runtime deps
/usr/share/letx/MANIFEST          ← Metadata instalasi
```

---

## Troubleshooting

### `letx: command not found`

Binary tidak terinstall atau tidak ada di PATH.
```bash
# Cek apakah file ada
ls -la /usr/bin/letx

# Jika tidak ada, jalankan ulang installer
sudo ./install.sh
```

### `Failed to fetch index from GitHub and no local cache found`

Let-X tidak bisa terhubung ke internet dan tidak ada cache lokal.
```bash
# Cek koneksi
ping github.com

# Paksa refresh cache
letx update
```

### `Package 'xxx' not found in VUR`

Package mungkin belum ada di VUR, atau nama salah ketik.
```bash
# Cari dengan nama parsial
letx search xxx

# Perbarui index dulu (mungkin ada package baru)
letx update
letx search xxx
```

### `Template 'xxx' not found locally`

Template belum diunduh.
```bash
letx get xxx
```

### `Python >= 3.11 required`

Versi Python terlalu lama. Update via xbps:
```bash
sudo xbps-install -Su python3
python3 --version
```

### Warning `Target directory already exists` saat install

Ini terjadi jika menginstall ulang di atas instalasi lama. `install.sh` terbaru menangani ini otomatis dengan membersihkan `/usr/lib/letx/` sebelum install.

Jika masih terjadi, bersihkan manual:
```bash
sudo rm -rf /usr/lib/letx
sudo ./install.sh
```

---

## Uninstall

```bash
# Dari direktori repo Let-X
sudo ./install.sh uninstall
```

Script akan menghapus:
- `/usr/bin/letx`
- `/usr/lib/letx/`
- `/usr/share/letx/`
- `/usr/share/man/man1/letx.1` (jika ada)

Data pengguna **tidak** dihapus otomatis. Untuk membersihkan semuanya:
```bash
rm -rf ~/.config/letx ~/.cache/letx
```

---

*Let-X v0.1.2 — VUR: [github.com/T4n-Labs/vur](https://github.com/T4n-Labs/vur)*
