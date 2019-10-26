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
# Constantes
#
ERROR_HEADER = "Error import [main.py]"
HEADER = "[netests - main.py]"
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

try:
    from functions.retrieve_bgp import *
except ImportError as importError:
    print(f"{ERROR_HEADER} nornir")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from nornir import InitNornir
    from nornir.core import Nornir
except ImportError as importError:
    print(f"{ERROR_HEADER} nornir")
    print(importError)
    exit(EXIT_FAILURE)

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
def init_nornir(log_file="./nornir/nornir.log", log_level=NORNIR_DEBUG_MODE, ansible=False, virtual=False) -> Nornir:
    """
    Initialize Nornir object with the following files
    """

    config_file = str()

    if ansible:
        if virtual:
            config_file= "./nornir/config_ansible_virt.yml"
        else:
            config_file="./nornir/config_ansible.yml"
    else:
        if virtual:
            config_file="./nornir/config_virt.yml"
        else:
            config_file="./nornir/config_std_virt.yml"

    nr = InitNornir(
        config_file=config_file,
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

# ----------------------------------------------------------------------------------------------------------------------
#
# Basic test for CI
#
def execute_test():
    pass

########################################################################################################################
#
# Main function
#
@click.command()
@click.option('--ansible', default=False, help=f"If TRUE, inventory file {PATH_TO_INVENTORY_FILES}{ANSIBLE_INVENTORY}")
@click.option('--virtual', default=False, help=f"If TRUE, inventory file {PATH_TO_INVENTORY_FILES}{ANSIBLE_INVENTORY_VIRTUAL}")
@click.option('--tests', default=False, help=f"If TRUE, only compilation tests will be executed")
def main(ansible, virtual, tests):

    if tests:
        execute_test()
        exit(EXIT_SUCCESS)

    # Create Nornir object
    nr = init_nornir(
        log_file="./nornir/nornir.log",
        log_level="debug",
        ansible=ansible,
        virtual=virtual
    )

    test_to_execute = open_file(PATH_TO_VERITY_FILES+TEST_TO_EXECUTE_FILENAME)
    print(test_to_execute)

    print(nr.inventory.hosts)

    # ''''''''''''''''''''''''''''''''''''''''''''
    # 1. Check BGP sessions
    # ''''''''''''''''''''''''''''''''''''''''''''
    if test_to_execute[TEST_TO_EXC_BGP_KEY] is not False:
        bgp_session_up = get_bgp(nr)
        #print(f"{HEADER} All BGP sessions are UP regarding YAML file ({BGP_SESSIONS_TO_CHECK}) => {bgp_session_up}")
        #if test_to_execute['bgp'] is True and all_bgp_session_established is False:
        #    exit_value = False
        print(f"{HEADER} BGP_SESSIONS are {bgp_session_up} !!")
    else:
        print(f"{HEADER} BGP_SESSIONS tests are not executed !!")

    return EXIT_SUCCESS



########################################################################################################################
#
# Entry Point
#
if __name__ == "__main__":
    main()
