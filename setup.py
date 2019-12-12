#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

########################################################################################################################
#
# Constantes
#
ERROR_HEADER = "Error import [setup.py]"
HEADER = "[netests - setup.py]"
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

########################################################################################################################
#
# Import Library
#

try:
    from setuptools import setup, find_packages
except ImportError as importError:
    print(f"{ERROR_HEADER} setuptools")
    print(importError)
    exit(EXIT_FAILURE)


########################################################################################################################
#
# Functions
#

def parse_requirements(filename):
    """ 
    load requirements from a pip requirements file 
    
    :param filename:
    """
    
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
            "noc-connections = netests.netests:main",
        ]
    },
)