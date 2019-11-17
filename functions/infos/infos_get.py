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
# HEADERS
#

ERROR_HEADER = "Error import [infos_gets.py]"
HEADER_GET = "[netests - get_infos]"

########################################################################################################################
#
# Import Library
#

try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from nornir.core import Nornir
    # To use advanced filters
    from nornir.core.filter import F
    # To execute netmiko commands
    from nornir.plugins.tasks.networking import netmiko_send_command
    # To execute napalm get config
    from nornir.plugins.tasks.networking import napalm_get
    # To print task results
    from nornir.plugins.functions.text import print_result
except ImportError as importError:
    print(f"{ERROR_HEADER} nornir")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.infos.infos_converters import _napalm_infos_converter
    from functions.infos.infos_converters import _cumulus_infos_converter
    from functions.infos.infos_converters import _nexus_infos_converter
    from functions.infos.infos_converters import _arista_infos_converter
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.infos.infos_converters")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    exit(EXIT_FAILURE)
    print(importError)

########################################################################################################################
#
# Functions
#
def get_infos(nr: Nornir):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=generic_infos_get(),
        on_failed=True,
        num_workers=10
    )
    #print_result(data)

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def generic_infos_get(task):

    if INFOS_DATA_HOST_KEY not in task.host.keys():

        use_ssh = False

        if NEXUS_PLATEFORM_NAME in task.host.platform or ARISTA_PLATEFORM_NAME in task.host.platform:
            if 'connexion' in task.host.keys():
                if task.host.data.get('connexion', NOT_SET) == 'ssh' or task.host.get('connexion', NOT_SET):
                    use_ssh = True

        if task.host.platform == CUMULUS_PLATEFORM_NAME:
            _cumulus_get_infos(task)

        elif task.host.platform == EXTREME_PLATEFORM_NAME:
            _extreme_vsp_get_infos(task)

        elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM :
            if use_ssh and NEXUS_PLATEFORM_NAME == task.host.platform:
                _nexus_get_infos(task)

            elif use_ssh and ARISTA_PLATEFORM_NAME == task.host.platform:
                _arista_get_infos(task)

            else:
                _generic_infos_napalm(task)

        else:
            # RAISE EXCEPTIONS
            print(f"{HEADER_GET} No plateform selected for {task.host.name}...")

# ----------------------------------------------------------------------------------------------------------------------
#
# Function for devices which are compatible with NAPALM
#
def _generic_infos_napalm(task):
    pass
# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus Networks
#
def _cumulus_get_infos(task):
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks (VSP)
#
def _extreme_vsp_get_infos(task):
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus NXOS
#
def _nexus_get_infos(task):
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS
#
def _cisco_get_infos(task):
    raise NotImplemented

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista vEOS
#
def _arista_get_infos(task):
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper JunOS
#
def _junos_get_infos(task):
    raise NotImplemented