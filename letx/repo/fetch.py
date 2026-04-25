"""
repo/fetch.py — Download folder template package dari VUR ke lokal
Strategi: GitHub Contents API (tidak butuh git/svn)
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Callable

import httpx

from letx.config import VUR_API_BASE, VUR_RAW_BASE, TEMPLATE_DIRS, ensure_dirs


# ─── Public ───────────────────────────────────────────────

def download_package(
    pkg_path: str,
    category: str,
    pkg_name: str,
    progress_cb: Callable[[str], None] | None = None,
) -> Path:
    """
    Download seluruh folder package dari VUR ke direktori lokal.

    Args:
        pkg_path:    path di repo, misal "extra/discord"
        category:    "core" | "extra" | "multilib"
        pkg_name:    nama package, misal "discord"
        progress_cb: opsional callback(pesan) untuk progress

    Returns:
        Path direktori lokal tempat template disimpan

    Raises:
        httpx.HTTPError: Jika gagal fetch dari GitHub
        ValueError: Jika category tidak dikenal
    """
    if category not in TEMPLATE_DIRS:
        raise ValueError(f"Category tidak dikenal: '{category}'")

    ensure_dirs()
    dest = TEMPLATE_DIRS[category] / pkg_name

    # Bersihkan dulu jika sudah ada (update)
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    _fetch_dir(pkg_path, dest, progress_cb)
    return dest


def package_exists_locally(category: str, pkg_name: str) -> bool:
    """Cek apakah template package sudah ada di lokal."""
    if category not in TEMPLATE_DIRS:
        return False
    dest = TEMPLATE_DIRS[category] / pkg_name
    return dest.exists() and any(dest.iterdir())


def local_package_path(category: str, pkg_name: str) -> Path | None:
    """Return path lokal package jika ada, None jika tidak."""
    if category not in TEMPLATE_DIRS:
        return None
    dest = TEMPLATE_DIRS[category] / pkg_name
    return dest if dest.exists() else None


# ─── Internal ─────────────────────────────────────────────

def _fetch_dir(
    api_path: str,
    local_dir: Path,
    progress_cb: Callable[[str], None] | None,
    _client: httpx.Client | None = None,
) -> None:
    """Rekursif fetch semua file dalam satu direktori via GitHub API."""
    own_client = _client is None
    client = _client or httpx.Client(timeout=15, follow_redirects=True)

    try:
        resp = client.get(f"{VUR_API_BASE}/{api_path}")
        resp.raise_for_status()
        items: list[dict] = resp.json()

        for item in items:
            if item["type"] == "file":
                _fetch_file(item["path"], local_dir / item["name"], client, progress_cb)
            elif item["type"] == "dir":
                sub_dir = local_dir / item["name"]
                sub_dir.mkdir(exist_ok=True)
                _fetch_dir(item["path"], sub_dir, progress_cb, _client=client)
    finally:
        if own_client:
            client.close()


def _fetch_file(
    repo_path: str,
    local_path: Path,
    client: httpx.Client,
    progress_cb: Callable[[str], None] | None,
) -> None:
    """Download satu file dari raw GitHub."""
    if progress_cb:
        progress_cb(f"  ↓ {repo_path}")

    url = f"{VUR_RAW_BASE}/{repo_path}"
    resp = client.get(url)
    resp.raise_for_status()
    local_path.write_bytes(resp.content)
