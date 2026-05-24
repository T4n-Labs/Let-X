"""
config.py — Global constants for Let-X
"""

from __future__ import annotations
from pathlib import Path

# ─── Package internals ────────────────────────────────────────────
# Resolve BACKEND_DIR dari lokasi file ini (__file__) supaya path
# tetap valid baik saat dijalankan dari source maupun setelah
# di-install sebagai wheel ke /usr/lib/letx/
_LETX_PKG_DIR = Path(__file__).parent        # .../letx/
BACKEND_DIR   = _LETX_PKG_DIR / "backend"   # .../letx/backend/
XBPS_SRC_PATH = BACKEND_DIR / "xbps-src"    # .../letx/backend/xbps-src

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

# Template storage directories (hasil `letx get`)
# Struktur: ~/.config/letx/<category>/<pkgname>/template
CATEGORIES: tuple[str, ...] = ("core", "extra", "multilib")

TEMPLATE_DIRS: dict[str, Path] = {
    cat: CONFIG_DIR / cat for cat in CATEGORIES
}

# Cache files
PACKAGES_CACHE   = CACHE_DIR / "packages.json"
CATEGORIES_CACHE = CACHE_DIR / "categories.json"

# Cache TTL in seconds (default: 1 hour)
CACHE_TTL = 3600

# ─── xbps-src workdirs ────────────────────────────────────────────
#
# Opsi A — semua workdir xbps-src di bawah ~/.config/letx/
#
# LETX_SRCPKGS_DIR : symlink bridge yang dikelola utils/xbps.py
#   ~/.config/letx/srcpkgs/<pkgname>  →  ~/.config/letx/<cat>/<pkgname>/
#   Di-set ke xbps-src via env var XBPS_SRCPKGDIR (setelah patch 1 baris)
#
# LETX_MASTERDIR   : chroot environment xbps-src
#   Di-pass ke xbps-src via flag -m
#   Dibuat oleh xbps-src sendiri saat `letx -x binary-bootstrap`
#
# LETX_HOSTDIR     : output build (.xbps packages, sources, repocache)
#   Di-pass ke xbps-src via flag -H
#
LETX_SRCPKGS_DIR = CONFIG_DIR / "srcpkgs"
LETX_MASTERDIR   = CONFIG_DIR / "masterdir"
LETX_HOSTDIR     = CONFIG_DIR / "hostdir"


# ─── Directory setup ──────────────────────────────────────────────

def ensure_dirs() -> None:
    """
    Buat semua direktori Let-X yang dikelola jika belum ada.

    Dipanggil otomatis oleh repo/fetch.py dan repo/index.py sebelum
    operasi baca/tulis apapun.

    Catatan: LETX_MASTERDIR dan LETX_HOSTDIR TIDAK dibuat di sini —
    xbps-src yang mengelolanya sendiri via `binary-bootstrap`.
    Membuatnya prematur bisa mengacaukan pengecekan init chroot xbps-src.
    LETX_SRCPKGS_DIR dibuat di sini karena dibutuhkan saat `letx get`.
    """
    managed: list[Path] = [
        *TEMPLATE_DIRS.values(),  # ~/.config/letx/{core,extra,multilib}/
        LETX_SRCPKGS_DIR,         # ~/.config/letx/srcpkgs/
        CACHE_DIR,                # ~/.cache/letx/
    ]
    for d in managed:
        d.mkdir(parents=True, exist_ok=True)


def ensure_xbps_workdirs() -> None:
    """
    Buat direktori kerja xbps-src jika belum ada.

    Dipisah dari ensure_dirs() karena direktori ini hanya perlu dibuat
    tepat sebelum xbps-src pertama kali dipanggil — bukan di setiap
    command letx. Dipanggil oleh utils/xbps.py.

    LETX_MASTERDIR dikecualikan karena xbps-src yang membuatnya sendiri
    saat binary-bootstrap. Kita hanya perlu pastikan parent-nya ada.
    """
    LETX_HOSTDIR.mkdir(parents=True, exist_ok=True)
    LETX_MASTERDIR.parent.mkdir(parents=True, exist_ok=True)