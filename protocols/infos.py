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
    domain: str
    version: str
    serial: str

    # The following values are not used by the __eq__ function !!
    base_mac: str
    memory: str
    vendor: str
    model: str
    syslog: str
    snmp: str
    interfaces_lst: list

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, hostname=NOT_SET, domain=NOT_SET, version=NOT_SET, serial=NOT_SET, base_mac=NOT_SET,
                 memory=NOT_SET, vendor=NOT_SET, model=NOT_SET, syslog=NOT_SET, snmp=NOT_SET, interfaces_lst=list()):
        self.hostname = hostname
        self.domain = domain
        self.version = version
        self.serial = serial
        self.base_mac = base_mac
        self.memory = memory
        self.vendor = vendor
        self.model = model
        self.syslog = syslog
        self.snmp = snmp
        self.interfaces_lst = interfaces_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, SystemInfos):
            return NotImplemented

        return ((str(self.hostname) == str(other.hostname)) and
                (str(self.domain) == str(other.domain)) and
                (str(self.version) == str(other.version)) and
                (str(self.serial) == str(other.serial)))

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<SystemInfos hostname={self.hostname} " \
                f"domain={self.domain} " \
                f"version={self.version} " \
                f"serial={self.serial} " \
                f"base_mac={self.base_mac} " \
                f"memory={self.memory} "\
                f"vendor={self.vendor} " \
                f"model={self.model} "\
                f"syslog={self.syslog} " \
                f"snmp={self.snmp} " \
                f"interfaces_lst={self.interfaces_lst}>\n"

