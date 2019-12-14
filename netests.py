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
# Constantes
#
ERROR_HEADER = "Error import [main.py]"
HEADER = "[netests - main.py]"
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
    from functions.global_tools import *
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.global_tools")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.vlan.vlan_compare import compare_vlan
    from functions.vlan.vlan_get import get_vlan
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.vlan")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.l2vni.l2vni_compare import compare_l2vni
    from functions.l2vni.l2vni_get import get_l2vni
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.l2vni")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.mlag.mlag_compare import compare_mlag
    from functions.mlag.mlag_get import get_mlag
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.mlag")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.mtu.mtu_compare import compare_mtu
    from functions.mtu.mtu_get import get_mtu
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.mtu")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.infos.infos_compare import compare_infos
    from functions.infos.infos_get import get_infos
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.infos")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.static.static_get import get_static
    from functions.static.static_compare import *
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.static")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.ip.ipv6.ipv6_get import *
    from functions.ip.ipv6.ipv6_compare import compare_ipv6
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.ip.ipv6")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.ip.ipv4.ipv4_get import *
    from functions.ip.ipv4.ipv4_compare import compare_ipv4
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.ip.ipv4")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.ospf.ospf_gets import *
    from functions.ospf.ospf_compare import compare_ospf
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.ospf")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.discovery_protocols.cdp.get_cdp import *
    from functions.discovery_protocols.cdp.cdp_compare import compare_cdp
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.discovery_protocols.cdp")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.discovery_protocols.lldp.get_lldp import *
    from functions.discovery_protocols.lldp.lldp_compare import compare_lldp
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.discovery_protocols.lldp")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.ping.execute_ping import *
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.ping")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.socket.execute_socket import *
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.socket")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.vrf.vrf_compare import *
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.vrf")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.bgp.bgp_compare import *
    from functions.bgp.bgp_reports import *
    from functions.bgp.bgp_gets import *
    from functions.bgp.bgp_checks import get_bgp_up
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.bgp")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from nornir import InitNornir
    from nornir.core import Nornir
    from nornir.plugins.connections.netmiko import Netmiko
except ImportError as importError:
    print(f"{ERROR_HEADER} nornir")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from netmiko import ConnectHandler
except ImportError as importError:
    print(f"{ERROR_HEADER} netmiko")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import click
except ImportError as importError:
    print(f"{ERROR_HEADER} click")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import yaml
except ImportError as importError:
    print(f"{ERROR_HEADER} yaml")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import urllib3
except ImportError as importError:
    print(f"{ERROR_HEADER} urllib3")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# Functions
#
def init_nornir(log_file="./nornir/nornir.log", log_level=NORNIR_DEBUG_MODE,
                ansible=False, virtual=False, netbox=False) -> Nornir:
    """
    Initialize Nornir object with the following files
    """

    config_file = str()
    if netbox:
        config_file = "./nornir/config_netbox.yml"
    elif ansible:
        if virtual:
            config_file= "./nornir/config_ansible_virt.yml"
        else:
            config_file="./nornir/config_ansible.yml"
    else:
        if virtual:
            config_file="./nornir/config_std_virt.yml"
        else:
            config_file="./nornir/config_std.yml"

    nr = InitNornir(
        config_file=config_file,
        logging={
            "file": log_file,
            "level": log_level
        }
    )

    return nr

# ----------------------------------------------------------------------------------------------------------------------
#
# Get level test function
#
def _get_level_test(level_value: int) -> int:

    if level_value != 1 and level_value != 2:
        return 0
    else:
        return level_value

# ----------------------------------------------------------------------------------------------------------------------
#
# Test devices connectivity function
#
def _check_connectivity(nr: Nornir) -> bool:
    """
    This function will test the connectivity to each devices

    :param nr:
    :return bool: True if ALL devices are reachable
    """

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=is_alive,
        num_workers=100
    )
    #print_result(data)

    for device in devices.inventory.hosts:
        if data[device].failed:
            print(f"\t--> Connection to {device} has failed.")

    if not data.failed:
        print("All devices are reachable :) !")
    else:
        print(f"\nPlease check credentials in the inventory")

    printline()
    return not data.failed

# ----------------------------------------------------------------------------------------------------------------------
#
# Test devices connectivity Nornir function
#
def is_alive(task) -> None:
    """
    This function will use Netmiko find_prompt() function to test connectivity
    :param task:
    :return None:
    """

    if task.host.platform in NETMIKO_NAPALM_MAPPING_PLATEFORM.keys():
        plateform = NETMIKO_NAPALM_MAPPING_PLATEFORM.get(task.host.platform)
    else:
        plateform = task.host.platform

    device = ConnectHandler(
        device_type=plateform,
        host=task.host.hostname,
        username=task.host.username,
        password=task.host.password
    )

    device.find_prompt()

