#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import pprint
PP = pprint.PrettyPrinter(indent=4)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)
NOT_SET = "NOT_SET"

# VERBOSE MODE VALUES
LEVEL0 = "level0"
LEVEL1 = "level1"
LEVEL2 = "level2"
LEVEL3 = "level3"
LEVEL4 = "level4"
LEVEL5 = "level5"

NETMIKO_NAPALM_MAPPING_PLATEFORM = {
    'ios': 'cisco_ios',
    'nxos': 'cisco_nxos',
    'eos': 'arista_eos',
    'junos': 'juniper_junos',
    'iosxr': 'cisco_xr'
}

# CONNEXION MODE
NETCONF_CONNECTION = "netconf"
SSH_CONNECTION = "ssh"
API_CONNECTION = "api"
NAPALM_CONNECTION = "napalm"

NETCONF_FILTER = "<filter>{}</filter>"

# REPORT PATH
REPORT_FOLDER = "reports/"
TEMPLATES_PATH = "templates/"
FEATURES_PATH = "features/"
FEATURES_SRC_PATH = f"{FEATURES_PATH}src/"
FEATURES_OUTPUT_PATH = f"{FEATURES_SRC_PATH}outputs/"
TEXTFSM_PATH = f"{TEMPLATES_PATH}textfsm/"
JINJA2_PATH = f"{TEMPLATES_PATH}jinja2/"
JINJA2_PING_PATH = f"{JINJA2_PATH}ping/"
JINJA2_PING_RESULT = f"{JINJA2_PING_PATH}result/"
JINJA2_SOCKET_PATH = f"{JINJA2_PATH}socket/"
JINJA2_SOCKET_RESULT = f"{JINJA2_SOCKET_PATH}result/"

# NORNIR INIT
NORNIR_DEBUG_MODE = 'debug'

PATH_TO_VERITY_FILES = "./verity/"
PATH_TO_INVENTORY_FILES = "./inventory/"

# INVENTORY
ANSIBLE_INVENTORY = "hosts"
ANSIBLE_INVENTORY_VIRTUAL = "hosts_virtual"

NAPALM_COMPATIBLE_PLATEFORM = [
    'junos', 'cisco_nxos', 'nxos',
    'cisco_ios', 'ios', 'iosxr',
    'cisco_iosxr', 'arista_eos', 'eos'
]
JUNOS_PLATEFORM_NAME = 'junos'
CUMULUS_PLATEFORM_NAME = 'linux'
NEXUS_PLATEFORM_NAME = 'nxos'
CISCO_IOS_PLATEFORM_NAME = 'ios'
CISCO_IOSXR_PLATEFORM_NAME = 'iosxr'
ARISTA_PLATEFORM_NAME = 'eos'
EXTREME_PLATEFORM_NAME = 'extreme_vsp'

