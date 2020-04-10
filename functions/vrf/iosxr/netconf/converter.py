#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from const.constants import (
    NOT_SET,
    LEVEL1,
    LEVEL3,
    LEVEL4,
)
from protocols.vrf import (
    VRF,
    ListVRF
)
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.netconf_tools import format_xml_output
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _iosxr_vrf_netconf_converter(hostname: str, cmd_output) -> ListVRF:
    cmd_output = format_xml_output(cmd_output)

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL4
    ):
        printline()
        print(type(cmd_output))
        PP.pprint(cmd_output)

    vrf_list = ListVRF(vrf_lst=list())

    for v in cmd_output.get('data').get('vrfs').get('vrf'):
        rias = None
        riin = None
        reas = None
        rein = None
        if (
            'afs' in v.keys() and 'af' in v.get('afs').keys() and
            'bgp' in v.get('afs').get('af').keys()
        ):
            rias = v.get('afs').get('af').get('bgp') \
                                         .get('import-route-targets') \
                                         .get('route-targets') \
                                         .get('route-target') \
                                         .get('as-or-four-byte-as') \
                                         .get('as')

            riin = v.get('afs').get('af').get('bgp') \
                                         .get('import-route-targets') \
                                         .get('route-targets') \
                                         .get('route-target') \
                                         .get('as-or-four-byte-as') \
                                         .get('as-index')

            reas = v.get('afs').get('af').get('bgp') \
                                         .get('export-route-targets') \
                                         .get('route-targets') \
                                         .get('route-target') \
                                         .get('as-or-four-byte-as') \
                                         .get('as')

            rein = v.get('afs').get('af').get('bgp') \
                                         .get('export-route-targets') \
                                         .get('route-targets') \
                                         .get('route-target') \
                                         .get('as-or-four-byte-as') \
                                         .get('as-index')

        vrf_list.vrf_lst.append(
            VRF(
                vrf_name=v.get('vrf-name'),
                vrf_id=NOT_SET,
                vrf_type=NOT_SET,
                l3_vni=NOT_SET,
                rd=NOT_SET,
                rt_imp=f"{rias}:{riin}" if rias is not None else NOT_SET,
                rt_exp=f"{reas}:{rein}" if reas is not None else NOT_SET,
                imp_targ=NOT_SET,
                exp_targ=NOT_SET
            )
        )

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(f">>>>> {hostname}")
        print(vrf_list)

    return vrf_list
