#/usr/bin/env python3.7
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
ERROR_HEADER = "Error import [mlag.py]"

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

try:
    from functions.global_tools import *
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.global_tools")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# MLAG CLASS
#
class MLAG:

    hostname: str
    local_id: str
    peer_id: str
    peer_alive: str
    peer_int: str
    peer_ip: str
    sys_mac: str

    # The following values are not used by the __eq__ function !!
    local_role: str
    peer_role: str
    local_priority: str
    peer_priority: str
    vxlan_anycast_ip: str



    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, hostname=NOT_SET, local_id=NOT_SET, peer_id=NOT_SET, local_role=NOT_SET,
                 peer_role=NOT_SET, peer_alive=NOT_SET, peer_int=NOT_SET, peer_ip=NOT_SET,
                 sys_mac=NOT_SET, local_priority=NOT_SET, peer_priority=NOT_SET, vxlan_anycast_ip=NOT_SET):

        self.hostname = hostname
        self.local_id = local_id
        self.peer_id = peer_id
        self.local_role = local_role
        self.peer_role = peer_role
        self.peer_alive = peer_alive
        self.peer_int = peer_int
        self.peer_ip = peer_ip
        self.sys_mac = sys_mac
        self.local_priority = local_priority
        self.peer_priority = peer_priority
        self.vxlan_anycast_ip = vxlan_anycast_ip

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, MLAG):
            return NotImplemented

        # Basic
        if (str(self.hostname) == str(self.hostname) and
                str(self.local_id) == str(other.local_id) and
                str(self.peer_id) == str(other.peer_id) and
                str(self.peer_int) == str(other.peer_int) and
                str(self.peer_ip) == str(other.peer_ip) and
                str(self.sys_mac) == str(other.sys_mac) and
                str(self.peer_alive) == str(other.peer_alive)):
            return True

        else:
            printline()
            print(self)
            print("IS NOT EQUAL TO\n")
            print(other)
            printline()
            return False

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<MLAG hostname={self.hostname} " \
               f"local_id={self.local_id} " \
               f"peer_id={self.peer_id} " \
               f"peer_int={self.peer_int} " \
               f"peer_ip={self.peer_ip} " \
               f"local_role={self.local_role} " \
               f"peer_role={self.peer_role} " \
               f"local_priority={self.local_priority} " \
               f"peer_priority={self.peer_priority} " \
               f"sys_mac={self.sys_mac} " \
               f"vxlan_anycast_ip={self.vxlan_anycast_ip} " \
               f"peer_alive={self.peer_alive}>\n"