# TESTS TO EXECUTE FILE
TEST_TO_EXECUTE_FILENAME = "_test_to_execute.yml"
TO_EXECUTE_FILE_VALUE = ['INFO', 'TRUE', 'FALSE']
YAML_BGKP_ASN_KEY = 'asn'
BGP_SRC_FILENAME = "bgp.yml"
VRF_SRC_FILENAME = "vrf.yml"
PING_SRC_FILENAME = "ping.yml"
SOCKET_SRC_FILENAME = "socket.yml"
LLDP_SRC_FILENAME = "lldp.yml"
CDP_SRC_FILENAME = "cdp.yml"
OSPF_SRC_FILENAME = "ospf.yml"
IPV4_SRC_FILENAME = "ipv4.yml"
IPV6_SRC_FILENAME = "ipv6.yml"
MLAG_SRC_FILENAME = "mlag.yml"
STATIC_SRC_FILENAME = "static.yml"
INFOS_SRC_FILENAME = "sys_infos.yml"
MTU_SRC_FILENAME = "mtu.yml"
L2VNI_SRC_FILENAME = "l2vni.yml"
VLAN_SRC_FILENAME = "vlan.yml"
BOND_SRC_FILENAME = "bond.yml"
TEST_TO_EXC_BGP_KEY = 'bgp'
TEST_TO_EXC_BGP_UP_KEY = 'bgp_all_up'
TEST_TO_EXC_VRF_KEY = 'vrf'
TEST_TO_EXC_PING_KEY = 'ping'
TEST_TO_EXC_SOCKET_KEY = 'socket'
TEST_TO_EXC_LLDP_KEY = 'lldp'
TEST_TO_EXC_CDP_KEY = 'cdp'
TEST_TO_EXC_OSPF_KEY = 'ospf'
TEST_TO_EXC_IPV4_KEY = 'ipv4'
TEST_TO_EXC_IPV6_KEY = 'ipv6'
TEST_TO_EXC_STATIC_KEY = 'static'
TEST_TO_EXC_INFOS_KEY = 'sys_infos'
TEST_TO_EXC_MTU_KEY = "mtu"
TEST_TO_EXC_MLAG_KEY = "mlag"
TEST_TO_EXC_L2VNI_KEY = "l2vni"
TEST_TO_EXC_VLAN_KEY = "vlan"
TEST_TO_EXC_BOND_KEY = "bond"

YAML_ALL_GROUPS_KEY = 'all'
YAML_GROUPS_KEY = 'groups'
YAML_DEVICES_KEY = 'devices'

# JUNOS COMMANDS
JUNOS_GET_INFOS = "show version | display json"
JUNOS_GET_IPV4 = JUNOS_GET_INT = "show interfaces brief | display json"
JUNOS_GET_MEMORY = "show system memory | display json"
JUNOS_GET_CONFIG_SYSTEM = "show configuration system | display json"
JUNOS_GET_SERIAL = "show chassis hardware detail | display json"
JUNOS_GET_BGP = "show bgp neighbor exact-instance master | display json"
JUNOS_GET_BGP_RID = (
    "show configuration routing-options router-id "
    "| display json"
)
JUNOS_GET_BGP_VRF = "show bgp neighbor exact-instance {} | display json"
JUNOS_GET_BGP_VRF_RID = (
    "show configuration routing-instances {} "
    "routing-options router-id | display json"
)
JUNOS_GET_VRF_DETAIL = "show route instance detail | display json"
JUNOS_GET_VRF = "show route instance | display json"
JUNOS_GET_MTU = "show interfaces | display json"
JUNOS_GET_OSPF_NEI = "show ospf neighbor detail | display json"
JUNOS_GET_OSPF_NEI_VRF = "show ospf neighbor detail instance {} | display json"
JUNOS_GET_OSPF_RID = "show ospf overview | display json"
JUNOS_GET_OSPF_RID_VRF = "show ospf overview instance {} | display json"
JUNOS_GET_STATIC = "show route protocol static | display json"
JUNOS_GET_LLDP = "show lldp neighbors | display json"

# CUMULUS COMMANDS
CUMULUS_GET_BGP = 'net show bgp summary json'
CUMULUS_GET_BGP_VRF = "net show bgp vrf {} summary json"
CUMULUS_GET_VRF = "net show bgp vrf"
CUMULUS_GET_LLDP_CDP = "net show lldp json"
CUMULUS_GET_OSPF = "net show ospf neighbor detail json"
CUMULUS_GET_OSPF_VRF = "net show ospf vrf {} neighbor detail json"
CUMULUS_GET_OSPF_RID = "net show ospf json"
CUMULUS_GET_OSPF_RID_VRF = "net show ospf vrf {} json"
CUMULUS_GET_IPV4 = "net show interface json"
CUMULUS_GET_IPV6 = CUMULUS_GET_IPV4
CUMULUS_GET_STATIC = "net show route static json"
CUMULUS_GET_STATIC_VRF = "net show route vrf {} static json"
CUMULUS_GET_INFOS = "net show system json"
CUMULUS_GET_SNMP = "net show snmp-server status json"
CUMULUS_GET_MTU = "net show interface all json"
CUMULUS_GET_MLAG = "net show clag json"
CUMULUS_GET_VLAN_VRF = "net show vrf list"
CUMULUS_GET_VLAN = "net show interface json"
CUMULUS_GET_VLAN_MEM = "net show bridge vlan json"
CUMULUS_GET_BOND = "net show interface bonds json"

