#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-


"""
Description ...

"""

__author__ = "Dylan Hamel"
__maintainer__ = "Dylan Hamel"
__version__ = "1.0"
__email__ = "dylan.hamel@protonmail.com"
__status__ = "Prototype"
__copyright__ = "Copyright 2019"

######################################################
#
# Default value used for exit()
#
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

######################################################
#
# Import Library
#
try:
    from base.base_device import BaseDevice
except ImportError as importError:
    print("Error import [cumulus_device.py] BaseDevice")
    print(importError)
    exit(EXIT_FAILURE)

######################################################
#
# Cumulus Class
#
class CumulusDevice(BaseDevice):


    