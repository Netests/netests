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

NOT_SET = "NOT_SET"

##### REPORT PATH #####
REPORT_FOLDER = "reports/"
TEMPLATES_PATH = "templates/"
TEXTFSM_PATH = f"{TEMPLATES_PATH}textfsm/"
JINJA2_PATH = f"{TEMPLATES_PATH}jinja2/"
JINJA2_PING_PATH = f"{JINJA2_PATH}ping/"
JINJA2_PING_RESULT = f"{JINJA2_PING_PATH}result/"

###### NORNIR INIT ######
NORNIR_DEBUG_MODE = 'debug'

PATH_TO_VERITY_FILES = "./verity/"
PATH_TO_INVENTORY_FILES = "./inventory/"

###### INVENTORY ######
ANSIBLE_INVENTORY = "hosts_virtual"
ANSIBLE_INVENTORY_VIRTUAL = "hosts_virtual"

NAPALM_COMPATIBLE_PLATEFORM = ['junos', 'cisco_nxos', 'nxos', 'cisco_ios', 'ios', 'arista_eos', 'eos']
JUNOS_PLATEFORM_NAME = 'junos'
CUMULUS_PLATEFORM_NAME = 'linux'
NEXUS_PLATEFORM_NAME = 'nxos'
CISCO_PLATEFORM_NAME = 'cisco_ios'
ARISTA_PLATEFORM_NAME = 'eos'
EXTREME_PLATEFORM_NAME = 'extreme_vsp'

###### TESTS TO EXECUTE FILE ######
TEST_TO_EXECUTE_FILENAME = "_test_to_execute.yml"
TO_EXECUTE_FILE_VALUE = ['INFO', 'TRUE', 'FALSE']
YAML_BGKP_ASN_KEY = 'asn'
BGP_SRC_FILENAME = "bgp.yml"
VRF_SRC_FILENAME = "vrf.yml"
PING_SRC_FILENAME = "ping.yml"
LLDP_SRC_FILENAME = "lldp.yml"
CDP_SRC_FILENAME = "cdp.yml"
OSPF_SRC_FILENAME = "ospf.yml"
TEST_TO_EXC_BGP_KEY = 'bgp'
TEST_TO_EXC_VRF_KEY = 'vrf'
TEST_TO_EXC_PING_KEY = 'ping'
TEST_TO_EXC_LLDP_KEY = 'lldp'
TEST_TO_EXC_CDP_KEY = 'cdp'
TEST_TO_EXC_OSPF_KEY = 'ospf'

YAML_ALL_GROUPS_KEY = 'all'
YAML_GROUPS_KEY = 'groups'
YAML_DEVICES_KEY = 'devices'

###### CUMULUS COMMANDS
CUMULUS_GET_BGP = 'net show bgp summary json'
CUMULUS_GET_BGP_VRF = "net show bgp vrf {} summary json"
CUMULUS_GET_VRF = "net show vrf"
CUMULUS_GET_LLDP_CDP = "net show lldp json"
CUMULUS_GET_OSPF = "net show ospf neighbor detail json"
CUMULUS_GET_OSPF_VRF = "net show ospf vrf {} neighbor detail json"
CUMULUS_GET_OSPF_RID = "net show ospf json"
CUMULUS_GET_OSPF_RID_VRF = "net show ospf vrf {} json"

##### NEXUS COMMANDS
NEXUS_GET_BGP = 'show bgp sessions | json'
NEXUS_GET_BGP_VRF = "show bgp sessions vrf {} | json"
NEXUS_GET_VRF = "show vrf all | json"
NEXUS_GET_LLDP = "show lldp neighbors detail | json"
NEXUS_GET_CDP = "show cdp neighbors detail | json"
NEXUS_GET_OSPF = "show ip ospf neighbors detail | json"
NEXUS_GET_OSPF_VRF = "show ip ospf neighbors vrf {} | json"
NEXUS_GET_OSPF_RID = "show ip ospf | json"
NEXUS_GET_OSPF_RID_VRF = "show ip ospf vrf {} | json"

##### ARISTA COMMANDS
ARISTA_GET_BGP = 'show ip bgp summary | json'
ARISTA_GET_BGP_VRF = "show ip bgp summary vrf {} | json"
ARISTA_GET_VRF = "show vrf | json"
ARISTA_GET_LLDP = "show lldp neighbors detail | json"
ARISTA_GET_OSPF = "show ip ospf neighbor detail | json"
ARISTA_GET_OSPF_RID = "show ip ospf | json"
ARISTA_GET_OSPF_VRF = "show ip ospf neighbor detail vrf {} | json"
ARISTA_GET_OSPF_RID_VRF = "show ip ospf vrf {} | json"

##### BGP CONSTANTES
BGP_SESSIONS_HOST_KEY = 'bgp_sessions'
BGP_WORKS_KEY = 'bgp_works'

BGP_STATE_UP_LIST = ['ESTABLISHED','established', 'Established', 'Estab','UP', 'up', 'Up']
BGP_STATE_BRIEF_UP = "UP"
BGP_STATE_BRIEF_DOWN = "DOWN"

##### OSPF CONSTANTES
OSPF_SESSIONS_HOST_KEY = 'ospf_sessions'
OSPF_WORKS_KEY = 'ospf_works'

##### VRF CONSTANTES
VRF_DATA_KEY = 'vrf_data'
VRF_NAME_DATA_KEY = 'vrf_name_data'
VRF_WORKS_KEY = 'vrf_works'

##### PING CONSTANTES
PING_DATA_HOST_KEY = 'ping_data'

##### LLDP CONSTANTES
LLDP_DATA_HOST_KEY = 'lldp_data'
LLDP_WORKS_KEY = 'lldp_works'

##### LLDP CONSTANTES
CDP_DATA_HOST_KEY = 'cdp_data'
CDP_WORKS_KEY = 'cdp_works'
