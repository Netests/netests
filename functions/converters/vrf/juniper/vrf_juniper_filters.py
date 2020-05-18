#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def _juniper_vrf_filter(vrf_name: str) -> bool:
    """
    This function will remove Juniper system. VRF
    - "master"
    - "__juniper_private1__"
    - "__juniper_private2__"
    - "__juniper_private4__"
    - "__master.anon__"

    :param vrf_name:
    :return bool: True if the VRF must be added in the list
    """
    return "__" not in vrf_name


def _juniper_vrf_default_mapping(vrf_name: str) -> str:
    """
    This function will convert Juniper global/default/master routing instance
    => master => default

    :param vrf_name:
    :return str: "default" if vrf_name = "master" else vrf_name
    """

    if vrf_name == "master":
        return "default"
    else:
        return vrf_name
