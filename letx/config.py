"""
config.py — Konstanta global untuk Let-X
"""

from pathlib import Path

# ─── Remote ───────────────────────────────────────────────
VUR_REPO     = "T4n-Labs/vur"
VUR_BRANCH   = "main"
VUR_RAW_BASE = f"https://raw.githubusercontent.com/{VUR_REPO}/{VUR_BRANCH}"
VUR_API_BASE = f"https://api.github.com/repos/{VUR_REPO}/contents"
VUR_SVN_BASE = f"https://github.com/{VUR_REPO}/trunk"

PACKAGES_URL   = f"{VUR_RAW_BASE}/packages.json"
CATEGORIES_URL = f"{VUR_RAW_BASE}/categories.json"

# ─── Local Paths ──────────────────────────────────────────
CONFIG_DIR = Path.home() / ".config" / "letx"
CACHE_DIR  = Path.home() / ".cache"  / "letx"

# Tempat template disimpan setelah `letx get`
TEMPLATE_DIRS: dict[str, Path] = {
    "core":     CONFIG_DIR / "core",
    "extra":    CONFIG_DIR / "extra",
    "multilib": CONFIG_DIR / "multilib",
}

# File cache index
PACKAGES_CACHE   = CACHE_DIR / "packages.json"
CATEGORIES_CACHE = CACHE_DIR / "categories.json"

# TTL cache dalam detik (default: 1 jam)
CACHE_TTL = 3600

# ─── xbps-src (untuk fase berikutnya) ─────────────────────
VOID_PACKAGES_DIR = Path.home() / "void-packages"
XBPS_SRC          = VOID_PACKAGES_DIR / "xbps-src"


def ensure_dirs() -> None:
    """Buat semua direktori yang dibutuhkan jika belum ada."""
    for d in [CONFIG_DIR, CACHE_DIR, *TEMPLATE_DIRS.values()]:
        d.mkdir(parents=True, exist_ok=True)
