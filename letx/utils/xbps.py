"""
utils/xbps.py — xbps-src wrapper for Let-X

Bertanggung jawab atas:
  1. Mencari template VUR di ~/.config/letx/{core,extra,multilib}/
  2. Staging template ke masterdir/letx-srcpkgs/<pkgname>/ sebelum build
  3. Memanggil backend/xbps-src dengan environment dan flag yang tepat
  4. Meneruskan semua output xbps-src langsung ke terminal (streaming)

Arsitektur srcpkgs:
  BACKEND_SRCPKGS_DIR  → backend only (base-files, base-chroot)
                          Dipakai: binary-bootstrap, zap, bootstrap, dll.

  LETX_CHROOT_SRCPKGS  → VUR templates staging (masterdir/letx-srcpkgs/)
                          Accessible di chroot sebagai /letx-srcpkgs/
                          xbps-src diarahkan ke sini via XBPS_SRCPKGDIR.
                          Template SOURCE tetap di core/extra/multilib.

VUR template flow untuk CMDS_NEED_PKG:
  ~/.config/letx/extra/zig/    ← SOURCE (tidak pernah diubah)
           ↓ stage_vur_template()
  masterdir/letx-srcpkgs/zig/  ← BUILD STAGE (patched copy)
           ↓ xbps-src baca dari sini (XBPS_SRCPKGDIR=/letx-srcpkgs/)
  build ✓
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from letx.config import (
    BACKEND_DIR,
    BACKEND_GIT_DIR,
    BACKEND_SRCPKGS_DIR,
    CATEGORIES,
    LETX_CHROOT_SRCPKGS,
    LETX_HOSTDIR,
    LETX_MASTERDIR,
    LETX_SRCPKGS_DIR,
    TEMPLATE_DIRS,
    XBPS_SRC_PATH,
    ensure_xbps_workdirs,
)

# ─── Klasifikasi command xbps-src ────────────────────────────────

# Command yang wajib diikuti <pkgname>
# Template VUR di-stage ke LETX_CHROOT_SRCPKGS
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

# Command yang TIDAK butuh pkgname — pakai BACKEND_SRCPKGS_DIR
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
    "show-var",
    "show-repo-updates",
    "show-sys-updates",
    "show-local-updates",
    "sort-dependencies",
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
    Cari template VUR di tiga kategori.

    Loop: core → extra → multilib
    Return (category, pkg_dir) jika ditemukan, None jika tidak.
    """
    for cat in CATEGORIES:
        pkg_dir = TEMPLATE_DIRS[cat] / pkgname
        if (pkg_dir / "template").is_file():
            return cat, pkg_dir
    return None


# ─── Template staging ────────────────────────────────────────────

def stage_vur_template(pkgname: str, pkg_dir: Path) -> Path:
    """
    Stage template VUR ke masterdir/letx-srcpkgs/<pkgname>/.

    Template SOURCE di core/extra/multilib TIDAK PERNAH dimodifikasi.
    Staging membuat copy di LETX_CHROOT_SRCPKGS dengan patch berikut:
      - Inject ${pkgname}_package() { :; } jika belum ada.
        xbps-src-doinstall.sh membutuhkan fungsi ini untuk semua package.
    File pendukung (patches/, files/, dll) juga di-copy.

    Di dalam chroot, staging area accessible sebagai /letx-srcpkgs/<pkgname>/.
    xbps-src membaca template dari sana via XBPS_SRCPKGDIR=/letx-srcpkgs/.

    Args:
        pkgname : nama package, contoh 'zig'
        pkg_dir : direktori template source, contoh ~/.config/letx/extra/zig/

    Returns:
        Path staging directory (LETX_CHROOT_SRCPKGS / pkgname)
    """
    staged_dir = LETX_CHROOT_SRCPKGS / pkgname
    if staged_dir.exists():
        shutil.rmtree(staged_dir)
    staged_dir.mkdir(parents=True, exist_ok=True)

    # Baca template source
    template_src = pkg_dir / "template"
    content = template_src.read_text(encoding="utf-8")

    # Inject ${pkgname}_package() jika belum ada
    func_name = f"{pkgname}_package"
    if f"{func_name}()" not in content:
        content += (
            "\n"
            "# Auto-injected by Let-X\n"
            f"# VUR templates tidak wajib mendefinisikan {func_name}().\n"
            f"{func_name}() {{ :; }}\n"
        )

    # Tulis template yang sudah di-patch ke staging
    (staged_dir / "template").write_text(content, encoding="utf-8")

    # Copy file pendukung: patches/, files/, subpkg, dll
    for item in pkg_dir.iterdir():
        if item.name == "template":
            continue
        dest = staged_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    return staged_dir


