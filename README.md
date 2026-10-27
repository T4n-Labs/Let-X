# Let-X

**Let-X** adalah alat bantu CLI (*Command Line Interface*) yang ringan dan cepat untuk mengelola **Void User Repository (VUR)**. Dibangun menggunakan Python murni (tanpa dependensi pihak ketiga), Let-X memudahkan pengguna untuk mencari, mengambil, memperbarui, dan melihat informasi detail paket dari repositori VUR.

## ✨ Fitur

- 🚀 **Cepat & Ringan**: Hanya menggunakan *Python Standard Library* (`urllib`, `json`, `re`, `argparse`, `pathlib`), sehingga tidak memerlukan `pip install` untuk dependensi eksternal.
- 🔍 **Pencarian Fleksibel**: Cari paket berdasarkan nama, deskripsi, atau kategori.
- 📦 **Manajemen Template**: Unduh dan perbarui file `template` Void Linux secara otomatis ke direktori konfigurasi lokal.
- 📊 **Informasi Detail Terformat**: Tampilkan metadata paket dan dependensi (`hostmakedepends`, `makedepends`, `depends`) dalam format grid 4 kolom yang rapi dan mudah dibaca.
- 💾 **Caching Lokal**: Database JSON disimpan secara lokal di `~/.config/letx/db/` untuk akses offline yang cepat setelah sinkronisasi awal.

## 📦 Instalasi

### Prasyarat
- Python 3.10 atau lebih baru
- [`uv`](https://docs.astral.sh/uv/) (Direkomendasikan untuk manajemen paket dan build yang cepat)

### Langkah Instalasi

1. **Clone repositori ini:**
   ```bash
   git clone https://github.com/T4n-Labs/letx.git
   cd letx
   ```

2. **Instal menggunakan `uv` (Global/Tool):**
   ```bash
   uv tool install .
   ```
   *Atau, untuk instalasi mode pengembangan (editable):*
   ```bash
   uv pip install -e .
   ```

3. **Verifikasi instalasi:**
   ```bash
   letx --help
   ```

## 🚀 Penggunaan

### 1. Memperbarui Database
Sebelum menggunakan fitur lainnya, sinkronkan database lokal dengan repositori VUR terbaru:
```bash
letx update
```
*Output:*
```text
🔄 Updating VUR database...
   ⤓ Downloading packages.json...
   ⤓ Downloading search.json...
   ⤓ Downloading index.json...
   ⤓ Downloading categories.json...
✔ Database successfully updated!
```

### 2. Mencari Paket
Cari paket berdasarkan nama, deskripsi, atau kategori (misalnya: "browser", "dinit", "core"):
```bash
letx search browser
```
*Output:*
```text
🔍 Found 5 package(s) for 'browser':

PACKAGE NAME                   | CATEGORY   | DESCRIPTION
--------------------------------------------------------------------------------
brave                          | extra      | Web browser that blocks ads and t...
brave-origin                   | extra      | Minimalist browser from the maker...
floorp                         | extra      | Firefox fork seeking balance betw...
helium-browser                 | extra      | Private, fast, and honest web bro...
zen-browser                    | extra      | Performance oriented Firefox-base...
```

### 3. Mengambil Template Paket
Unduh file `template` Void Linux untuk paket tertentu ke direktori konfigurasi lokal:
```bash
letx get calamares
```

### 4. Memperbarui Template Paket
Jika maintainer merilis revisi baru pada template, perbarui template spesifik tanpa mengunduh ulang seluruh database:
```bash
letx update calamares
```

### 5. Melihat Informasi Detail Paket
Tampilkan metadata lengkap paket, termasuk dependensi yang diformat dalam grid 4 kolom:
```bash
letx info calamares
```
*Output:*
```text
Name Package    : calamares
Version         : 3.4.2
Revision        : 3
Archs           : aarch64, x86_64, x86_64-musl, ...
Description     : Distribution-independent installer framework
Maintainer      : Naz <ndpm13@ch-naseem.com>
Distributor     : Gh0sT4n <darskevoid@gmail.com>
License         : BSD-2-Clause, GPL-3.0-or-later, ...
Homepage        : https://calamares.io
Build Style     : cmake
Hostmakedepends :
-) git                   -) extra-cmake-modules -) pkg-config          -) gettext            
-) ckbcomp               -) kcoreaddons           -) python3-QtPy        -) libpwquality       
-) python3-yaml          -) python3-jsonschema  
Makedepends     :
-) python3-devel         -) python3-jsonschema  -) yaml-cpp-devel      -) python3-yaml       
-) boost-devel           -) qt6-base-devel      -) python3-devel       -) kpmcore-devel      
-) qt6-tools             -) qt6-translations    -) boost               -) boost-python3      
-) python3-QtPy          -) qt6-svg-devel       -) libpwquality        -) qt6-webengine      
-) plasma-framework-devel -) qt6-webengine     
Depends         :
-) kconfig               -) kcoreaddons         -) kiconthemes         -) ki18n              
-) kio                   -) ksolid              -) boost               -) ckbcomp            
-) polkit-qt6            -) gtk-update-icon-cache -) plasma-framework  -) squashfs-tools     
-) libpwquality        -) icu                 -) rsync               
```

## 📂 Struktur Direktori & Konfigurasi

Let-X menyimpan data caching dan template di direktori konfigurasi pengguna (`~/.config/letx/`):

```text
~/.config/letx/
├── db/                  # Cache database JSON lokal
│   ├── packages.json
│   ├── search.json
│   ├── index.json
│   └── categories.json
├── core/                # Template paket kategori 'core'
│   └── calamares/
│       └── template
├── extra/               # Template paket kategori 'extra'
└── multilib/            # Template paket kategori 'multilib'
```

## 🏗️ Struktur Proyek

```text
letx/
├── letx/
│   ├── __init__.py
│   ├── main.py          # Entry point CLI dan parsing argumen
│   └── src/
│       ├── __init__.py
│       ├── config.py    # Konstanta URL dan path direktori
│       ├── cmd.py       # Logika perintah (get, search, update, info)
│       └── utility.py   # Fungsi utilitas (fetch, parse template, format grid)
├── pyproject.toml       # Konfigurasi build dan metadata proyek
├── LICENSE              # Lisensi proyek
└── README.md            # Dokumentasi ini
```

## 🛠️ Pengembangan (Development)

Jika Anda ingin berkontribusi atau memodifikasi kode:

1. Clone repositori dan masuk ke direktori proyek.
2. Sinkronkan lingkungan pengembangan:
   ```bash
   uv sync
   ```
3. Jalankan secara langsung tanpa menginstal:
   ```bash
   uv run letx --help
   ```

## 📜 Lisensi

Proyek ini didistribusikan di bawah lisensi yang sama dengan repositori induknya. Silakan lihat file [`LICENSE`](LICENSE) untuk detail lebih lanjut.

## 👥 Kontributor

- **Gh0sT4n** - *Lead Developer & Distributor* ([darskevoid@gmail.com](mailto:darskevoid@gmail.com))