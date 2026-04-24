"""
tests/test_search.py — Unit test untuk search & index
"""

import json
import time
from pathlib import Path

import pytest

# ─── Fixture: mock packages.json ──────────────────────────

MOCK_PACKAGES = [
    {"name": "discord",    "category": "extra",    "path": "extra/discord",    "version": "0.0.134",  "homepage": "https://discord.com",      "maintainer": "Gh0sT4n <a@b.com>"},
    {"name": "wine",       "category": "multilib", "path": "multilib/wine",    "version": "11.5",     "homepage": "http://winehq.org",         "maintainer": "Helmut <h@h.com>"},
    {"name": "linux-zen",  "category": "core",     "path": "core/linux-zen",   "version": "6.13.0",   "homepage": "https://kernel.org",        "maintainer": "JuanMa <j@j.com>"},
    {"name": "obsidian",   "category": "extra",    "path": "extra/obsidian",   "version": "1.12.7",   "homepage": "https://obsidian.md",       "maintainer": "Naz <n@n.com>"},
    {"name": "zen-browser","category": "extra",    "path": "extra/zen-browser","version": "1.19.8b",  "homepage": "https://zen-browser.app",   "maintainer": "Naz <n@n.com>"},
]


@pytest.fixture
def fake_cache(tmp_path, monkeypatch):
    """Ganti PACKAGES_CACHE dengan file temp berisi mock data."""
    cache_file = tmp_path / "packages.json"
    cache_file.write_text(json.dumps(MOCK_PACKAGES))

    import let.config as cfg
    monkeypatch.setattr(cfg, "PACKAGES_CACHE", cache_file)
    monkeypatch.setattr(cfg, "CACHE_TTL", 9999)  # Selalu fresh

    # Patch juga di index module
    import let.repo.index as idx
    monkeypatch.setattr(idx, "PACKAGES_CACHE", cache_file)
    monkeypatch.setattr(idx, "CACHE_TTL", 9999)

    return cache_file


# ─── Tests: index ─────────────────────────────────────────

def test_fetch_index_from_cache(fake_cache):
    from let.repo.index import fetch_index
    packages = fetch_index()
    assert len(packages) == len(MOCK_PACKAGES)


def test_get_package_found(fake_cache):
    from let.repo.index import get_package
    pkg = get_package("discord")
    assert pkg is not None
    assert pkg["category"] == "extra"


def test_get_package_case_insensitive(fake_cache):
    from let.repo.index import get_package
    assert get_package("DISCORD") is not None
    assert get_package("Discord") is not None


def test_get_package_not_found(fake_cache):
    from let.repo.index import get_package
    assert get_package("nonexistent-pkg") is None


# ─── Tests: search ────────────────────────────────────────

def test_search_by_name(fake_cache):
    from let.ops.search import search_packages
    results = search_packages("discord")
    assert len(results) == 1
    assert results[0]["name"] == "discord"


def test_search_partial(fake_cache):
    from let.ops.search import search_packages
    results = search_packages("zen")
    names = [r["name"] for r in results]
    assert "zen-browser" in names
    assert "linux-zen" in names


def test_search_with_category_filter(fake_cache):
    from let.ops.search import search_packages
    results = search_packages("zen", category="extra")
    assert all(r["category"] == "extra" for r in results)
    assert "linux-zen" not in [r["name"] for r in results]


def test_search_no_results(fake_cache):
    from let.ops.search import search_packages
    assert search_packages("xxxnotfoundxxx") == []


# ─── Tests: list ──────────────────────────────────────────

def test_list_all(fake_cache):
    from let.ops.search import list_packages
    assert len(list_packages()) == len(MOCK_PACKAGES)


def test_list_by_category(fake_cache):
    from let.ops.search import list_packages
    extra = list_packages(category="extra")
    assert all(p["category"] == "extra" for p in extra)
    assert len(extra) == 3


def test_available_categories(fake_cache):
    from let.ops.search import available_categories
    cats = available_categories()
    assert set(cats) == {"core", "extra", "multilib"}
