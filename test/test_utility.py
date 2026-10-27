import pytest
from letx.src.utility import format_dependencies, parse_template

def test_format_dependencies_normal():
    deps = "git cmake pkg-config"
    result = format_dependencies(deps)
    assert "-) git" in result
    assert "-) cmake" in result
    assert "-) pkg-config" in result

def test_format_dependencies_empty():
    assert format_dependencies("") == "N/A"
    assert format_dependencies("N/A") == "N/A"

def test_parse_template():
    template_content = """
pkgname=calamares
version=3.4.2
revision=3
build_style=cmake
depends="kconfig kcoreaddons"
license="GPL-3.0-or-later"
"""
    result = parse_template(template_content)
    assert result['revision'] == '3'
    assert result['build_style'] == 'cmake'
    assert result['depends'] == 'kconfig kcoreaddons'
    assert result['license'] == 'GPL-3.0-or-later'
    assert result['hostmakedepends'] == 'N/A' # Tidak ada di template