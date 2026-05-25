"""
utils/xbps.py — xbps-src wrapper for Let-X

Bertanggung jawab atas:
  1. Mencari template package di ~/.config/letx/{core,extra,multilib}/
  2. Membuat symlink bridge ~/.config/letx/srcpkgs/<pkg> → <cat>/<pkg>/
  3. Memanggil backend/xbps-src dengan environment dan flag yang tepat
  4. Meneruskan semua output xbps-src langsung ke terminal (streaming)

Yang TIDAK dikerjakan di sini:
  - Build logic (itu urusan xbps-src)
  - Parsing output xbps-src
  - Format/styling output (itu urusan utils/print.py)

XBPS_SRCPKGDIR routing:
  CMDS_NO_PKG  → BACKEND_SRCPKGS_DIR  (bundled: base-files/, base-chroot/)
  CMDS_NEED_PKG → LETX_SRCPKGS_DIR    (user VUR symlink bridge)
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from letx.config import (
    BACKEND_DIR,
    BACKEND_GIT_DIR,
    BACKEND_SRCPKGS_DIR,
    CATEGORIES,
    LETX_HOSTDIR,
    LETX_MASTERDIR,
    LETX_SRCPKGS_DIR,
    TEMPLATE_DIRS,
    XBPS_SRC_PATH,
    ensure_xbps_workdirs,
)

# ─── Klasifikasi command xbps-src ────────────────────────────────
#
# Dipakai untuk:
#   (a) Validasi argumen sebelum panggil xbps-src
#   (b) Routing XBPS_SRCPKGDIR yang tepat:
#       CMDS_NEED_PKG → LETX_SRCPKGS_DIR    (VUR user templates)
#       CMDS_NO_PKG   → BACKEND_SRCPKGS_DIR  (bundled internal templates)
#
# Sumber: letx-xbps.md + analisis langsung xbps-src (1095 baris)

# Command yang wajib diikuti <pkgname>
# XBPS_SRCPKGDIR → ~/.config/letx/srcpkgs/ (VUR symlink bridge)
CMDS_NEED_PKG: frozenset[str] = frozenset({
    "fetch",
    "extract",
    "patch",
    "configure",
    "build",
    "check",
    "install",
    "pkg",
    "clean",
    "remove",
    "show",
    "show-avail",
    "show-build-deps",
    "show-check-deps",
    "show-deps",
    "show-files",
    "show-hostmakedepends",
    "show-makedepends",
    "show-options",
    "show-shlib-provides",
    "show-shlib-requires",
    "update-check",
})

# Command yang TIDAK butuh pkgname
# XBPS_SRCPKGDIR → backend/srcpkgs/ (bundled: base-files, base-chroot)
CMDS_NO_PKG: frozenset[str] = frozenset({
    "binary-bootstrap",
    "bootstrap",
    "bootstrap-update",
    "consistency-check",
    "chroot",
    "clean-repocache",
    "list",
    "remove-autodeps",
    "purge-distfiles",
    "show-var",           # butuh <var>, bukan pkgname
    "show-repo-updates",
    "show-sys-updates",
    "show-local-updates",
    "sort-dependencies",  # butuh <pkg> <pkg2> ..., tidak perlu symlink
    "update-bulk",
    "update-sys",
    "update-local",
    "update-hash-cache",
    "zap",
})

ALL_CMDS: frozenset[str] = CMDS_NEED_PKG | CMDS_NO_PKG


# ─── Template resolution ─────────────────────────────────────────

def find_template(pkgname: str) -> tuple[str, Path] | None:
    """
    Cari template package di ketiga kategori VUR.

    Urutan pencarian: core → extra → multilib
    (core diprioritaskan karena package sistem biasanya ada di sana)

    Returns:
        (category, pkg_dir) jika ditemukan, None jika tidak.
        pkg_dir adalah direktori yang berisi file 'template',
        contoh: ~/.config/letx/extra/discord/
    """
    for cat in CATEGORIES:
        pkg_dir = TEMPLATE_DIRS[cat] / pkgname
        template_file = pkg_dir / "template"
        if template_file.is_file():
            return cat, pkg_dir
    return None


# ─── Symlink bridge ──────────────────────────────────────────────

def setup_srcpkg_symlink(pkgname: str, pkg_dir: Path) -> Path:
    """
    Buat symlink ~/.config/letx/srcpkgs/<pkgname> → <pkg_dir>

    xbps-src mencari template di $XBPS_SRCPKGDIR/<pkgname>/template.
    Kita set XBPS_SRCPKGDIR=~/.config/letx/srcpkgs/ untuk CMDS_NEED_PKG,
    jadi symlink ini yang menjembatani struktur kategori Let-X dan
    ekspektasi xbps-src.

    Symlink lama dihapus dulu kalau sudah ada (staleness protection).

    Returns:
        Path symlink yang dibuat.
    """
    LETX_SRCPKGS_DIR.mkdir(parents=True, exist_ok=True)
    symlink = LETX_SRCPKGS_DIR / pkgname

    if symlink.is_symlink() or symlink.exists():
        symlink.unlink()

    symlink.symlink_to(pkg_dir.resolve())
    return symlink


def cleanup_srcpkg_symlink(pkgname: str) -> None:
    """
    Hapus symlink setelah xbps-src selesai (opsional cleanup).

    Tidak di-raise jika symlink tidak ada — cleanup bersifat best-effort.
    """
    symlink = LETX_SRCPKGS_DIR / pkgname
    try:
        if symlink.is_symlink():
            symlink.unlink()
    except OSError:
        pass


# ─── Environment setup ───────────────────────────────────────────

def build_xbps_env(*, use_backend_srcpkgs: bool = False) -> dict[str, str]:
    """
    Bangun environment variables untuk subprocess xbps-src.

    Args:
        use_backend_srcpkgs:
            True  → XBPS_SRCPKGDIR = backend/srcpkgs/ (bundled)
                    Dipakai oleh CMDS_NO_PKG:
                    binary-bootstrap, bootstrap, consistency-check, dll.
                    xbps-src butuh base-files/ dan base-chroot/ dari sini.
            False → XBPS_SRCPKGDIR = ~/.config/letx/srcpkgs/ (VUR)
                    Dipakai oleh CMDS_NEED_PKG:
                    pkg, build, fetch, install, dll.

    GIT_DIR:
        xbps-src memanggil `git symbolic-ref` untuk detect branch info.
        Direktori .git/ sudah diganti nama menjadi root-git/ agar tidak
        bentrok dengan .git/ proyek Let-X. GIT_DIR di-set eksplisit ke
        backend/root-git/ supaya git tetap bisa menemukan repo-nya.
        Fix untuk: "fatal: not a git repository"

    GIT_WORK_TREE:
        Di-set ke BACKEND_DIR supaya git tahu working tree-nya.

    Catatan: XBPS_MASTERDIR dan XBPS_HOSTDIR di-pass via flag -m dan -H,
    bukan env var, karena xbps-src memprioritaskan flag di atas env var
    untuk kedua variabel tersebut (lihat xbps-src line 547-553).
    """
    env = os.environ.copy()

    # Routing XBPS_SRCPKGDIR berdasarkan jenis command
    if use_backend_srcpkgs:
        env["XBPS_SRCPKGDIR"] = str(BACKEND_SRCPKGS_DIR)
    else:
        env["XBPS_SRCPKGDIR"] = str(LETX_SRCPKGS_DIR)

    # Fix "missing <lang>_package() function" — xbps-src mencari
    # common/build-style/, common/hooks/, dll relatif terhadap
    # XBPS_COMMONDIR. Kalau tidak di-set eksplisit, xbps-src default
    # ke <XBPS_SRCPKGDIR>/../common/ — yang valid saat SRCPKGDIR=backend/srcpkgs/,
    # tapi SALAH saat SRCPKGDIR=~/.config/letx/srcpkgs/ (VUR mode).
    # Di-set eksplisit ke backend/common/ agar selalu tepat di kedua mode.
    env["XBPS_COMMONDIR"] = str(BACKEND_DIR / "common")

    # Fix "fatal: not a git repository"
    # root-git/ adalah .git/ yang di-rename agar tidak bentrok dengan
    # .git/ proyek Let-X. Tapi saat di-install sebagai wheel ke
    # /usr/lib/python3.x/site-packages/, folder root-git/ TIDAK ikut
    # ter-package (git dirs di-exclude dari wheel secara default).
    #
    # Strategi:
    #   - Jika root-git/ ada (dev mode / editable install): set GIT_DIR
    #     supaya git tahu repo-nya.
    #   - Jika tidak ada (wheel install): UNSET GIT_DIR dari env yang
    #     di-inherit user. xbps-src tetap memanggil git, tapi output
    #     "fatal: not a git repository" akan muncul sebagai warning
    #     non-fatal — build tetap jalan. Dengan unset, kita cegah
    #     git salah baca GIT_DIR dari env user yang kebetulan ter-set.
    if BACKEND_GIT_DIR.is_dir():
        env["GIT_DIR"]       = str(BACKEND_GIT_DIR)
        env["GIT_WORK_TREE"] = str(BACKEND_DIR)
    else:
        env.pop("GIT_DIR",       None)
        env.pop("GIT_WORK_TREE", None)

    return env


# ─── Core runner ─────────────────────────────────────────────────

def run(args: list[str]) -> int:
    """
    Entry point utama yang dipanggil oleh cli.py.

    args: semua argumen setelah `letx -x`, contoh:
        ["pkg", "discord"]
        ["-j4", "pkg", "discord", "-G"]
        ["binary-bootstrap"]
        ["-h"]
        ["-A", "aarch64", "pkg", "neovim"]

    Returns:
        Exit code dari xbps-src (0 = sukses).
    """
    if not args:
        return _run_xbps_raw([])

    # Pisahkan options xbps-src (dimulai dengan -) dari target dan pkgname.
    # xbps-src sendiri yang parse options via getopt, jadi kita tidak perlu
    # parse detail — cukup identifikasi target (non-option pertama) dan pkgname.
    target, pkgname, xbps_options = _parse_args(args)

    # Jika tidak ada target (misal hanya -h atau -V), langsung forward
    if target is None:
        return _run_xbps_raw(args)

    # Validasi: target dikenal?
    if target not in ALL_CMDS:
        _print_error(
            f"Unknown xbps-src target: '{target}'\n"
            f"Run 'letx -x -h' to see available targets."
        )
        return 1

    # Command yang butuh pkgname: cari template VUR, setup symlink
    if target in CMDS_NEED_PKG:
        if not pkgname:
            _print_error(
                f"Target '{target}' requires a package name.\n"
                f"Usage: letx -x {target} <pkgname>"
            )
            return 1
        return _run_with_template(target, pkgname, xbps_options)

    # Command yang tidak butuh pkgname: pakai backend/srcpkgs/
    return _run_xbps_raw(args, use_backend_srcpkgs=True)


# ─── Internal helpers ────────────────────────────────────────────

def _parse_args(
    args: list[str],
) -> tuple[str | None, str | None, list[str]]:
    """
    Identifikasi target, pkgname, dan xbps-options dari args.

    xbps-src memproses options via getopt sebelum target, jadi
    format valid adalah:
        [options...] <target> [pkgname] [options...]

    Returns:
        (target, pkgname, xbps_options_list)
        target dan pkgname bisa None jika tidak ditemukan.
    """
    target: str | None = None
    pkgname: str | None = None
    xbps_options: list[str] = []
    positionals: list[str] = []

    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith("-"):
            xbps_options.append(arg)
            # Beberapa options xbps-src butuh argument: -A -a -c -H -j -m -o -p -r
            if arg in ("-A", "-a", "-c", "-H", "-j", "-m", "-o", "-p", "-r") \
                    and i + 1 < len(args):
                i += 1
                xbps_options.append(args[i])
        else:
            positionals.append(arg)
        i += 1

    if positionals:
        target = positionals[0]
    if len(positionals) >= 2:
        pkgname = positionals[1]

    return target, pkgname, xbps_options


def _run_with_template(
    target: str,
    pkgname: str,
    xbps_options: list[str],
) -> int:
    """
    Jalankan xbps-src untuk command yang butuh pkgname (CMDS_NEED_PKG).

    XBPS_SRCPKGDIR → ~/.config/letx/srcpkgs/ (VUR symlink bridge)

    Alur:
      1. Cari template di {core,extra,multilib}
      2. Buat symlink bridge di ~/.config/letx/srcpkgs/
      3. Pastikan workdirs xbps-src ada
      4. Jalankan xbps-src dengan env VUR + flag yang tepat
      5. Cleanup symlink (best-effort)
    """
    # 1. Cari template
    result = find_template(pkgname)
    if result is None:
        _print_error(
            f"Package '{pkgname}' not found in any category.\n"
            "Searched: " + ", ".join(
                str(TEMPLATE_DIRS[c] / pkgname) for c in CATEGORIES
            ) + "\n"
            f"Run 'letx get {pkgname}' to download the template first."
        )
        return 1

    cat, pkg_dir = result

    # 2. Setup symlink bridge
    setup_srcpkg_symlink(pkgname, pkg_dir)

    # 3. Pastikan workdirs ada
    ensure_xbps_workdirs()

    # 4. Bangun command xbps-src
    #    Flag -m dan -H di-inject otomatis, tapi bisa di-override user
    #    via xbps_options (xbps-src ambil yang terakhir kalau duplikat)
    cmd = [
        str(XBPS_SRC_PATH),
        "-m", str(LETX_MASTERDIR),
        "-H", str(LETX_HOSTDIR),
        *xbps_options,
        target,
        pkgname,
    ]

    # XBPS_SRCPKGDIR → ~/.config/letx/srcpkgs/ (VUR)
    env = build_xbps_env(use_backend_srcpkgs=False)

    try:
        proc = subprocess.run(
            cmd,
            env=env,
            cwd=str(BACKEND_DIR),
        )
        return proc.returncode
    except FileNotFoundError:
        _print_error(
            f"xbps-src not found at: {XBPS_SRC_PATH}\n"
            "Make sure Let-X is properly installed."
        )
        return 127
    except KeyboardInterrupt:
        print("\n[INTERRUPTED] xbps-src build interrupted by user.", file=sys.stderr)
        return 130
    finally:
        # 5. Cleanup symlink (best-effort, tidak raise)
        cleanup_srcpkg_symlink(pkgname)


def _run_xbps_raw(
    args: list[str],
    *,
    use_backend_srcpkgs: bool = False,
) -> int:
    """
    Forward args langsung ke xbps-src tanpa preprocessing.

    Dipakai untuk:
    - CMDS_NO_PKG: binary-bootstrap, bootstrap, consistency-check, dll
      → use_backend_srcpkgs=True (backend/srcpkgs/ bundled)
    - Flag-only invocation: -h, -V
      → use_backend_srcpkgs=False (default, tidak relevan)

    Flag -m dan -H di-inject otomatis kecuali user sudah set sendiri.
    """
    has_m = "-m" in args
    has_H = "-H" in args

    injected: list[str] = []
    if not has_m:
        injected += ["-m", str(LETX_MASTERDIR)]
    if not has_H:
        injected += ["-H", str(LETX_HOSTDIR)]

    cmd = [str(XBPS_SRC_PATH), *injected, *args]
    env = build_xbps_env(use_backend_srcpkgs=use_backend_srcpkgs)

    # Untuk binary-bootstrap, pastikan parent masterdir ada
    if args and args[0] == "binary-bootstrap":
        ensure_xbps_workdirs()

    try:
        proc = subprocess.run(
            cmd,
            env=env,
            cwd=str(BACKEND_DIR),
        )
        return proc.returncode
    except FileNotFoundError:
        _print_error(
            f"xbps-src not found at: {XBPS_SRC_PATH}\n"
            "Make sure Let-X is properly installed."
        )
        return 127
    except KeyboardInterrupt:
        print("\n[INTERRUPTED] xbps-src interrupted by user.", file=sys.stderr)
        return 130


def _print_error(msg: str) -> None:
    """Print error ke stderr dengan prefix [ERROR] konsisten dengan Let-X style."""
    print(f"[ERROR] {msg}", file=sys.stderr)