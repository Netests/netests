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
ERROR_HEADER = "Error import [netbox.py]"
HEADER = "[netests - netbox.py]"
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
    from const.netbox_const import *
except ImportError as importError:
    print(f"{ERROR_HEADER} const.netbox_const")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import pynetbox
except ImportError as importError:
    print(f"{ERROR_HEADER} pynetbox")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# Functions
#
def netbox_init(netbox_url=NETBOX_URL, user_token=NETBOX_AUTOMATE_TOKEN, secure=False) -> pynetbox:

    protocol = ""

    if secure:
        protocol = "https://"
    else:
        protocol = "http://"

    return pynetbox.api(
        url=f"{protocol}{netbox_url}",
        token=user_token
    )











########################################################################################################################
#
# Main Function
#





########################################################################################################################
#
# Entry Point
#
if __name__ == "__main__":
    main()


