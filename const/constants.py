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
ANSIBLE_INVENTORY = "hosts"
ANSIBLE_INVENTORY_VIRTUAL = "hosts_virtual"

NAPALM_COMPATIBLE_PLATEFORM = [
    'junos', 'cisco_nxos', 'nxos', 'cisco_ios', 'ios', 'iosxr', 'cisco_iosxr', 'arista_eos', 'eos'
]
JUNOS_PLATEFORM_NAME = 'junos'
CUMULUS_PLATEFORM_NAME = 'linux'
NEXUS_PLATEFORM_NAME = 'nxos'
CISCO_IOS_PLATEFORM_NAME = 'ios'
CISCO_IOSXR_PLATEFORM_NAME = 'iosxr'
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
IPV4_SRC_FILENAME = "ipv4.yml"
IPV6_SRC_FILENAME = "ipv6.yml"
STATIC_SRC_FILENAME = "static.yml"
INFOS_SRC_FILENAME = "sys_infos.yml"
TEST_TO_EXC_BGP_KEY = 'bgp'
TEST_TO_EXC_BGP_UP_KEY = 'bgp_all_up'
TEST_TO_EXC_VRF_KEY = 'vrf'
TEST_TO_EXC_PING_KEY = 'ping'
TEST_TO_EXC_LLDP_KEY = 'lldp'
TEST_TO_EXC_CDP_KEY = 'cdp'
TEST_TO_EXC_OSPF_KEY = 'ospf'
TEST_TO_EXC_IPV4_KEY = 'ipv4'
TEST_TO_EXC_IPV6_KEY = 'ipv6'
TEST_TO_EXC_STATIC_KEY = 'static'
TEST_TO_EXC_INFOS_KEY = 'sys_infos'

YAML_ALL_GROUPS_KEY = 'all'
YAML_GROUPS_KEY = 'groups'
YAML_DEVICES_KEY = 'devices'

##### JUNOS COMMANDS
JUNOS_GET_INFOS = "show version | display json"
JUNOS_GET_INT = "show interfaces brief | display json"
JUNOS_GET_MEMORY = "show system memory | display json"
JUNOS_GET_CONFIG_SYSTEM = "show configuration system | display json"
JUNOS_GET_SERIAL = "show chassis hardware detail | display json"
JUNOS_GET_BGP = "show bgp summary | display json"
JUNOS_GET_BGP_VRF = "show bgp summary instance {} | display json"
JUNOS_GET_VRF_DETAIL = "show route instance detail | display json"
JUNOS_GET_VRF = "show route instance | display json"

###### CUMULUS COMMANDS
CUMULUS_GET_BGP = 'net show bgp summary json'
CUMULUS_GET_BGP_VRF = "net show bgp vrf {} summary json"
CUMULUS_GET_VRF = "net show bgp vrf"
CUMULUS_GET_LLDP_CDP = "net show lldp json"
CUMULUS_GET_OSPF = "net show ospf neighbor detail json"
CUMULUS_GET_OSPF_VRF = "net show ospf vrf {} neighbor detail json"
CUMULUS_GET_OSPF_RID = "net show ospf json"
CUMULUS_GET_OSPF_RID_VRF = "net show ospf vrf {} json"
CUMULUS_GET_IPV4 = "net show interface json"
CUMULUS_GET_STATIC = "net show route static json"
CUMULUS_GET_STATIC_VRF = "net show route vrf {} static json"
CUMULUS_GET_INFOS = "net show system json"
CUMULUS_GET_SNMP = "net show snmp-server status json"

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
NEXUS_GET_IPV4 = "show ip int | json"
NEXUS_GET_IPV4_VRF = "show ip int vrf {} | json"
NEXUS_GET_STATIC = "show ip route static | json"
NEXUS_GET_STATIC_VRF = "show ip route static  vrf {} | json"
NEXUS_GET_INFOS = "show version | json"
NEXUS_GET_INT = "show interface brief | json"
NEXUS_GET_SNMP = "show snmp host | json"
NEXUS_GET_DOMAIN = "show hostname | json"

