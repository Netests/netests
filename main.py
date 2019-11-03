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
    print(f"{ERROR_HEADER} const.constants")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.lldp.get_lldp import *
    from functions.lldp.lldp_compare import compare_lldp
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.ping")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.ping.execute_ping import *
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.ping")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.vrf.vrf_compare import *
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.vrf")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.bgp.bgp_compare import *
    from functions.bgp.bgp_reports import *
    from functions.bgp.bgp_gets import *
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.bgp")
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
            config_file="./nornir/config_std.yml"

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
@click.option('--reports', default=False, help=f"If TRUE, configuration reports will be create")
def main(ansible, virtual, tests, reports):

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

    # ''''''''''''''''''''''''''''''''''''''''''''
    # 1. Check BGP sessions
    # ''''''''''''''''''''''''''''''''''''''''''''
    if test_to_execute[TEST_TO_EXC_BGP_KEY] is not False:
        get_bgp(nr)
        bgp_data = open_file(f"{PATH_TO_VERITY_FILES}{BGP_SRC_FILENAME}")
        same = compare_bgp(nr, bgp_data)
        if reports:
            create_reports(nr, bgp_data)
        if test_to_execute[TEST_TO_EXC_BGP_KEY] is True and same is False:
            exit_value = False
        print(
            f"{HEADER} BGP sessions are the same that defined in {PATH_TO_VERITY_FILES}{BGP_SRC_FILENAME} = {same} !!")
    else:
        print(f"{HEADER} BGP_SESSIONS tests are not executed !!")


    dict
    # ''''''''''''''''''''''''''''''''''''''''''''
    # 2. LLDP Neighbors check
    # ''''''''''''''''''''''''''''''''''''''''''''
    if TEST_TO_EXC_LLDP_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_LLDP_KEY] is not False:
            get_lldp(nr)
            lldp_data = open_file(f"{PATH_TO_VERITY_FILES}{LLDP_SRC_FILENAME}")
            same = compare_lldp(nr, lldp_data)
            if test_to_execute[TEST_TO_EXC_LLDP_KEY] is True and same is False:
                exit_value = False
            print(
                f"{HEADER} LLDP sessions are the same that defined in {PATH_TO_VERITY_FILES}{LLDP_SRC_FILENAME} = {same} !!")
        else:
            print(f"{HEADER} LLDP sessions tests are not executed !!")
    else:
        print(f"{HEADER} LLDP sessions key is not defined in {PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!")

    # ''''''''''''''''''''''''''''''''''''''''''''
    # 3. Check VRF on devices
    # ''''''''''''''''''''''''''''''''''''''''''''
    if TEST_TO_EXC_VRF_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_VRF_KEY] is not False:
            get_vrf(nr)
            vrf_data = open_file(f"{PATH_TO_VERITY_FILES}{VRF_SRC_FILENAME}")
            same = compare_vrf(nr, vrf_data)
            if test_to_execute[TEST_TO_EXC_VRF_KEY] is True and same is False:
                exit_value = False
            print(f"{HEADER} VRF are the same that defined in {PATH_TO_VERITY_FILES}{VRF_SRC_FILENAME} = {same} !!")
        else:
            print(f"{HEADER} VRF tests are not executed !!")
    else:
        print(f"{HEADER} VRF key is not defined in {PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!")

    # ''''''''''''''''''''''''''''''''''''''''''''
    # 4. Execute PING on devices
    # ''''''''''''''''''''''''''''''''''''''''''''
    if TEST_TO_EXC_PING_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_PING_KEY] is not False:
            works = execute_ping(nr)
            if test_to_execute[TEST_TO_EXC_PING_KEY] is True and works is False:
                exit_value = False
            print(f"{HEADER} Pings defined in {PATH_TO_VERITY_FILES}{PING_SRC_FILENAME} work = {works} !!")
        else:
            print(f"{HEADER} Pings have not been executed !!")
    else:
        print(f"{HEADER} PING key is not defined in {PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!")



    return EXIT_SUCCESS



########################################################################################################################
#
# Entry Point
#
if __name__ == "__main__":
    main()