# ─── Environment setup ───────────────────────────────────────────

def build_xbps_env(*, use_backend_srcpkgs: bool = False) -> dict[str, str]:
    """
    Bangun environment variables untuk subprocess xbps-src.

    use_backend_srcpkgs=True  → CMDS_NO_PKG (binary-bootstrap, zap, dll)
    use_backend_srcpkgs=False → CMDS_NEED_PKG (VUR builds)
    """
    env = os.environ.copy()

    # GIT_DIR fix: root-git/ adalah .git/ yang di-rename
    if BACKEND_GIT_DIR.is_dir():
        env["GIT_DIR"]       = str(BACKEND_GIT_DIR)
        env["GIT_WORK_TREE"] = str(BACKEND_DIR)
    else:
        env.pop("GIT_DIR",       None)
        env.pop("GIT_WORK_TREE", None)

    if use_backend_srcpkgs:
        # CMDS_NO_PKG: pakai backend srcpkgs (base-files, base-chroot)
        env["XBPS_SRCPKGDIR"] = str(BACKEND_SRCPKGS_DIR)
        env["XBPS_COMMONDIR"] = str(BACKEND_DIR / "common")
    else:
        # CMDS_NEED_PKG: arahkan outer xbps-src ke LETX_CHROOT_SRCPKGS.
        #
        # Ada dua instance xbps-src yang perlu tahu lokasi template:
        #
        # 1. Outer xbps-src (host, sebelum chroot):
        #    Baca XBPS_SRCPKGDIR dari env var. Di-set ke LETX_CHROOT_SRCPKGS
        #    (path absolut di host: masterdir/letx-srcpkgs/) supaya
        #    setup_pkg() bisa source template sebelum masuk chroot.
        #
        # 2. Inner xbps-src (di dalam chroot):
        #    Env di-clear oleh `env -i` di chroot_handler. Baca dari
        #    masterdir/etc/xbps/xbps-src.conf yang sudah di-set ke
        env["XBPS_SRCPKGDIR"] = str(LETX_CHROOT_SRCPKGS)
        env.pop("XBPS_COMMONDIR", None)

    return env


# ─── Core runner ─────────────────────────────────────────────────

def run(args: list[str]) -> int:
    """Entry point utama yang dipanggil oleh cli.py."""
    if not args:
        return _run_xbps_raw([])

    target, pkgname, xbps_options = _parse_args(args)

    if target is None:
        return _run_xbps_raw(args)

    if target not in ALL_CMDS:
        _print_error(
            f"Unknown xbps-src target: '{target}'\n"
            f"Run 'letx -x -h' to see available targets."
        )
        return 1

    if target in CMDS_NEED_PKG:
        if not pkgname:
            _print_error(
                f"Target '{target}' requires a package name.\n"
                f"Usage: letx -x {target} <pkgname>"
            )
            return 1
        return _run_with_template(target, pkgname, xbps_options)

    return _run_xbps_raw(args, use_backend_srcpkgs=True)


# ─── Internal helpers ────────────────────────────────────────────