##### ARISTA COMMANDS
ARISTA_GET_BGP = 'show ip bgp summary | json'
ARISTA_GET_BGP_VRF = "show ip bgp summary vrf {} | json"
ARISTA_GET_VRF = "show vrf | json"
ARISTA_GET_LLDP = "show lldp neighbors detail | json"
ARISTA_GET_OSPF = "show ip ospf neighbor detail | json"
ARISTA_GET_OSPF_RID = "show ip ospf | json"
ARISTA_GET_OSPF_VRF = "show ip ospf neighbor detail vrf {} | json"
ARISTA_GET_OSPF_RID_VRF = "show ip ospf vrf {} | json"
ARISTA_GET_IPV4 = "show ip int | json"
ARISTA_GET_STATIC = "show ip route static | json"
ARISTA_GET_STATIC_VRF = "show ip route vrf {} static | json"
ARISTA_GET_INFOS = "show version | json"
ARISTA_GET_INT = "show interfaces status | json"
ARISTA_GET_DOMAIN = "show hostname | json"

##### EXTREME VSP COMMANDS
EXTREME_VSP_GET_BGP = 'show ip bgp summary'
EXTREME_VSP_GET_BGP_VRF = "show ip bgp summary vrf {}"
EXTREME_VSP_GET_VRF = "show ip vrf"
EXTREME_VSP_GET_LLDP = "show lldp neighbor"
EXTREME_VSP_GET_OSPF = "show ip ospf neighbor"
EXTREME_VSP_GET_OSPF_RID = "show ip ospf"
EXTREME_VSP_GET_OSPF_VRF = "show ip ospf neighbor vrf {}"
EXTREME_VSP_GET_OSPF_RID_VRF = "show ip ospf vrf {}"
EXTREME_VSP_GET_IPV4 = "show ip interface"
EXTREME_VSP_GET_IPV4_VRF = "show ip interface vrf {}"
EXTREME_VSP_GET_STATIC = "show ip route static"
EXTREME_VSP_GET_STATIC_VRF = "show ip route static vrf {}"
EXTREME_VSP_GET_INFOS = "show tech"
EXTREME_VSP_GET_SNMP = "show snmp-server host"
EXTREME_VSP_GET_DOMAIN = "show sys dns"
EXTREME_VSP_GET_INT = "show interfaces gigabitEthernet name"

##### CISCO IOS
IOS_GET_INFOS = "show version"
IOS_GET_SNMP = "show snmp"
IOS_GET_INT = "show ip interface brief"

##### BGP CONSTANTES
BGP_SESSIONS_HOST_KEY = 'bgp_sessions'
BGP_WORKS_KEY = 'bgp_works'
BGP_ALL_BGP_UP_KEY = 'bgp_all_up'

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
PING_WORKS_KEY = 'ping_works'

##### LLDP CONSTANTES
LLDP_DATA_HOST_KEY = 'lldp_data'
LLDP_WORKS_KEY = 'lldp_works'

##### CDP CONSTANTES
CDP_DATA_HOST_KEY = 'cdp_data'
CDP_WORKS_KEY = 'cdp_works'

##### IPv4 CONSTANTES
IPV4_DATA_HOST_KEY = 'ipv4_data'
IPV4_WORKS_KEY = 'ipv4_works'

##### STATIC CONSTANTES
STATIC_DATA_HOST_KEY = "static_data"
STATIC_WORKS_KEY = "static_works"

##### INFOS / FACTS CONST
INFOS_DATA_HOST_KEY = "infos_data"
INFOS_WORKS_KEY = "infos_works"
INFOS_SYS_DICT_KEY = "get_infos_sys"
INFOS_SNMP_DICT_KEY = "get_infos_snmp"
INFOS_INT_DICT_KEY = "get_infos_int"
INFOS_DOMAIN_DICT_KEY = "get_infos_domain"
INFOS_MEMORY_DICT_KEY = "get_infos_memory"
INFOS_CONFIG_DICT_KEY = "get_infos_config"
INFOS_SERIAL_DICT_KEY = "get_infos_serial"