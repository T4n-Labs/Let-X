"""
repo/fetch.py — Download package template folder from VUR to local storage
Strategy: GitHub Contents API (no git or svn required)
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
    Download the full package folder from VUR to local storage.

    Args:
        pkg_path:    path in the repo, e.g. "extra/discord"
        category:    "core" | "extra" | "multilib"
        pkg_name:    package name, e.g. "discord"
        progress_cb: optional callback(message) for download progress

    Returns:
        Local directory path where the template was saved

    Raises:
        httpx.HTTPError: If the GitHub request fails
        ValueError: If the category is not recognized
    """
    if category not in TEMPLATE_DIRS:
        raise ValueError(f"Unknown category: '{category}'")

    ensure_dirs()
    dest = TEMPLATE_DIRS[category] / pkg_name

    # Clean up existing copy (for re-downloads)
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    _fetch_dir(pkg_path, dest, progress_cb)
    return dest


def package_exists_locally(category: str, pkg_name: str) -> bool:
    """Check whether a package template already exists locally."""
    if category not in TEMPLATE_DIRS:
        return False
    dest = TEMPLATE_DIRS[category] / pkg_name
    return dest.exists() and any(dest.iterdir())


def local_package_path(category: str, pkg_name: str) -> Path | None:
    """Return the local path for a package, or None if not found."""
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
    """Recursively fetch all files in a directory via GitHub API."""
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
    """Download a single file from raw GitHub."""
    if progress_cb:
        progress_cb(f"  ↓ {repo_path}")

    url = f"{VUR_RAW_BASE}/{repo_path}"
    resp = client.get(url)
    resp.raise_for_status()
    local_path.write_bytes(resp.content)