# NEXUS COMMANDS
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
NEXUS_GET_MTU = "show interface | json"

# ARISTA COMMANDS
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
ARISTA_GET_MTU = "show interfaces | json"
ARISTA_GET_INT_VLAN = "show interfaces vlan 1-4094 | json"
ARISTA_GET_VLAN = "show vlan | json"
ARISTA_GET_IP_VLAN = "show ip interface vlan 1-4094 | json"
ARISTA_GET_IPV6 = "show ipv6 interface | json"

# EXTREME VSP COMMANDS
EXTREME_VSP_GET_BGP = 'show ip bgp summary'
EXTREME_VSP_GET_BGP_VRF = "show ip bgp summary vrf {}"
EXTREME_VSP_GET_VRF = "show ip vrf"
EXTREME_VSP_GET_LLDP = "show lldp neighbor"
EXTREME_VSP_GET_OSPF = "show ip ospf neighbor"
EXTREME_VSP_GET_OSPF_INTERFACES = "show ip ospf interface"
EXTREME_VSP_GET_OSPF_RID = "show ip ospf"
EXTREME_VSP_GET_OSPF_VRF = "show ip ospf neighbor vrf {}"
EXTREME_VSP_GET_OSPF_RID_VRF = "show ip ospf vrf {}"
EXTREME_VSP_GET_OSPF_INTERFACES_VRF = "show ip ospf interface vrf {}"
EXTREME_VSP_GET_IPV4 = "show ip interface"
EXTREME_VSP_GET_IPV4_VRF = "show ip interface vrf {}"
EXTREME_VSP_GET_STATIC = "show ip route static"
EXTREME_VSP_GET_STATIC_VRF = "show ip route static vrf {}"
EXTREME_VSP_GET_INFOS = "show tech"
EXTREME_VSP_GET_SNMP = "show snmp-server host"
EXTREME_VSP_GET_DOMAIN = "show sys dns"
EXTREME_VSP_GET_INT = "show interfaces gigabitEthernet name"
EXTREME_VSP_GET_MTU = "show interfaces gigabitEthernet"

# CISCO IOS
IOS_GET_INFOS = "show version"
IOS_GET_SNMP = "show snmp"
IOS_GET_INT = "show ip interface brief"
IOS_GET_VRF = "show vrf detail"
IOS_GET_LLDP = "show lldp neighbors detail"
IOS_GET_CDP = "show cdp neighbors detail"
IOS_GET_BGP = "show ip bgp summary"
IOS_GET_BGP_VRF = "show bgp vrf {} all summary"
IOS_GET_STATIC = "show ip route static"
IOS_GET_STATIC_VRF = "show ip route vrf {} static"
IOS_GET_IPV4_BRIEF = "show ip int brief"
IOS_GET_IPV4 = "show ip interface"
IOS_GET_MTU = "show interface"
IOS_GET_OSPF = "show ip ospf"
IOS_GET_OSPF_NEI = "show ip ospf neighbor detail"
IOS_GET_OSPF_INT = "show ip ospf interface brief"

# CISCO IOSXR
IOSXR_GET_VRF = "show vrf detail"

# BGP CONSTANTES
BGP_SESSIONS_HOST_KEY = 'bgp_sessions'
BGP_WORKS_KEY = 'bgp_works'
BGP_ALL_BGP_UP_KEY = 'bgp_all_up'