########################################################################################################################
#
# Main function
#
@click.command()
@click.option('--ansible', default=False, help=f"If TRUE, inventory file {PATH_TO_INVENTORY_FILES}{ANSIBLE_INVENTORY}")
@click.option('--virtual', default=False, help=f"If TRUE, inventory file {PATH_TO_INVENTORY_FILES}{ANSIBLE_INVENTORY_VIRTUAL}")
@click.option('--netbox', default=False, help=f"If TRUE, inventory file {PATH_TO_INVENTORY_FILES}{ANSIBLE_INVENTORY_VIRTUAL}")
@click.option('--reports', default=False, help=f"If TRUE, configuration reports will be create")
@click.option('--verbose', default=False, help=f"If TRUE, print fome information about inventory")
@click.option('--check-connectivity', default=False, help=f"If TRUE, check if devices are reachable")
def main(ansible, virtual, netbox, reports, verbose, check_connectivity):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Create Nornir object
    nr = init_nornir(
        log_file="./nornir/nornir.log",
        log_level="debug",
        ansible=ansible,
        virtual=virtual,
        netbox=netbox
    )


    printline_comment_json(
        comment="Devices selected",
        json_to_print=nr.inventory.hosts
    )

    if verbose:
        for host in nr.inventory.hosts:
            print(nr.inventory.hosts[host].data)
            print(nr.inventory.hosts[host].username)
            print(nr.inventory.hosts[host].password)
            print(nr.inventory.hosts[host].hostname)
            print(nr.inventory.hosts[host].port)

    if check_connectivity:
        if _check_connectivity(nr):
            exit(EXIT_SUCCESS)
        else:
            exit(EXIT_FAILURE)

    test_to_execute = open_file(PATH_TO_VERITY_FILES+TEST_TO_EXECUTE_FILENAME)

    # ''''''''''''''''''''''''''''''''''''''''''''
    # 0. Check BGP sessions
    # ''''''''''''''''''''''''''''''''''''''''''''
    if test_to_execute[TEST_TO_EXC_BGP_KEY] is True:
        get_bgp(nr)
        bgp_data = open_file(f"{PATH_TO_VERITY_FILES}{BGP_SRC_FILENAME}")
        same = compare_bgp(nr, bgp_data)
        if reports:
            create_reports(nr, bgp_data)
        if test_to_execute[TEST_TO_EXC_BGP_KEY] is True and same is False:
            exit_value = False
        print(
            f"{HEADER} BGP sessions are the same that defined in {PATH_TO_VERITY_FILES}{BGP_SRC_FILENAME} = {same} !!")
    else:
        print(f"{HEADER} BGP_SESSIONS tests are not executed !!")

    # ''''''''''''''''''''''''''''''''''''''''''''
    # 1. Check all BGP sessions UP
    # ''''''''''''''''''''''''''''''''''''''''''''
    if test_to_execute[TEST_TO_EXC_BGP_UP_KEY] is True:

        works = get_bgp_up(nr)

        if reports:
            create_reports(nr, bgp_data)
        if test_to_execute[TEST_TO_EXC_BGP_UP_KEY] is True and works is False:
            exit_value = False
        print(
            f"{HEADER} All BGP sessions on devices are UP = {works} !!")
    else:
        print(f"{HEADER} All BGP sessions tests are not executed !!")

    # ''''''''''''''''''''''''''''''''''''''''''''
    # 2. LLDP Neighbors check
    # ''''''''''''''''''''''''''''''''''''''''''''
    if TEST_TO_EXC_LLDP_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_LLDP_KEY] is True:
            get_lldp(nr)
            lldp_data = open_file(f"{PATH_TO_VERITY_FILES}{LLDP_SRC_FILENAME}")
            same = compare_lldp(nr, lldp_data)
            if test_to_execute[TEST_TO_EXC_LLDP_KEY] is True and same is False:
                exit_value = False
            print(
                f"{HEADER} LLDP sessions are the same that defined in {PATH_TO_VERITY_FILES}{LLDP_SRC_FILENAME} = {same} !!")
        else:
            print(f"{HEADER} LLDP sessions tests are not executed !!")
    else:
        print(f"{HEADER} LLDP sessions key is not defined in {PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!")


    # ''''''''''''''''''''''''''''''''''''''''''''
    # 3. CDP Neighbors check
    # ''''''''''''''''''''''''''''''''''''''''''''
    if TEST_TO_EXC_CDP_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_CDP_KEY] is True:
            get_cdp(nr)
            cdp_data = open_file(f"{PATH_TO_VERITY_FILES}{CDP_SRC_FILENAME}")
            same = compare_cdp(nr, cdp_data)
            if test_to_execute[TEST_TO_EXC_CDP_KEY] is True and same is False:
                exit_value = False
            print(
                f"{HEADER} CDP sessions are the same that defined in {PATH_TO_VERITY_FILES}{CDP_SRC_FILENAME} = {same} !!")
        else:
            print(f"{HEADER} CDP sessions tests are not executed !!")
    else:
        print(f"{HEADER} CDP sessions key is not defined in {PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!")

    # ''''''''''''''''''''''''''''''''''''''''''''
    # 4. Check VRF on devices
    # ''''''''''''''''''''''''''''''''''''''''''''
    if TEST_TO_EXC_VRF_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_VRF_KEY] is True:
            get_vrf(nr)
            vrf_data = open_file(f"{PATH_TO_VERITY_FILES}{VRF_SRC_FILENAME}")
            same = compare_vrf(nr, vrf_data)
            if test_to_execute[TEST_TO_EXC_VRF_KEY] is True and same is False:
                exit_value = False
            print(f"{HEADER} VRF are the same that defined in {PATH_TO_VERITY_FILES}{VRF_SRC_FILENAME} = {same} !!")
        else:
            print(f"{HEADER} VRF tests are not executed !!")
    else:
        print(f"{HEADER} VRF key is not defined in {PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!")

    # ''''''''''''''''''''''''''''''''''''''''''''
    # 5. Execute PING on devices
    # ''''''''''''''''''''''''''''''''''''''''''''
    if TEST_TO_EXC_PING_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_PING_KEY] is True:
            works = execute_ping(nr)
            if test_to_execute[TEST_TO_EXC_PING_KEY] is True and works is False:
                exit_value = False
            print(f"{HEADER} Pings defined in {PATH_TO_VERITY_FILES}{PING_SRC_FILENAME} work = {works} !!")
        else:
            print(f"{HEADER} Pings have not been executed !!")
    else:
        print(f"{HEADER} PING key is not defined in {PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!")


    # ''''''''''''''''''''''''''''''''''''''''''''
    # 6. Check OSPF sessions
    # ''''''''''''''''''''''''''''''''''''''''''''
    if TEST_TO_EXC_OSPF_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_OSPF_KEY].get('test') is True:

            get_ospf(nr)

            ospf_data = open_file(
                path=f"{PATH_TO_VERITY_FILES}{OSPF_SRC_FILENAME}"
            )

            works = compare_ospf(
                nr=nr,
                ospf_data=ospf_data,
                level_test=_get_level_test(
                    level_value=test_to_execute.get(TEST_TO_EXC_OSPF_KEY).get('level', NOT_SET)
                )
            )

            if test_to_execute[TEST_TO_EXC_OSPF_KEY] is True and works is False:
                exit_value = False
            print(f"{HEADER} OSPF sessions defined in {PATH_TO_VERITY_FILES}{OSPF_SRC_FILENAME} work = {works} !!")
        else:
            print(f"{HEADER} OSPF have not been executed !!")
    else:
        print(f"{HEADER} OSPF sessions  key is not defined in {PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!")


    # ''''''''''''''''''''''''''''''''''''''''''''
    # 6. Check IPv4 addresses
    # ''''''''''''''''''''''''''''''''''''''''''''
    if TEST_TO_EXC_IPV4_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_IPV4_KEY].get('test') is True:

            get_ipv4(
                nr=nr,
                get_vlan=test_to_execute.get(TEST_TO_EXC_IPV4_KEY).get("get_vlan", True),
                get_loopback=test_to_execute.get(TEST_TO_EXC_IPV4_KEY).get("get_loopback", True),
                get_peerlink=test_to_execute.get(TEST_TO_EXC_IPV4_KEY).get("get_peerlink", True),
                get_vni=test_to_execute.get(TEST_TO_EXC_IPV4_KEY).get("get_vni", True),
                get_physical=test_to_execute.get(TEST_TO_EXC_IPV4_KEY).get("get_physical", True)
            )

            ipv4_yaml_data = open_file(
                path=f"{PATH_TO_VERITY_FILES}{IPV4_SRC_FILENAME}"
            )
            same = compare_ipv4(nr, ipv4_yaml_data)
            if test_to_execute[TEST_TO_EXC_IPV4_KEY] is True and same is False:
                exit_value = False
            print(f"{HEADER} IPv4 addresses defined in {PATH_TO_VERITY_FILES}{IPV4_SRC_FILENAME} work = {same} !!")
        else:
            print(f"{HEADER} IPv4 addresses have not been executed !!")
    else:
        print(f"{HEADER} IPv4 addresses key is not defined in {PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!")


    # ''''''''''''''''''''''''''''''''''''''''''''
    # 7. Check Static routes
    # ''''''''''''''''''''''''''''''''''''''''''''
    if TEST_TO_EXC_STATIC_KEY in test_to_execute.keys():
        if test_to_execute.get(TEST_TO_EXC_STATIC_KEY).get('test', False) is True:

            get_static(nr)

            same = compare_static(
                nr=nr,
                ansible_vars=test_to_execute.get(TEST_TO_EXC_STATIC_KEY).get('ansible_vars').get('enable', False),
                dict_keys=test_to_execute.get(TEST_TO_EXC_STATIC_KEY).get('ansible_vars').get('dict_keys', False),
                your_keys=test_to_execute.get(TEST_TO_EXC_STATIC_KEY).get('ansible_vars').get('your_keys', False)
            )

            if test_to_execute.get(TEST_TO_EXC_STATIC_KEY).get('test', False) is True and same is False:
                exit_value = False
            print(f"{HEADER} Static routes defined in {PATH_TO_VERITY_FILES}{STATIC_SRC_FILENAME} work = {same} !!")
        else:
            print(f"{HEADER} Static routes have not been executed !!")
    else:
        print(f"{HEADER} Static routes key is not defined in {PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!")

    # ''''''''''''''''''''''''''''''''''''''''''''
    # 8. Check system infos
    # ''''''''''''''''''''''''''''''''''''''''''''
    if TEST_TO_EXC_INFOS_KEY in test_to_execute.keys():
        if test_to_execute.get(TEST_TO_EXC_INFOS_KEY) is True:

            get_infos(nr)
            same = compare_infos(
                nr=nr,
                infos_data=open_file(f"{PATH_TO_VERITY_FILES}{INFOS_SRC_FILENAME}")
            )

            if test_to_execute.get(TEST_TO_EXC_INFOS_KEY) is True and same is False:
                exit_value = False
            print(f"{HEADER} System informations defined in {PATH_TO_VERITY_FILES}{INFOS_SRC_FILENAME} work = {same}!!")
        else:
            print(f"{HEADER} System informations have not been executed !!")
    else:
        print(f"{HEADER} System informations key is not defined in {PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME} !!")


    # ''''''''''''''''''''''''''''''''''''''''''''
    # 9. Check MTU interfaces
    # ''''''''''''''''''''''''''''''''''''''''''''
    if TEST_TO_EXC_MTU_KEY in test_to_execute.keys():
        if test_to_execute.get(TEST_TO_EXC_MTU_KEY) is True:

            get_mtu(nr)
            same = compare_mtu(
                nr=nr,
                mtu_data=open_file(f"{PATH_TO_VERITY_FILES}{MTU_SRC_FILENAME}")
            )

            if test_to_execute.get(TEST_TO_EXC_MTU_KEY) is True and same is False:
                exit_value = False
            print(f"{HEADER} MTU interfaces defined in {PATH_TO_VERITY_FILES}{MTU_SRC_FILENAME} work = {same}!!")
        else:
            print(f"{HEADER} MTU interfaces have not been executed !!")
    else:
        print(f"{HEADER} MTU interfaces key is not defined in {PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME} !!")


    # ''''''''''''''''''''''''''''''''''''''''''''
    # 10. Check MLAG
    # ''''''''''''''''''''''''''''''''''''''''''''
    if TEST_TO_EXC_MLAG_KEY in test_to_execute.keys():
        if test_to_execute.get(TEST_TO_EXC_MLAG_KEY) is True:

            get_mlag(nr)
            same = compare_mlag(
                nr=nr,
                mlag_yaml_data=open_file(f"{PATH_TO_VERITY_FILES}{MLAG_SRC_FILENAME}")
            )

            if test_to_execute.get(TEST_TO_EXC_MLAG_KEY) is True and same is False:
                exit_value = False
            print(f"{HEADER} MLAG defined in {PATH_TO_VERITY_FILES}{MLAG_SRC_FILENAME} work = {same}!!")
        else:
            print(f"{HEADER} MLAG have not been executed !!")
    else:
        print(f"{HEADER} MLAG key is not defined in {PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME} !!")


    # ''''''''''''''''''''''''''''''''''''''''''''
    # 11. Execute Socket
    # ''''''''''''''''''''''''''''''''''''''''''''
    if TEST_TO_EXC_SOCKET_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_SOCKET_KEY] is True:
            same = execute_socket(nr)
            if test_to_execute[TEST_TO_EXC_SOCKET_KEY] is True and same is False:
                exit_value = False
            print(f"{HEADER} Sockets defined in {PATH_TO_VERITY_FILES}{SOCKET_SRC_FILENAME} work = {same} !!")
        else:
            print(f"{HEADER} Sockets have not been executed !!")
    else:
        print(f"{HEADER} SOCKET key is not defined in {PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!")


    # ''''''''''''''''''''''''''''''''''''''''''''
    # 12. Check L2VNI
    # ''''''''''''''''''''''''''''''''''''''''''''
    if TEST_TO_EXC_L2VNI_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_L2VNI_KEY] is True:

            get_l2vni(nr)
            same = compare_l2vni(
                nr=nr,
                l2vni_yaml_data=open_file(f"{PATH_TO_VERITY_FILES}{L2VNI_SRC_FILENAME}")
            )

            if test_to_execute[TEST_TO_EXC_L2VNI_KEY] is True and same is False:
                exit_value = False
            print(f"{HEADER} L2VNI defined in {PATH_TO_VERITY_FILES}{L2VNI_SRC_FILENAME} work = {same} !!")
        else:
            print(f"{HEADER} L2VNI have not been executed !!")
    else:
        print(f"{HEADER} L2VNI key is not defined in {PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!")

    # ''''''''''''''''''''''''''''''''''''''''''''
    # 13. Check VLAN
    # ''''''''''''''''''''''''''''''''''''''''''''
    if TEST_TO_EXC_VLAN_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_VLAN_KEY] is True:

            get_vlan(nr)
            same = compare_vlan(
                nr=nr,
                vlan_yaml_data=open_file(f"{PATH_TO_VERITY_FILES}{VLAN_SRC_FILENAME}")
            )

            if test_to_execute[TEST_TO_EXC_VLAN_KEY] is True and same is False:
                exit_value = False
            print(f"{HEADER} VLAN defined in {PATH_TO_VERITY_FILES}{VLAN_SRC_FILENAME} work = {same} !!")
        else:
            print(f"{HEADER} VLAN have not been executed !!")
    else:
        print(f"{HEADER} VLAN key is not defined in {PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!")

    # ''''''''''''''''''''''''''''''''''''''''''''
    # 14. Check IPv6 addresses
    # ''''''''''''''''''''''''''''''''''''''''''''
    if TEST_TO_EXC_IPV6_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_IPV6_KEY].get('test') is True:

            get_ipv6(
                nr=nr,
                get_vlan=test_to_execute.get(TEST_TO_EXC_IPV6_KEY).get("get_vlan", True),
                get_loopback=test_to_execute.get(TEST_TO_EXC_IPV6_KEY).get("get_loopback", True),
                get_peerlink=test_to_execute.get(TEST_TO_EXC_IPV6_KEY).get("get_peerlink", True),
                get_vni=test_to_execute.get(TEST_TO_EXC_IPV6_KEY).get("get_vni", True),
                get_physical=test_to_execute.get(TEST_TO_EXC_IPV6_KEY).get("get_physical", True)
            )

            ipv6_yaml_data = open_file(
                path=f"{PATH_TO_VERITY_FILES}{IPV6_SRC_FILENAME}"
            )
            same = compare_ipv6(nr, ipv6_yaml_data)
            if test_to_execute[TEST_TO_EXC_IPV6_KEY] is True and same is False:
                exit_value = False
            print(f"{HEADER} IPv6 addresses defined in {PATH_TO_VERITY_FILES}{IPV6_SRC_FILENAME} work = {same} !!")
        else:
            print(f"{HEADER} IPv6 addresses have not been executed !!")
    else:
        print(f"{HEADER} IPv6 addresses key is not defined in {PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!")

    return EXIT_SUCCESS


########################################################################################################################
#
# Entry Point
#
if __name__ == "__main__":
    main()
