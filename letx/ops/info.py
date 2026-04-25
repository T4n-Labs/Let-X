"""
ops/info.py — Detail lengkap satu package
"""

from __future__ import annotations

from typing import Any

from letx.repo.index import get_package
from letx.repo.fetch import package_exists_locally, local_package_path

Package = dict[str, Any]


def get_info(name: str) -> dict[str, Any] | None:
    """
    Ambil informasi lengkap sebuah package.
    Gabungkan data dari index + status lokal.

    Returns:
        Dict berisi semua info package + status lokal,
        atau None jika package tidak ditemukan.
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