def _parse_args(
    args: list[str],
) -> tuple[str | None, str | None, list[str]]:
    """Identifikasi target, pkgname, dan xbps-options dari args."""
    target: str | None = None
    pkgname: str | None = None
    xbps_options: list[str] = []
    positionals: list[str] = []

    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith("-"):
            xbps_options.append(arg)
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
    Jalankan xbps-src untuk CMDS_NEED_PKG dengan VUR template.

    Alur:
      1. Cari template di VUR: loop core → extra → multilib
      2. Stage template ke masterdir/letx-srcpkgs/<pkgname>/
         (copy + inject _package() jika perlu)
      3. Set XBPS_SRCPKGDIR=/letx-srcpkgs/ di chroot conf
      4. Pastikan workdirs ada
      5. Jalankan xbps-src
    """
    # 1. Cari template di VUR: core → extra → multilib
    result = find_template(pkgname)
    if result is None:
        searched = ", ".join(
            str(TEMPLATE_DIRS[c] / pkgname) for c in CATEGORIES
        )
        _print_error(
            f"Package '{pkgname}' not found in any VUR category.\n"
            f"Searched: {searched}\n"
            f"Run 'letx get {pkgname}' to download the template first."
        )
        return 1

    cat, pkg_dir = result

    # 2. Stage template ke masterdir/letx-srcpkgs/<pkgname>/
    #    Source di core/extra/multilib tidak dimodifikasi.
    stage_vur_template(pkgname, pkg_dir)

    # 3. Pastikan workdirs ada
    ensure_xbps_workdirs()

    # Buat mount point untuk bind-mount staging VUR ke dalam chroot.
    # uunshare resolve dest path di host filesystem (bukan namespace),
    # sehingga masterdir/void-packages/srcpkgs/ harus exist secara fisik
    # sebelum uunshare bisa bind-mount staging area ke sana.
    vur_mount_point = LETX_MASTERDIR / "void-packages" / "srcpkgs"
    vur_mount_point.mkdir(parents=True, exist_ok=True)

    # 4. Build environment + inject staging area ke chroot.
    #
    #    Inner xbps-src (IN_CHROOT=1) selalu set:
    #      XBPS_DISTDIR=/void-packages/  (dari lokasi script $0)
    #      XBPS_SRCPKGDIR=/void-packages/srcpkgs/  (default dari XBPS_DISTDIR)
    #    Conf file override tidak efektif karena xbps-src overwrite setelahnya.
    #
    #    Solusi: bind-mount LETX_CHROOT_SRCPKGS ke /void-packages/srcpkgs/
    #    via uunshare flag -b <src:dest> (dest relatif ke masterdir).
    #    uunshare apply extra mounts SETELAH BACKEND_DIR di-mount ke
    #    /void-packages/, sehingga mount point void-packages/srcpkgs/ sudah
    #    ada di namespace dan bind-mount bisa dilakukan.
    #
    #    Hasilnya di dalam chroot:
    #      /void-packages/srcpkgs/ = LETX_CHROOT_SRCPKGS (staging VUR) ✓
    #      /void-packages/srcpkgs/zig/template              accessible ✓
    env = build_xbps_env(use_backend_srcpkgs=False)

    # Gunakan custom chroot style letx.sh (bukan uunshare.sh default).
    # letx.sh menaruh EXTRA_ARGS SETELAH DISTDIR mount sehingga
    # bind mount VUR srcpkgs tidak tertimpa oleh DISTDIR mount.
    # Script ada di BACKEND_DIR/common/chroot-style/letx.sh.
    env["XBPS_CHROOT_CMD"] = "letx"

    # Bind mount LETX_CHROOT_SRCPKGS ke /void-packages/srcpkgs/ di chroot.
    # Format uunshare: -b <src>:<dest> (dest relatif ke masterdir).
    # Karena letx.sh menaruh ini SETELAH DISTDIR mount, overlay bekerja:
    #   /void-packages/srcpkgs/ ← LETX_CHROOT_SRCPKGS (staging VUR) ✓
    env["XBPS_CHROOT_CMD_ARGS"] = (
        f"-b {LETX_CHROOT_SRCPKGS}:void-packages/srcpkgs"
    )

    # 5. Jalankan xbps-src
    cmd = [
        str(XBPS_SRC_PATH),
        "-m", str(LETX_MASTERDIR),
        "-H", str(LETX_HOSTDIR),
        *xbps_options,
        target,
        pkgname,
    ]

    try:
        proc = subprocess.run(cmd, env=env, cwd=str(BACKEND_DIR))
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


def _run_xbps_raw(
    args: list[str],
    *,
    use_backend_srcpkgs: bool = False,
) -> int:
    """
    Forward args langsung ke xbps-src tanpa preprocessing.

    Untuk CMDS_NO_PKG: restore XBPS_SRCPKGDIR ke default backend
    supaya tidak terpengaruh oleh VUR build sebelumnya.
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

    if args and args[0] == "binary-bootstrap":
        ensure_xbps_workdirs()

    try:
        proc = subprocess.run(cmd, env=env, cwd=str(BACKEND_DIR))
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
    print(f"[ERROR] {msg}", file=sys.stderr)
