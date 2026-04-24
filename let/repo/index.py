"""
repo/index.py — Fetch & cache packages.json dari VUR
"""

import json
import time
from pathlib import Path
from typing import Any

import httpx

from let.config import (
    PACKAGES_URL,
    PACKAGES_CACHE,
    CACHE_TTL,
    ensure_dirs,
)

Package = dict[str, Any]


def _cache_valid() -> bool:
    """Cek apakah cache masih fresh (belum melewati TTL)."""
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
    Ambil index packages dari VUR.
    - Pakai cache lokal jika masih valid dan force=False
    - Fetch dari GitHub jika cache expired atau force=True

    Returns:
        List of package dicts dari packages.json
    
    Raises:
        httpx.HTTPError: Jika gagal fetch dari GitHub
        RuntimeError: Jika tidak ada cache dan tidak bisa online
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
        # Jika gagal tapi ada cache lama, pakai itu
        if PACKAGES_CACHE.exists():
            return _read_cache()
        raise RuntimeError(
            f"Gagal fetch index dari GitHub dan tidak ada cache lokal.\n"
            f"Error: {e}"
        ) from e


def get_package(name: str, force: bool = False) -> Package | None:
    """Cari satu package berdasarkan nama eksak (case-insensitive)."""
    index = fetch_index(force=force)
    name_lower = name.lower()
    for pkg in index:
        if pkg["name"].lower() == name_lower:
            return pkg
    return None


def cache_info() -> dict[str, Any]:
    """Informasi status cache saat ini."""
    if not PACKAGES_CACHE.exists():
        return {"exists": False, "path": str(PACKAGES_CACHE)}
    
    age = time.time() - PACKAGES_CACHE.stat().st_mtime
    data = _read_cache()
    return {
        "exists":    True,
        "path":      str(PACKAGES_CACHE),
        "packages":  len(data),
        "age_secs":  int(age),
        "fresh":     age < CACHE_TTL,
    }
