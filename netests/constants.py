#!/usr/bin/env python3
# -*- coding: utf-8 -*-

NOT_SET = 'NOT_SET'
NORNIR_DEBUG_MODE = 'debug'
EXIT_FAILURE = 1
EXIT_SUCCESS = 0

NETMIKO_NAPALM_MAPPING_PLATEFORM = {
    'ios': 'cisco_ios',
    'nxos': 'cisco_nxos',
    'eos': 'arista_eos',
    'junos': 'juniper_junos',
    'iosxr': 'cisco_xr'
}

NETCONF_CONNECTION = "netconf"
SSH_CONNECTION = "ssh"
API_CONNECTION = "api"
NAPALM_CONNECTION = "napalm"
CONNEXION_MODE = [
    NETCONF_CONNECTION,
    SSH_CONNECTION,
    API_CONNECTION,
    NAPALM_CONNECTION
]
NETCONF_FILTER = "<filter>{}</filter>"

# CONFIG FILE
NETESTS_CONFIG = "netests.yml"

# REPORT PATH
DATA_MODELS_PATH = "netests/data_models/"
REPORT_FOLDER = "reports/"
TEMPLATES_PATH = "netests/templates/"
TESTS_PATH = "tests/"
FEATURES_PATH = f"{TESTS_PATH}features/"
FEATURES_SRC_PATH = f"{FEATURES_PATH}src/"
FEATURES_OUTPUT_PATH = f"{FEATURES_SRC_PATH}outputs/"
TEXTFSM_PATH = f"{TEMPLATES_PATH}textfsm/"
JINJA2_PATH = f"{TEMPLATES_PATH}jinja2/"
JINJA2_PING_PATH = f"{JINJA2_PATH}ping/"
JINJA2_PING_RESULT = f"{JINJA2_PING_PATH}result/"
JINJA2_SOCKET_PATH = f"{JINJA2_PATH}socket/"
JINJA2_SOCKET_RESULT = f"{JINJA2_SOCKET_PATH}result/"

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
PLATFORM_SUPPORTED = [
    ARISTA_PLATEFORM_NAME,
    CUMULUS_PLATEFORM_NAME,
    EXTREME_PLATEFORM_NAME,
    CISCO_IOS_PLATEFORM_NAME,
    CISCO_IOSXR_PLATEFORM_NAME,
    JUNOS_PLATEFORM_NAME,
    NEXUS_PLATEFORM_NAME
]

# JUNOS COMMANDS
JUNOS_GET_FACTS = "show version | display json"
JUNOS_GET_IPV4 = JUNOS_GET_INT = "show interfaces terse | display json"
JUNOS_GET_MEMORY = "show system memory | display json"
JUNOS_GET_CONFIG_SYSTEM = "show configuration system | display json"
JUNOS_GET_SERIAL = "show chassis hardware detail | display json"
JUNOS_GET_BGP = "show bgp neighbor exact-instance master | display json"
JUNOS_GET_BGP_RID = "show route instance master detail | display json"
JUNOS_GET_BGP_VRF = "show bgp neighbor exact-instance {} | display json"
JUNOS_GET_BGP_VRF_RID = "show route instance {} detail | display json"
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
CUMULUS_API_GET_BGP = 'show bgp summary json'
CUMULUS_GET_BGP_VRF = "net show bgp vrf {} summary json"
CUMULUS_API_GET_BGP_VRF = "show bgp vrf {} summary json"
CUMULUS_GET_VRF = "net show vrf"
CUMULUS_API_GET_VRF = "show vrf"
CUMULUS_GET_LLDP_CDP = "net show lldp json"
CUMULUS_API_GET_LLDP_CDP = "show lldp json"
CUMULUS_GET_OSPF = "net show ospf neighbor detail json"
CUMULUS_API_GET_OSPF = "show ospf neighbor detail json"
CUMULUS_GET_OSPF_VRF = "net show ospf vrf {} neighbor detail json"
CUMULUS_API_GET_OSPF_VRF = "show ospf vrf {} neighbor detail json"
CUMULUS_GET_OSPF_RID = "net show ospf json"
CUMULUS_API_GET_OSPF_RID = "show ospf json"
CUMULUS_GET_OSPF_RID_VRF = "net show ospf vrf {} json"
CUMULUS_API_GET_OSPF_RID_VRF = "show ospf vrf {} json"
CUMULUS_API_GET_INT = "show interface all json"
CUMULUS_GET_INT = "net show interface all json"
CUMULUS_GET_IPV4 = "net show interface json"
CUMULUS_GET_IPV6 = CUMULUS_GET_IPV4
CUMULUS_GET_STATIC = "net show route static json"
CUMULUS_GET_STATIC_VRF = "net show route vrf {} static json"
CUMULUS_GET_FACTS = "net show system json"
CUMULUS_API_GET_FACTS = "show system json"
CUMULUS_GET_FACTS = "net show system json"
CUMULUS_GET_SNMP = "net show snmp-server status json"
CUMULUS_GET_MTU = "net show interface all json"
CUMULUS_GET_MLAG = "net show clag json"
CUMULUS_GET_VLAN_VRF = "net show vrf list"
CUMULUS_GET_VLAN = "net show interface json"
CUMULUS_API_GET_VLAN = "show interface json"
CUMULUS_GET_VLAN_MEM = "net show bridge vlan json"
CUMULUS_GET_BOND = "net show interface bonds json"

