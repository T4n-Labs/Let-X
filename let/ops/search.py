"""
ops/search.py — Cari package di index VUR
"""

from __future__ import annotations

from typing import Any

from let.repo.index import fetch_index

Package = dict[str, Any]

# Field yang ikut di-search
_SEARCH_FIELDS = ("name", "maintainer", "homepage")


def search_packages(
    keyword: str,
    category: str | None = None,
) -> list[Package]:
    """
    Cari packages berdasarkan keyword (case-insensitive).
    Keyword dicocokkan ke field: name, maintainer, homepage.

    Args:
        keyword:  kata kunci pencarian
        category: filter opsional ("core"|"extra"|"multilib")

    Returns:
        List package yang cocok, diurutkan: name-match duluan
    """
    index = fetch_index()
    kw    = keyword.lower()

    results: list[Package] = []
    for pkg in index:
        # Filter category dulu
        if category and pkg.get("category", "").lower() != category.lower():
            continue
        # Cek keyword di semua field
        for field in _SEARCH_FIELDS:
            if kw in str(pkg.get(field, "")).lower():
                results.append(pkg)
                break

    # Urutkan: exact name match → name contains → lainnya
    def _rank(pkg: Package) -> int:
        name = pkg["name"].lower()
        if name == kw:
            return 0
        if name.startswith(kw):
            return 1
        if kw in name:
            return 2
        return 3

    results.sort(key=_rank)
    return results


def list_packages(category: str | None = None) -> list[Package]:
    """
    Tampilkan semua package, opsional filter by category.

    Args:
        category: None → semua | "core"|"extra"|"multilib"
    """
    index = fetch_index()
    if category:
        return [p for p in index if p.get("category", "").lower() == category.lower()]
    return index


def available_categories() -> list[str]:
    """Return list kategori unik yang ada di index."""
    index = fetch_index()
    return sorted({p["category"] for p in index if "category" in p})
