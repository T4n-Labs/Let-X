# setup.py — Compatibility shim untuk xbps-src python3-module build style
# xbps-src memanggil: python3 setup.py build
# setuptools akan baca semua config dari pyproject.toml secara otomatis
from setuptools import setup

setup()
