# Let-X — Prompt Konteks untuk AI Coder

> Paste prompt ini ke system prompt atau awal percakapan sebelum meminta bantuan kode.

---

```
Kamu sedang bekerja pada proyek Let-X — CLI tool Python (VUR Helper untuk Void Linux).
Binary: `letx` | Versi: 0.2.0 | Python 3.11+

## Arsitektur (separation of concerns ketat)
cli.py → ops/ → repo/ → utils/
- cli.py       : argparse saja, tidak ada logika
- ops/         : logika bisnis (search.py, info.py)
- repo/        : akses data (index.py, fetch.py)
- utils/print  : semua output terminal via Rich
- utils/xbps   : SATU-SATUNYA modul yang boleh panggil subprocess xbps-src
- config.py    : semua konstanta/path, hanya boleh import stdlib

## Path Penting (config.py)
BACKEND_DIR          = letx/backend/              # bundle xbps-src
XBPS_SRC_PATH        = letx/backend/xbps-src
BACKEND_GIT_DIR      = letx/backend/root-git/     # .git/ yang di-rename
BACKEND_SRCPKGS_DIR  = letx/backend/srcpkgs/      # base-files, base-chroot SAJA
CONFIG_DIR           = ~/.config/letx/
CACHE_DIR            = ~/.cache/letx/
TEMPLATE_DIRS        = {core|extra|multilib: CONFIG_DIR/<cat>/}
LETX_MASTERDIR       = ~/.config/letx/masterdir/
LETX_CHROOT_SRCPKGS  = ~/.config/letx/masterdir/letx-srcpkgs/
LETX_HOSTDIR         = ~/.config/letx/hostdir/

## Sistem Template VUR
Template disimpan di: ~/.config/letx/{core,extra,multilib}/<pkgname>/template
find_template() loop: core → extra → multilib
Template TIDAK PERNAH dimodifikasi. stage_vur_template() membuat patched copy
di LETX_CHROOT_SRCPKGS/<pkgname>/ sebelum setiap build.

Patch yang diterapkan saat staging:
  Jika ${pkgname}_package() tidak ada → inject `${pkgname}_package() { :; }`
  (xbps-src-doinstall.sh membutuhkan fungsi ini untuk semua package)

## Integrasi xbps-src (utils/xbps.py)
Dua kelompok command:
  CMDS_NEED_PKG → _run_with_template()
    1. find_template()           # loop core/extra/multilib
    2. stage_vur_template()      # copy+patch ke masterdir/letx-srcpkgs/
    3. build_xbps_env()          # set XBPS_CHROOT_CMD=letx
                                 # set XBPS_CHROOT_CMD_ARGS (bind mount)
    4. subprocess: BACKEND_DIR/xbps-src <target> <pkg>

  CMDS_NO_PKG → _run_xbps_raw()
    XBPS_SRCPKGDIR = BACKEND_SRCPKGS_DIR
    subprocess: BACKEND_DIR/xbps-src <target>

## Kritis: letx.sh (custom chroot style)
File: letx/backend/common/chroot-style/letx.sh
KENAPA: uunshare.sh default menaruh EXTRA_ARGS SEBELUM mount DISTDIR.
        Di Linux namespace, mount DISTDIR menimpa submount EXTRA_ARGS.
        letx.sh menaruh DISTDIR dulu, EXTRA_ARGS sesudah → overlay bekerja.
XBPS_CHROOT_CMD=letx mengaktifkannya.
XBPS_CHROOT_CMD_ARGS="-b {LETX_CHROOT_SRCPKGS}:void-packages/srcpkgs"

## Dua Instance xbps-src per Build
Outer (host)  : baca XBPS_SRCPKGDIR dari env → LETX_CHROOT_SRCPKGS
Inner (chroot): env di-clear oleh env -i, baca dari XBPS_DISTDIR
  → XBPS_SRCPKGDIR=/void-packages/srcpkgs/ (default)
  → accessible karena letx.sh bind-mount LETX_CHROOT_SRCPKGS ke sana

## Fix GIT_DIR
root-git/ = .git/ yang di-rename (hindari konflik dengan .git/ proyek Let-X).
build_xbps_env() set GIT_DIR=root-git/ jika ada, jika tidak pop dari env.

## VUR Remote
REPO: T4n-Labs/vur | BRANCH: main
PACKAGES_URL: raw.githubusercontent.com/T4n-Labs/vur/main/packages.json

## Konvensi Kode
- Type hints wajib di semua fungsi publik
- Urutan import: stdlib → third-party → internal (selalu absolute)
- Output: selalu via utils/print.py (tidak boleh print() di ops/ atau repo/)
- Error: return int exit code (0=ok, 1=error), tidak pernah sys.exit() di ops/
- Command baru: subparser di build_parser() + cmd_<nama>() + dispatch di main()

## TODO Diketahui (v0.3.0)
- Cleanup staging setelah build (masterdir/letx-srcpkgs/ terus bertambah)
- letx-bwrap.sh untuk kompatibilitas chroot style bwrap
- Dukungan subpackage ($subpackages) di stage_vur_template()
- Hapus path legacy LETX_SRCPKGS_DIR

## Aturan Sesi Ini
- JANGAN fetch atau baca file kecuali diminta secara eksplisit
- JANGAN reproduksi seluruh file — tampilkan hanya bagian yang berubah
- Jika butuh isi file untuk menjawab, tanya: "Tolong share <file>"
- Anggap arsitektur di atas sudah benar; tanya sebelum mengubah pola
- Gunakan surgical edit (gaya str_replace) bukan rewrite penuh
```