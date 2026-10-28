from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="letx",
    version="1.0.0",
    author="Gh0sT4n",
    author_email="darskevoid@gmail.com",
    description="CLI Tools - VUR Helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "letx=letx.main:main",
        ],
    },
)
