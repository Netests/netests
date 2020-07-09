#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import ValidationError
from netests.protocols.isis import (
    ISISAdjacency,
    ListISISAdjacency,
    ISISAdjacencyVRF,
    ListISISAdjacencyVRF,
    ISIS
)
from netests.constants import ISIS_LEVEL_1, ISIS_LEVEL_2
import pprint
PP = pprint.PrettyPrinter(indent=4)


@given(u'I create a ISISAdjacency object named o0000')
def step_impl(context):
    
    context.o0000 = ISISAdjacency(
        session_state="Up",
        level_type=ISIS_LEVEL_2,
        circuit_type="2",
        local_interface_name="ge-0/0/1.0",
        neighbor_sys_name="vMX5",
        neighbor_ip_addr="10.100.15.2",
        snap="0:50:56:a2:81:7c"
    )


@then(u'I can print ISISAdjacency object named o0000')
def step_impl(context):
    print("")
    print(context.o0000)


@then(u'I can print ISISAdjacency object named o0000 in JSON format')
def step_impl(context):
    print("")
    PP.pprint(context.o0000.to_json())


@then(u'I can print ISISAdjacency object named o0000 in dict format')
def step_impl(context):
    print("")
    PP.pprint(context.o0000.dict())


@given(u'I create a ListISISAdjcency object named o0001')
def step_impl(context):

    context.o0001 = ListISISAdjacency(
        isis_adj_lst=list()
    )

    context.o0001.isis_adj_lst.append(
        ISISAdjacency(
            session_state="Up",
            level_type=ISIS_LEVEL_2,
            circuit_type="2",
            local_interface_name="ge-0/0/1.0",
            neighbor_sys_name="vMX5",
            neighbor_ip_addr="10.100.15.2",
            snap="0:50:56:a2:81:7c"
        )
    )

    context.o0001.isis_adj_lst.append(
        ISISAdjacency(
            session_state="Up",
            level_type=ISIS_LEVEL_2,
            circuit_type="2",
            local_interface_name="ge-0/0/1.0",
            neighbor_sys_name="vMX5",
            neighbor_ip_addr="10.100.15.2",
            snap="0:50:56:a2:81:7c"
        )
    )




@then(u'I can print ListISISAdjcency object named o0001')
def step_impl(context):
    print("")
    print(context.o0001)


@then(u'I can print ListISISAdjcency object named o0001 in JSON format')
def step_impl(context):
    print("")
    PP.pprint(context.o0001.to_json())


@then(u'I can print ListISISAdjcency object named o0001 in dict format')
def step_impl(context):
    print("")
    PP.pprint(context.o0001.dict())


@given(u'I create a ISISAdjcencyVRF object named o0002')
def step_impl(context):
    isis_adj_lst = ListISISAdjacency(
        isis_adj_lst=list()
    )

    isis_adj_lst.isis_adj_lst.append(
        ISISAdjacency(
            session_state="Up",
            level_type=ISIS_LEVEL_2,
            circuit_type="2",
            local_interface_name="ge-0/0/1.0",
            neighbor_sys_name="vMX5",
            neighbor_ip_addr="10.100.15.2",
            snap="0:50:56:a2:81:7c"
        )
    )

    isis_adj_lst.isis_adj_lst.append(
        ISISAdjacency(
            session_state="Up",
            level_type=ISIS_LEVEL_2,
            circuit_type="2",
            local_interface_name="ge-0/0/1.0",
            neighbor_sys_name="vMX5",
            neighbor_ip_addr="10.100.15.2",
            snap="0:50:56:a2:81:7c"
        )
    )

    context.o0002 = ISISAdjacencyVRF(
        router_id="10.100.100.1",
        system_id="1010.0100.0001",
        area_id="49.0001",
        vrf_name="default",
        isis_adj_lst=isis_adj_lst
    )


@then(u'I can print ISISAdjcencyVRF object named o0002')
def step_impl(context):
    print("")
    print(context.o0002)


@then(u'I can print ISISAdjcencyVRF object named o0002 in JSON format')
def step_impl(context):
    print("")
    PP.pprint(context.o0002.to_json())


@then(u'I can print ISISAdjcencyVRF object named o0002 in dict format')
def step_impl(context):
    print("")
    PP.pprint(context.o0002.dict())
