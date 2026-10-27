# Language/Bahasa
- [EN](#void-packaging-for-letx)
- [ID](#void-packaging-untuk-letx)

# Void Packaging for letx

This folder contains the `xbps-src` template used to build `letx` into a 
native XBPS package (`.xbps`), rather than just a manual copy using `install.sh`.

## Structure

```
template/
└── letx/
    └── template
```

This structure is intentionally designed to match the official 
`void-packages` repository, making it a drop-in ready setup.

## How to Use

1. Clone `void-packages` (if you haven't already):

   ```sh
   git clone --depth=1 [https://github.com/void-linux/void-packages.git](https://github.com/void-linux/void-packages.git)
   cd void-packages
   ./xbps-src binary-bootstrap

```

2. Copy this template into `void-packages`:
```sh
cp -r /path/to/letx/template/letx srcpkgs/letx

```

3. Calculate the official release tarball checksum, and replace `checksum=SKIP`
in the template with the actual hash:
```sh
./xbps-src fetch letx
./xbps-src update-checksums letx

```


4. Build the package:
```sh
./xbps-src pkg letx

```

5. Install the built package:
```sh
sudo xbps-install --repository=hostdir/binpkgs letx
```

## Updating the Version

Whenever a new release comes out, update the `template` file:

1. Update `version=`
2. Reset `revision=1`
3. Update the `checksum` using `./xbps-src update-checksums letx`

If you are only fixing packaging issues without changing the source code
(e.g., modifying `do_install`), simply increment the `revision`
(`revision=2`, etc.) and leave `version` unchanged.

# Void Packaging untuk letx

Folder ini isinya template `xbps-src`, dipakai buat build `letx` jadi paket
XBPS asli (`.xbps`), bukan cuma copy manual pakai `install.sh`.

## Struktur

```
template/
└── letx/
    └── template
```

Struktur ini sengaja dibuat sama persis kayak struktur repo resmi
`void-packages`, biar tinggal drop-in.

## Cara pakai

1. Clone `void-packages` (kalau belum ada):

   ```sh
   git clone --depth=1 https://github.com/void-linux/void-packages.git
   cd void-packages
   ./xbps-src binary-bootstrap
   ```

2. Copy template ini ke dalam `void-packages`:

   ```sh
   cp -r /path/ke/letx/template/letx srcpkgs/letx
   ```

3. Hitung checksum asli tarball release, ganti `checksum=SKIP` di template
   dengan hash sebenarnya:

   ```sh
   ./xbps-src fetch letx
   ./xbps-src update-checksums letx
   ```

4. Build paketnya:

   ```sh
   ./xbps-src pkg letx
   ```

5. Install hasil buildnya:

   ```sh
   sudo xbps-install --repository=hostdir/binpkgs letx
   ```

## Update versi

Setiap ada rilis baru, di file `template`:

1. Update `version=`
2. Reset `revision=1`
3. Update `checksum` pakai `./xbps-src update-checksums letx`

Kalau cuma perbaikan packaging tanpa ganti source code (misal ubah
`do_install`), cukup naikkan `revision` (`revision=2`, dst), jangan ubah
`version`.
