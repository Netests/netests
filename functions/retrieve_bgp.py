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
ERROR_HEADER = "Error import [retrieve_bgp]"

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
    from nornir.core import Nornir
except ImportError as importError:
    print(f"{ERROR_HEADER} nornir")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# Functions
#
def check_cumulus_bgp(nr: Nornir):

    devices = nr.filter(
        F(groups__contains="leaf") |
        F(groups__contains="spine") |
        F(groups__contains="exit")
    )

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[check_cumulus_lldp] no device selected.")

    path_url = os.environ['tests_path']+BGP_SESSIONS_TO_CHECK

    data = devices.run(
        task=netests.bgp._cumulus_get_bgp_summary,
        on_failed=True,
        num_workers=10
    )
    #print_result(data)
    if data.failed is True:
        return False

    netests.bgp._cumulus_bgp_summary_converter(devices)
    content = open_file(path_url)
    content = (content)

    return (netests.bgp.compare_topology_and_bgp_output(content, devices))
