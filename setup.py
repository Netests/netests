#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def parse_requirements(filename):
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


setup(
    name="netests",
    version="0.1",
    packages=find_packages(),
    author="Dylan Hamel",
    author_email="dylan.hamel@protonmail.com",
    install_requires=parse_requirements("requirements.txt"),
    entry_points={
        "console_scripts": [
            "netests = netests.netests:main",
        ]
    },
)
