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
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

########################################################################################################################
#
# CONSTANTES
#
PATH_TO_VERITY_FILES = "./verity/"
PATH_TO_INVENTORY_FILES = "./inventory/"

###### INVENTORY ######
ANSIBLE_INVENTORY = "hosts"
ANSIBLE_INVENTORY_VIRTUAL = "hosts_virtual"

BGP_SRC_FILENAME = "bgp.yml"
TEST_TO_EXECUTE_FILENAME = "_test_to_execute.yml"

TO_EXECUTE_FILE_VALUE = ['INFO', 'TRUE', 'FALSE']