# NEXUS COMMANDS
NEXUS_GET_BGP = 'show bgp sessions | json'
NEXUS_API_GET_BGP = 'show bgp sessions'
NEXUS_GET_BGP_VRF = "show bgp sessions vrf {} | json"
NEXUS_API_GET_BGP_VRF = "show bgp sessions vrf {}"
NEXUS_GET_VRF = "show vrf all detail | json"
NEXUS_API_GET_VRF = "show vrf all detail"
NEXUS_GET_LLDP = "show lldp neighbors detail | json"
NEXUS_API_GET_LLDP = "show lldp neighbors detail"
NEXUS_GET_CDP = "show cdp neighbors detail | json"
NEXUS_API_GET_CDP = "show cdp neighbors detail"
NEXUS_GET_OSPF = "show ip ospf neighbors detail | json"
NEXUS_GET_OSPF_VRF = "show ip ospf neighbors vrf {} | json"
NEXUS_GET_OSPF_RID = "show ip ospf | json"
NEXUS_GET_OSPF_RID_VRF = "show ip ospf vrf {} | json"
NEXUS_API_GET_OSPF = "show ip ospf neighbors detail"
NEXUS_API_GET_OSPF_VRF = "show ip ospf neighbors vrf {}"
NEXUS_API_GET_OSPF_RID = "show ip ospf"
NEXUS_API_GET_OSPF_RID_VRF = "show ip ospf vrf {}"
NEXUS_GET_IPV4 = "show ip int | json"
NEXUS_GET_IPV4_VRF = "show ip int vrf {} | json"
NEXUS_GET_STATIC = "show ip route static | json"
NEXUS_GET_STATIC_VRF = "show ip route static  vrf {} | json"
NEXUS_GET_FACTS = "show version | json"
NEXUS_API_GET_FACTS = "show version"
NEXUS_GET_INT = "show interface brief | json"
NEXUS_API_GET_INT = "show interface brief"
NEXUS_GET_SNMP = "show snmp host | json"
NEXUS_GET_DOMAIN = "show hostname | json"
NEXUS_API_GET_DOMAIN = "show hostname"
NEXUS_GET_MTU = "show interface | json"

# ARISTA COMMANDS
ARISTA_GET_BGP = 'show ip bgp summary | json'
ARISTA_API_GET_BGP = 'show ip bgp summary'
ARISTA_GET_BGP_VRF = "show ip bgp summary vrf {} | json"
ARISTA_API_GET_BGP_VRF = "show ip bgp summary vrf {}"
ARISTA_GET_VRF = "show vrf | json"
ARISTA_GET_LLDP = "show lldp neighbors detail | json"
ARISTA_GET_OSPF = "show ip ospf neighbor detail vrf default | json"
ARISTA_GET_OSPF_RID = "show ip ospf vrf default | json"
ARISTA_GET_OSPF_VRF = "show ip ospf neighbor detail vrf {} | json"
ARISTA_GET_OSPF_RID_VRF = "show ip ospf vrf {} | json"
ARISTA_API_GET_OSPF = "show ip ospf neighbor detail vrf default"
ARISTA_API_GET_OSPF_RID = "show ip ospf vrf default"
ARISTA_API_GET_OSPF_VRF = "show ip ospf neighbor detail vrf {}"
ARISTA_API_GET_OSPF_RID_VRF = "show ip ospf vrf {}"
ARISTA_GET_IPV4 = "show ip int | json"
ARISTA_GET_STATIC = "show ip route static | json"
ARISTA_GET_STATIC_VRF = "show ip route vrf {} static | json"
ARISTA_GET_FACTS = "show version | json"
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
EXTREME_VSP_GET_FACTS = "show tech"
EXTREME_VSP_GET_SNMP = "show snmp-server host"
EXTREME_VSP_GET_DOMAIN = "show sys dns"
EXTREME_VSP_GET_INT = "show interfaces gigabitEthernet name"
EXTREME_VSP_GET_MTU = "show interfaces gigabitEthernet"

# CISCO IOS
IOS_GET_FACTS = "show version"
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
IOSXR_GET_VRF = "show vrf all detail"
IOSXR_GET_BGP_PEERS = "show bgp neighbors"
IOSXR_GET_BGP_RID = "show bgp summary"
IOSXR_VRF_GET_BGP_PEERS = "show bgp vrf {} neighbors"
IOSXR_VRF_GET_BGP_RID = "show bgp vrf {} summary"
IOSXR_GET_FACTS = "show version"
IOSXR_GET_INT = "show ip interface brief"
IOSXR_GET_LLDP = "show lldp neighbors"
IOSXR_GET_CDP = "show cdp neighbors detail"

# BGP CONSTANTES
BGP_SESSIONS_HOST_KEY = 'bgp_sessions'
BGP_WORKS_KEY = 'bgp_works'
BGP_ALL_BGP_UP_KEY = 'bgp_all_up'
BGP_UPTIME_FORMAT_MS = "msec"
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

# FACTS CONST
FACTS_DATA_HOST_KEY = "infos_data"
FACTS_WORKS_KEY = "infos_works"
FACTS_SYS_DICT_KEY = "get_infos_sys"
FACTS_SNMP_DICT_KEY = "get_infos_snmp"
FACTS_INT_DICT_KEY = "get_infos_int"
FACTS_DOMAIN_DICT_KEY = "get_infos_domain"
FACTS_MEMORY_DICT_KEY = "get_infos_memory"
FACTS_CONFIG_DICT_KEY = "get_infos_config"
FACTS_SERIAL_DICT_KEY = "get_infos_serial"

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
