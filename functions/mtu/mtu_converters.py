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
ERROR_HEADER = "Error import [mtu_converters.py]"
HEADER_GET = "[netests - mtu_converters]"

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
    from protocols.mtu import InterfaceMTU, ListInterfaceMTU, MTU
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.mtu")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.discovery_protocols.discovery_functions import _mapping_interface_name
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.discovery_protocols.discovery_functions")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# Functions
#

# ----------------------------------------------------------------------------------------------------------------------
#
# NAPALM MTU converter
#
def _napalm_mtu_converter(hostname:str(), cmd_output:json) -> MTU:
	pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus MTU converter
#
def _cumulus_mtu_converter(hostname:str(), cmd_output:json) -> MTU:

	if cmd_output is None:
		return None

	interface_mtu_lst = ListInterfaceMTU(
		list()
	)

	for interface in cmd_output:
		if "swp" in interface or "eth" in interface:
			interface_mtu_lst.interface_mtu_lst.append(
				InterfaceMTU(
					interface_name=_mapping_interface_name(
						interface
					),
					mtu_size=cmd_output.get(interface).get('iface_obj').get('mtu', NOT_SET)
				)
			)

	return MTU(
		hostname=hostname,
		interface_mtu_lst=interface_mtu_lst
	)

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus MTU Converter
#
def _nexus_mtu_converter(hostname:str(), cmd_output:json) -> MTU:

	if cmd_output is None:
		return None

	interface_mtu_lst = ListInterfaceMTU(
		list()
	)

	if "TABLE_interface" in cmd_output.keys():
		if "ROW_interface" in cmd_output.get("TABLE_interface").keys():
			for interface in cmd_output.get("TABLE_interface").get("ROW_interface"):
				if "Ethernet" in interface.get("interface", NOT_SET) or \
                        "mgmt" in interface.get("interface", NOT_SET):
					interface_mtu_lst.interface_mtu_lst.append(
						InterfaceMTU(
							interface_name=_mapping_interface_name(
								interface.get("interface", NOT_SET)
							),
							mtu_size=interface.get("eth_mtu", NOT_SET)
						)
					)

	return MTU(
		hostname=hostname,
		interface_mtu_lst=interface_mtu_lst
	)
# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS MTU Converter
#
def _ios_mtu_converter(hostname:str(), cmd_output:list) -> MTU:

	if cmd_output is None:
		return None

	interface_mtu_lst = ListInterfaceMTU(
		list()
	)
	
	for interface in cmd_output:
		interface_mtu_lst.interface_mtu_lst.append(
			InterfaceMTU(
				interface_name=_mapping_interface_name(
					interface[0]
				),
				mtu_size=interface[8]
			)
		)

	return MTU(
		hostname=hostname,
		interface_mtu_lst=interface_mtu_lst
	)
	
# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS XR MTU Converter
#
def _iosxr_mtu_converter(hostname:str(), cmd_output:list) -> MTU:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista MTU addresses Converter
#
def _arista_mtu_converter(hostname:str(), cmd_output:json) -> MTU:

	if cmd_output is None:
		return None

	interface_mtu_lst = ListInterfaceMTU(
		list()
	)

	if "interfaces" in cmd_output.keys():
		for interface in cmd_output.get("interfaces"):
			if "Ethernet" in interface or "Management" in interface:
				interface_mtu_lst.interface_mtu_lst.append(
					InterfaceMTU(
						interface_name=_mapping_interface_name(
							interface
						),
						mtu_size=cmd_output.get("interfaces").get(interface).get('mtu', NOT_SET)
					)
				)

	return MTU(
		hostname=hostname,
		interface_mtu_lst=interface_mtu_lst
	)

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper MTU Converter
#
def _juniper_mtu_converter(hostname:str(), cmd_output:json) -> MTU:

	if cmd_output is None:
		return None

	interface_mtu_lst = ListInterfaceMTU(
		list()
	)

	if "interface-information" in cmd_output.keys():
		for interface in cmd_output.get("interface-information")[0].get("physical-interface"):

			if ("em" in interface.get("name")[0].get("data", NOT_SET) and \
                "demux"not in interface.get("name")[0].get("data", NOT_SET)) or \
					"fxp" in interface.get("name")[0].get("data", NOT_SET):

				interface_mtu_lst.interface_mtu_lst.append(
					InterfaceMTU(
						interface_name=_mapping_interface_name(
							interface.get("name")[0].get("data", NOT_SET)
						),
						mtu_size=interface.get("mtu")[0].get("data", NOT_SET)
					)
				)

	return MTU(
		hostname=hostname,
		interface_mtu_lst=interface_mtu_lst
	)
	
# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks VSP MTU Converter
#
def _extreme_vsp_mtu_converter(hostname:str(), cmd_output:dict) -> MTU:
    pass
