"""
ops/search.py — Search and list packages from the VUR index
"""

from __future__ import annotations

from typing import Any

from letx.repo.index import fetch_index

Package = dict[str, Any]

_SEARCH_FIELDS = ("name", "maintainer", "homepage")


def search_packages(
    keyword: str,
    category: str | None = None,
) -> list[Package]:
    """
    Search packages by keyword (case-insensitive).
    Keyword is matched against: name, maintainer, homepage.

    Args:
        keyword:  search keyword
        category: optional filter ("core"|"extra"|"multilib")

    Returns:
        Matching packages sorted by relevance (exact name first)
    """
    index = fetch_index()
    kw    = keyword.lower()

    results: list[Package] = []
    for pkg in index:
        if category and pkg.get("category", "").lower() != category.lower():
            continue
        for field in _SEARCH_FIELDS:
            if kw in str(pkg.get(field, "")).lower():
                results.append(pkg)
                break

    def _rank(pkg: Package) -> int:
        name = pkg["name"].lower()
        if name == kw:          return 0
        if name.startswith(kw): return 1
        if kw in name:          return 2
        return 3

    results.sort(key=_rank)
    return results


def list_packages(category: str | None = None) -> list[Package]:
    """
    Return all packages, optionally filtered by category.

    Args:
        category: None → all | "core"|"extra"|"multilib"
    """
    index = fetch_index()
    if category:
        return [p for p in index if p.get("category", "").lower() == category.lower()]
    return index


def available_categories() -> list[str]:
    """Return a sorted list of unique categories in the index."""
    index = fetch_index()
    return sorted({p["category"] for p in index if "category" in p})
