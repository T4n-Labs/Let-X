"""
config.py - Konstanta Global Untuk Let
"""

from pathlib import Path

# -- Remote --
VUR_REPO = "T4n-Labs/vur"
VUR_BRANCH = "main"
VUR_RAW_BASE = f"https://raw.githubusercontent.com/{VUR_REPO}/VUR_BRANCH"
VUR_API_BASE = f"https://api.github.com/repos/{VUR_REPO}/contents"
VUR_SVN_BASE = f"https://github.com/{VUR_REPO}/trunk"
PACKAGES_URL = f"{VUR_RAW_BASE}/packages.json"
CATEGORIES_URL = f"{VUR_RAW_BASE}/categories.json"

# -- Local Path --
CONFIG_DIR = Path.home() / ".config" / "let"
CACHE_DIR = Path.home() / ".cache" / "let"

# PATH Template "let get <package>"
TEMPLATE_DIRS: dict[str, Path] = {
        "core": CONFIG_DIR / "core",
        "extra": CONFIG_DIR / "extra",
        "multilib": CONFIG_DIR / "multilib",
}

# File Cache index
PACKAGES_CACHE   = CACHE_DIR / "packages.json"
CATEGORIES_CACHE = CACHE_DIR / "categories.json"

# TTL Cache Dalam Detik (Default : 1 Jam)
CACHE_TTL = 3600

# -- xbps-src[Backend] --
VOID_PACKAGES_DIR = Path.home() / "void-packages"
XBPS_SRC = VOID_PACKAGES_DIR / "xbps-src"

def ensure_dirs() -> None:
    """Membuat Directory Yang Dibutuhkan Jika Belum ada"""
    for d in [CONFIG_DIR, CACHE_DIR, *TEMPLATE_DIRS.values()] :
        d.mkdir(parents=True, exist_ok=True)
