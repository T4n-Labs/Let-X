# Core Let-X

> Minimal `srcpkgs/` layer for integrating **xbps-src** into custom projects.  
> Maintains all required bootstrap packages and symlinks for building Void Linux packages.

## What is this?

**Core Let-X** adalah kumpulan folder `srcpkgs/` yang wajib ada agar `xbps-src` dapat berfungsi di dalam proyek Let-X. Semua folder bootstrap, symlink subpackage, dan dependensi `binary-bootstrap` telah dikurasi dan didokumentasikan.

## Required srcpkgs (43 Folder)

### Folder Utama (direktori berisi `template`)

| Folder                       | Keterangan                                              |
|------------------------------|---------------------------------------------------------|
| `base-files/`                | Struktur direktori dasar filesystem                     |
| `base-chroot/`               | Meta-paket bootstrap utama                              |
| `base-chroot-cyclic-solver/` | Solver dependensi siklik saat bootstrap                 |
| `gcc/`                       | Compiler C/C++ — induk banyak symlink                   |
| `binutils/`                  | Toolchain: assembler & linker                           |
| `glibc/`                     | C library (target glibc)                                |
| `musl/`                      | C library (target musl)                                 |
| `zlib/`                      | Kompresi                                                |
| `curl/`                      | HTTP client — induk `libcurl` & `libcurl-devel`         |
| `zstd/`                      | Kompresi zstandard — induk `libzstd` & `libzstd-devel`  |
| `xbps/`                      | Package manager                                         |
| `jansson/`                   | JSON library                                            |
| `c-ares/`                    | Async DNS                                               |
| `nghttp2/`                   | HTTP/2 library                                          |
| `libssh2/`                   | SSH library                                             |
| `libev/`                     | Event loop library                                      |
| `chroot-bash/`               | Bash khusus chroot                                      |
| `chroot-git/`                | Git khusus chroot                                       |
| `chroot-distcc/`             | Distcc khusus chroot                                    |

### Symlink Wajib (subpackage)

| Symlink              | → Target   |
|----------------------|------------|
| `binutils-devel/`    | `binutils` |
| `binutils-libs/`     | `binutils` |
| `libgcc/`            | `gcc`      |
| `libgcc-devel/`      | `gcc`      |
| `libstdc++/`         | `gcc`      |
| `libstdc++-devel/`   | `gcc`      |
| `libatomic/`         | `gcc`      |
| `libatomic-devel/`   | `gcc`      |
| `glibc-devel/`       | `glibc`    |
| `glibc-locales/`     | `glibc`    |
| `musl-devel/`        | `musl`     |
| `zlib-devel/`        | `zlib`     |
| `libcurl/`           | `curl`     |
| `libcurl-devel/`     | `curl`     |
| `libzstd/`           | `zstd`     |
| `libzstd-devel/`     | `zstd`     |
| `libxbps/`           | `xbps`     |
| `libxbps-devel/`     | `xbps`     |
| `xbps-tests/`        | `xbps`     |
| `jansson-devel/`     | `jansson`  |
| `c-ares-devel/`      | `c-ares`   |
| `nghttp2-devel/`     | `nghttp2`  |
| `libssh2-devel/`     | `libssh2`  |
| `libev-devel/`       | `libev`    |

> **Catatan:** `xbps-triggers` bukan paket tersendiri — lokasinya ada di `srcpkgs/base-files/xbps-triggers/` sebagai subfolder dari `base-files`.

## Script

### Copy srcpkgs (preserves symlinks)

Script ini menyalin **hanya folder yang terdaftar** di `required-srcpkgs.txt` dari void-packages ke direktori Let-X sambil **mempertahankan semua symlink** (tidak di-resolve ke isi folder aslinya).

Letakkan `copy-srcpkgs.sh` dan `required-srcpkgs.txt` dalam satu direktori yang sama.

```sh
$ chmod +x copy-srcpkgs.sh
$ ./copy-srcpkgs.sh
```

**Contoh output:**

```
[?] INDONESIA(1) / ENGLISH(2) : 1

[?] PATH Void-Packages/xbps-src : /home/user/void-packages
[?] PATH Tujuan (Let-X/srcpkgs) : /home/user/Let-X/srcpkgs

[!] Sumber      : /home/user/void-packages/srcpkgs
[!] Tujuan      : /home/user/Let-X/srcpkgs
[!] File List   : /home/user/Let-X/required-srcpkgs.txt

[*] Memproses...

[*] Menyalin: base-files
[*] Menyalin: base-chroot
[*] Menyalin: gcc
[*] Menyalin: libgcc
...

[i] Berhasil disalin : 43 folder
[i] Tidak ditemukan  : 0 folder (di-skip)
[i] Symlink dipertahankan (tidak di-resolve)

[*] Selesai! Disalin ke: /home/user/Let-X/srcpkgs
```

**Dependensi:** `rsync` — install via `sudo xbps-install rsync`

### Menambah folder baru

Edit `required-srcpkgs.txt` — tambahkan nama folder satu per baris. Baris diawali `#` dianggap komentar.

```
# contoh tambahan
openssl
openssl-devel
```

## Notes

- `binary-bootstrap` **tidak** membutuhkan `musl-bootstrap` — paket musl diambil langsung dari binary repo Void, bukan di-build dari source.
- Untuk target musl, jalankan: `./xbps-src -A x86_64-musl binary-bootstrap`
- `nghttp3` dan `libssh` **tidak wajib** — keduanya opsional dan tidak masuk ke dependency chain bootstrap.

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>