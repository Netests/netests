#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
Description ...

"""

__author__ = "Dylan Hamel"
__maintainer__ = "Dylan Hamel"
__version__ = "0.1"
__email__ = "dylan.hamel@protonmail.com"
__status__ = "Prototype"
__copyright__ = "Copyright 2019"

########################################################################################################################
#
# HEADERS
#
ERROR_HEADER = "Error import [infos.py]"

########################################################################################################################
#
# Default value used for exit()
#
try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# BGP SESSION CLASS
#
class SystemInfos:

    hostname: str
    version: str

    # The following values are not used by the __eq__ function !!
    serial: str
    domain: str
    base_mac: str
    memory: str
    vendor: str
    model: str
    snmp: list
    interfaces_lst: list

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, hostname=NOT_SET, domain=NOT_SET, version=NOT_SET, build=NOT_SET, serial=NOT_SET,
                 base_mac=NOT_SET, memory=NOT_SET, vendor=NOT_SET, model=NOT_SET, snmp_ips=list(), interfaces_lst=list()):
        self.hostname = hostname
        self.domain = domain
        self.version = version
        self.build = build
        self.serial = serial
        self.base_mac = base_mac
        self.memory = memory
        self.vendor = vendor
        self.model = model
        self.snmp_ips = snmp_ips
        self.interfaces_lst = interfaces_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, SystemInfos):
            return NotImplemented

        return ((str(self.hostname) == str(other.hostname)) and
                (str(self.version) == str(other.version)))

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<SystemInfos hostname={self.hostname} " \
                f"domain={self.domain} " \
                f"version={self.version} " \
                f"build={self.build} " \
                f"serial={self.serial} " \
                f"base_mac={self.base_mac} " \
                f"memory={self.memory} "\
                f"vendor={self.vendor} " \
                f"model={self.model} "\
                f"snmp_ips={self.snmp_ips} " \
                f"interfaces_lst={self.interfaces_lst}>\n"

