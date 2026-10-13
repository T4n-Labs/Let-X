"""
ops/search.py — Search, list, and local template lookup for Let-X
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from letx.repo.index import fetch_index
from letx.config import TEMPLATE_DIRS

Package = dict[str, Any]

# Default search fields — name and description only
# (homepage/maintainer excluded to avoid false positives)
_SEARCH_FIELDS = ("name", "description")


def search_packages(
    keyword: str,
    category: str | None = None,
) -> list[Package]:
    """
    Search packages by keyword (case-insensitive).
    Matches against: name, description.

    Args:
        keyword:  search keyword (plain name or quoted description)
        category: optional filter ("core"|"extra"|"multilib")

    Returns:
        Matching packages sorted by relevance (exact name first)
    """
    index = fetch_index()
    kw    = keyword.lower().strip('"').strip("'")

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
        cat = category.lower()
        return [p for p in index if p.get("category", "").lower() == cat]
    return index


def latest_packages(category: str | None = None, limit: int = 20) -> list[Package]:
    """
    Return the most recently added packages (last N in packages.json).

    Args:
        category: optional category filter
        limit:    max number of packages to return (default 20)
    """
    packages = list_packages(category=category)
    # packages.json order = insertion order, last = newest
    return packages[-limit:][::-1]


def available_categories() -> list[str]:
    """Return a sorted list of unique categories in the index."""
    index = fetch_index()
    return sorted({p["category"] for p in index if "category" in p})


def count_packages(category: str | None = None) -> dict[str, int]:
    """
    Return package counts.

    Returns:
        Dict with total and per-category counts
    """
    index = fetch_index()
    cats  = available_categories()
    result: dict[str, int] = {"total": len(index)}
    for cat in cats:
        result[cat] = sum(1 for p in index if p.get("category") == cat)
    if category:
        cat = category.lower()
        result["filtered"] = result.get(cat, 0)
    return result


# ─── Local template search ────────────────────────────────

class LocalTemplateResult:
    """Result of a local template search."""
    def __init__(
        self,
        found: bool,
        pkg_name: str,
        category: str | None = None,
        path: Path | None = None,
        files: list[str] | None = None,
    ) -> None:
        self.found    = found
        self.pkg_name = pkg_name
        self.category = category
        self.path     = path
        self.files    = files or []


def search_local_template(pkg_name: str) -> LocalTemplateResult:
    """
    Search for a package template across local directories.
    Checks: core → extra → multilib (in order).

    Args:
        pkg_name: package name to look for

    Returns:
        LocalTemplateResult with found status, location, and file list
    """
    search_order = ["core", "extra", "multilib"]

    for cat in search_order:
        template_path = TEMPLATE_DIRS.get(cat)
        if template_path is None:
            continue

        pkg_dir = template_path / pkg_name
        if pkg_dir.exists() and pkg_dir.is_dir():
            files = _list_template_files(pkg_dir)
            return LocalTemplateResult(
                found=True,
                pkg_name=pkg_name,
                category=cat,
                path=pkg_dir,
                files=files,
            )

    return LocalTemplateResult(found=False, pkg_name=pkg_name)


def _list_template_files(pkg_dir: Path) -> list[str]:
    """Recursively list all files in a template directory."""
    files = []
    for root, _, filenames in os.walk(pkg_dir):
        for fname in filenames:
            rel = os.path.relpath(os.path.join(root, fname), pkg_dir)
            files.append(rel)
    return sorted(files)
