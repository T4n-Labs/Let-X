"""
repo/index.py — Fetch and cache packages.json from VUR
"""

import json
import time
from typing import Any

import httpx

from letx.config import (
    PACKAGES_URL,
    PACKAGES_CACHE,
    CACHE_TTL,
    ensure_dirs,
)

Package = dict[str, Any]


def _cache_valid() -> bool:
    """Check whether the local cache is still fresh (within TTL)."""
    if not PACKAGES_CACHE.exists():
        return False
    age = time.time() - PACKAGES_CACHE.stat().st_mtime
    return age < CACHE_TTL


def _write_cache(data: list[Package]) -> None:
    ensure_dirs()
    PACKAGES_CACHE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _read_cache() -> list[Package]:
    return json.loads(PACKAGES_CACHE.read_text(encoding="utf-8"))


def fetch_index(force: bool = False) -> list[Package]:
    """
    Fetch the VUR package index.
    - Uses local cache if still valid and force=False
    - Fetches from GitHub if cache is expired or force=True

    Returns:
        List of package dicts from packages.json

    Raises:
        RuntimeError: If fetch fails and no local cache exists
    """
    if not force and _cache_valid():
        return _read_cache()

    try:
        resp = httpx.get(PACKAGES_URL, timeout=10, follow_redirects=True)
        resp.raise_for_status()
        data: list[Package] = resp.json()
        _write_cache(data)
        return data

    except httpx.HTTPError as e:
        if PACKAGES_CACHE.exists():
            return _read_cache()
        raise RuntimeError(
            f"Failed to fetch index from GitHub and no local cache found.\n"
            f"Error: {e}"
        ) from e


def get_package(name: str, force: bool = False) -> Package | None:
    """Find a single package by exact name (case-insensitive)."""
    index = fetch_index(force=force)
    name_lower = name.lower()
    for pkg in index:
        if pkg["name"].lower() == name_lower:
            return pkg
    return None


def cache_info() -> dict[str, Any]:
    """Return current cache status information."""
    if not PACKAGES_CACHE.exists():
        return {"exists": False, "path": str(PACKAGES_CACHE)}

    age = time.time() - PACKAGES_CACHE.stat().st_mtime
    data = _read_cache()
    return {
        "exists":   True,
        "path":     str(PACKAGES_CACHE),
        "packages": len(data),
        "age_secs": int(age),
        "fresh":    age < CACHE_TTL,
    }
