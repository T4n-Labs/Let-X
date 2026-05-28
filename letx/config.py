"""
config.py — Global constants for Let-X
"""

from __future__ import annotations
from pathlib import Path

# ─── Package internals ────────────────────────────────────────────
_LETX_PKG_DIR = Path(__file__).parent
BACKEND_DIR   = _LETX_PKG_DIR / "backend"
XBPS_SRC_PATH = BACKEND_DIR / "xbps-src"

# ─── Backend git dir ──────────────────────────────────────────────
BACKEND_GIT_DIR = BACKEND_DIR / "root-git"

# ─── VUR Remote ───────────────────────────────────────────────────
VUR_REPO     = "T4n-Labs/vur"
VUR_BRANCH   = "main"
VUR_RAW_BASE = f"https://raw.githubusercontent.com/{VUR_REPO}/{VUR_BRANCH}"
VUR_API_BASE = f"https://api.github.com/repos/{VUR_REPO}/contents"
VUR_SVN_BASE = f"https://github.com/{VUR_REPO}/trunk"

PACKAGES_URL   = f"{VUR_RAW_BASE}/packages.json"
CATEGORIES_URL = f"{VUR_RAW_BASE}/categories.json"

# ─── Local Paths ──────────────────────────────────────────────────
CONFIG_DIR = Path.home() / ".config" / "letx"
CACHE_DIR  = Path.home() / ".cache"  / "letx"

CATEGORIES: tuple[str, ...] = ("core", "extra", "multilib")

TEMPLATE_DIRS: dict[str, Path] = {
    cat: CONFIG_DIR / cat for cat in CATEGORIES
}

PACKAGES_CACHE   = CACHE_DIR / "packages.json"
CATEGORIES_CACHE = CACHE_DIR / "categories.json"

CACHE_TTL = 3600

# ─── xbps-src workdirs ────────────────────────────────────────────
#
# BACKEND_SRCPKGS_DIR : template internal xbps-src (backend only)
#   Hanya untuk: binary-bootstrap, bootstrap, zap, consistency-check, dll.
#   Berisi: base-files/, base-chroot/
#   TIDAK dipakai untuk build VUR packages.
#
# LETX_MASTERDIR : chroot environment xbps-src
#   Dibuat oleh xbps-src saat `letx -x binary-bootstrap`.
#   Di-pass ke xbps-src via flag -m.
#
# LETX_CHROOT_SRCPKGS : staging area VUR templates di dalam masterdir
#   Path: ~/.config/letx/masterdir/letx-srcpkgs/
#   Di dalam chroot accessible sebagai: /letx-srcpkgs/
#   AMAN — tidak ditimpa oleh bind mount manapun (bukan /void-packages/).
#   Template di-stage dari core/extra/multilib ke sini sebelum build.
#   Source template di core/extra/multilib TIDAK PERNAH dimodifikasi.
#   xbps-src diarahkan ke sini via XBPS_SRCPKGDIR=/letx-srcpkgs/
#   yang ditulis ke masterdir/etc/xbps/xbps-src.conf sebelum setiap build.
#
# LETX_HOSTDIR : output build (.xbps packages, sources, repocache)
#   Di-pass ke xbps-src via flag -H.
#
BACKEND_SRCPKGS_DIR = BACKEND_DIR   / "srcpkgs"
LETX_SRCPKGS_DIR    = CONFIG_DIR    / "srcpkgs"       # legacy, kept for compat
LETX_MASTERDIR      = CONFIG_DIR    / "masterdir"
LETX_CHROOT_SRCPKGS = LETX_MASTERDIR / "letx-srcpkgs" # /letx-srcpkgs/ di chroot
LETX_HOSTDIR        = CONFIG_DIR    / "hostdir"


# ─── Directory setup ──────────────────────────────────────────────

def ensure_dirs() -> None:
    """
    Buat semua direktori Let-X yang dikelola jika belum ada.

    Catatan: LETX_MASTERDIR dan LETX_HOSTDIR TIDAK dibuat di sini —
    xbps-src yang mengelolanya sendiri via `binary-bootstrap`.
    LETX_CHROOT_SRCPKGS juga tidak dibuat di sini — dibuat oleh
    stage_vur_template() saat pertama kali dibutuhkan.
    """
    managed: list[Path] = [
        *TEMPLATE_DIRS.values(),
        LETX_SRCPKGS_DIR,
        CACHE_DIR,
    ]
    for d in managed:
        d.mkdir(parents=True, exist_ok=True)


def ensure_xbps_workdirs() -> None:
    """
    Buat direktori kerja xbps-src jika belum ada.

    LETX_MASTERDIR dikecualikan — xbps-src yang membuatnya saat
    binary-bootstrap.
    """
    LETX_HOSTDIR.mkdir(parents=True, exist_ok=True)
    LETX_MASTERDIR.parent.mkdir(parents=True, exist_ok=True)
