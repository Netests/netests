#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
Add a description ....

"""

__author__ = "Dylan Hamel"
__maintainer__ = "Dylan Hamel"
__version__ = "1.0"
__email__ = "dylan.hamel@protonmail.com"
__status__ = "Prototype"
__copyright__ = "Copyright 2019"

########################################################################################################################
#
# Default value used for exit()
#
ERROR_HEADER = "Error import [main.py]"

########################################################################################################################
#
# Import Library
#
try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} nornir")
    print(importError)
    exit(EXIT_FAILURE)

from nornir import InitNornir
from nornir.core import Nornir

try:
    import click
except ImportError as importError:
    print(f"{ERROR_HEADER} click")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import yaml
except ImportError as importError:
    print(f"{ERROR_HEADER} yaml")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# Functions
#
def init_nornir(log_file="./nornir/nornir.log", log_level="debug", ansible=False, virtual=False) -> Nornir:
    """
    Initialize Nornir object with the following files
    """
    if ansible:
        if virtual:
            nr = InitNornir(
                config_file="./nornir/config_ansible_virt.yml",
                logging={
                    "file": log_file,
                    "level": log_level
                }
            )
        else:
            nr = InitNornir(
                config_file="./nornir/config_ansible.yml",
                logging={
                    "file": log_file,
                    "level": log_level
                }
            )
    else:
        nr = InitNornir(
            config_file="./nornir/config_std.yml",
            logging={
                "file": log_file,
                "level": log_level
            }
        )


    return nr

# ----------------------------------------------------------------------------------------------------------------------
#
# Open a YAML File and open VM_path contains into YAML file
#
def open_file(path: str()) -> dict():
    """
    This function  will open a yaml file and return is data

    Args:
        param1 (str): Path to the yaml file

    Returns:
        str: Node name
    """

    with open(path, 'r') as yamlFile:
        try:
            data = yaml.load(yamlFile)
        except yaml.YAMLError as exc:
            print(exc)

    return data

########################################################################################################################
#
# Entry Point
#
@click.command()
@click.option('--ansible', default=False, help=f"If this value is TRUE, inventory file {PATH_TO_INVENTORY_FILES}{ANSIBLE_INVENTORY}")
@click.option('--virtual', default=False, help=f"If this value is TRUE, inventory file {PATH_TO_INVENTORY_FILES}{ANSIBLE_INVENTORY_VIRTUAL}")
def main(ansible, virtual):

    # Create Nornir object
    nr = init_nornir()

    test_to_execute = open_file(PATH_TO_VERITY_FILES+TEST_TO_EXECUTE_FILENAME)

    print(test_to_execute)



    return EXIT_SUCCESS



########################################################################################################################
#
# Entry Point
#
if __name__ == "__main__":
    main()