BGP_STATE_UP_LIST = [
    'ESTABLISHED', 'established', 'Established', 'Estab', 'UP', 'up', 'Up'
]
BGP_STATE_BRIEF_UP = "UP"
BGP_STATE_BRIEF_DOWN = "DOWN"

# OSPF CONSTANTES
OSPF_SESSIONS_HOST_KEY = 'ospf_sessions'
OSPF_WORKS_KEY = 'ospf_works'
OSPF_RIB_KEY = 'ospf'
OSPF_INT_NAME_KEY = 'int_name'
OSPF_INT_KEY = 'interfaces'
OSPF_NEI_KEY = 'neighbors'

# VRF CONSTANTES
VRF_DATA_KEY = 'vrf_data'
VRF_NAME_DATA_KEY = 'vrf_name_data'
VRF_WORKS_KEY = 'vrf_works'
VRF_DEFAULT_RT_LST = ["default", "global", "GlobalRouter"]

# PING CONSTANTES
PING_DATA_HOST_KEY = 'ping_data'
PING_WORKS_KEY = 'ping_works'

# SOCKET CONSTANTES
SOCKET_DATA_HOST_KEY = "socket_data"
SOCKET_WORKS_KEY = "socket_works"

# LLDP CONSTANTES
LLDP_DATA_HOST_KEY = 'lldp_data'
LLDP_WORKS_KEY = 'lldp_works'

# CDP CONSTANTES
CDP_DATA_HOST_KEY = 'cdp_data'
CDP_WORKS_KEY = 'cdp_works'

# IPv4 CONSTANTES
IPV4_DATA_HOST_KEY = 'ipv4_data'
IPV4_WORKS_KEY = 'ipv4_works'

# IPv6 CONSTANTES
IPV6_DATA_HOST_KEY = 'ipv6_data'
IPV6_WORKS_KEY = 'ipv6_works'

# STATIC CONSTANTES
STATIC_DATA_HOST_KEY = "static_data"
STATIC_WORKS_KEY = "static_works"

# INFOS / FACTS CONST
INFOS_DATA_HOST_KEY = "infos_data"
INFOS_WORKS_KEY = "infos_works"
INFOS_SYS_DICT_KEY = "get_infos_sys"
INFOS_SNMP_DICT_KEY = "get_infos_snmp"
INFOS_INT_DICT_KEY = "get_infos_int"
INFOS_DOMAIN_DICT_KEY = "get_infos_domain"
INFOS_MEMORY_DICT_KEY = "get_infos_memory"
INFOS_CONFIG_DICT_KEY = "get_infos_config"
INFOS_SERIAL_DICT_KEY = "get_infos_serial"

# MTU
MTU_DATA_HOST_KEY = "mtu_data"
MTU_WORKS_HOST_KEY = "mtu_works"
MTU_INTER_YAML_KEY = "interfaces"
MTU_GLOBAL_YAML_KEY = "global_mtu"

# MLAG
MLAG_DATA_HOST_KEY = "mlag_data"
MLAG_WORKS_KEY = "mlag_works"

# L2VNI
L2VNI_DATA_HOST_KEY = "l2vni_data"
L2VNI_WORKS_KEY = "l2vni_works"

# VLAN
VLAN_DATA_HOST_KEY = "vlan_data"
VLAN_WORKS_KEY = "vlan_works"
VLAN_VRF_LIST_KEY = "get_vlan_vrf"
VLAN_VRF_DETAIL_KEY = "get_vlan_detail"
VLAN_VRF_MEMBERS_KEY = "get_vlan_members"
VLAN_GET_L2 = "get_vlan_l2"
VLAN_GET_L3 = "get_vlan_l3"
VLAN_GET_INT = "get_vlan_int"

# BOND
BOND_DATA_HOST_KEY = "bond_data"
BOND_WORKS_KEY = "bond_works"
BOND_DATA_LIST_KEY = "bond_data_list"
