"""Install packages as defined in this file into the Python environment."""
from setuptools import setup, find_packages

setup(
    name="pyram",
    author="Teko",
    author_email="dev@teko.vn",
    description="RAM lib for Python",
    version="0.9.0",
    packages=find_packages(where=".", exclude=["tests"]),
    install_requires=[
        "setuptools>=45.0",
    ],
)