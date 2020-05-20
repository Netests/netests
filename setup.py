#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def parse_requirements(filename):
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="netests",
    version="0.1",
    packages=find_packages(),
    author="Dylan Hamel",
    author_email="dylan.hamel@protonmail.com",
    description="Netests.io install package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/DylanHamel/netests/-/tree/master",
    install_requires=parse_requirements("requirements.txt"),
    entry_points={
        "console_scripts": [
            "netests = netests.netests:main",
        ]
    },
    python_requires='>=3.6',
)
