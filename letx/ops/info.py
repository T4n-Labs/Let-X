"""
ops/info.py — Package info and local template details for Let-X
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from letx.repo.index import get_package
from letx.repo.fetch import package_exists_locally, local_package_path
from letx.ops.search import search_local_template

Package = dict[str, Any]


def get_info(name: str) -> dict[str, Any] | None:
    """
    Fetch full details for a package from the VUR index.
    Combines index data with local template status.

    Returns:
        Dict with all package fields + local status,
        or None if the package was not found.
    """
    pkg = get_package(name)
    if not pkg:
        return None

    category   = pkg.get("category", "")
    is_local   = package_exists_locally(category, name)
    local_path = local_package_path(category, name)

    return {
        **pkg,
        "installed_locally": is_local,
        "local_path": str(local_path) if local_path else None,
    }


def get_local_template_info(pkg_name: str) -> dict[str, Any]:
    """
    Get detailed info about a locally stored template.

    Returns:
        Dict with found status, category, path, files, and VUR index data
    """
    result = search_local_template(pkg_name)

    info: dict[str, Any] = {
        "found":    result.found,
        "pkg_name": result.pkg_name,
        "category": result.category,
        "path":     str(result.path) if result.path else None,
        "files":    result.files,
        "vur_data": None,
    }

    # Try to enrich with VUR index data
    if result.found:
        pkg = get_package(pkg_name)
        if pkg:
            info["vur_data"] = pkg

    return info
