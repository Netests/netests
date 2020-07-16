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
        adjacencies=isis_adj_lst
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


@then(u'I create a ISISAdjacency object to test compare function named o9999')
def step_impl(context):
    context.o9999 = ISISAdjacency(
        session_state="Up",
        level_type=ISIS_LEVEL_2,
        circuit_type="2",
        local_interface_name="ge-0/0/1.0",
        neighbor_sys_name="vMX5",
        neighbor_ip_addr="10.100.15.2",
        snap="0:50:56:a2:81:7c"
    )


@then(u'I create a ISISAdjacency object to test compare function with <circuit_type> named o9982')
def step_impl(context):
    options = {
        'compare': {
            'circuit_type': True
        }
    }
    context.o9982 = create_isis_obj_for_compare(options)

@then(u'I create a ISISAdjacency object to test compare equal to o9982 without <circuit_type> named o9983')
def step_impl(context):
    options = {}
    context.o9983 = create_isis_obj_for_compare(options)


@then(u'I compare ISISAdjacency o9982 and o9999 with a personal function - should not work')
def step_impl(context):
    assert context.o9982 != context.o9999


@then(u'I compare ISISAdjacency o9983 and o9999 with a personal function - should work')
def step_impl(context):
    assert context.o9983 == context.o9999


@then(u'I create a ISISAdjacency object to test compare function with <local_interface_name> named o9984')
def step_impl(context):
    options = {
        'compare': {
            'local_interface_name': True
        }
    }
    context.o9984 = create_isis_obj_for_compare(options)


@then(u'I create a ISISAdjacency object to test compare equal to o9984 without <local_interface_name> named o9985')
def step_impl(context):
    options = {}
    context.o9985 = create_isis_obj_for_compare(options)


@then(u'I compare ISISAdjacency o9984 and o9999 with a personal function - should not work')
def step_impl(context):
    assert context.o9984 != context.o9999


@then(u'I compare ISISAdjacency o9985 and o9999 with a personal function - should work')
def step_impl(context):
    assert context.o9985 == context.o9999


@then(u'I create a ISISAdjacency object to test compare function with <neighbor_ip_addr> named o9986')
def step_impl(context):
    options = {
        'compare': {
            'neighbor_ip_addr': True
        }
    }
    context.o9986 = create_isis_obj_for_compare(options)
    

@then(u'I create a ISISAdjacency object to test compare equal to o9986 without <neighbor_ip_addr> named o9987')
def step_impl(context):
    options = {}
    context.o9987 = create_isis_obj_for_compare(options)


@then(u'I compare ISISAdjacency o9986 and o9999 with a personal function - should not work')
def step_impl(context):
    assert context.o9986 != context.o9999


@then(u'I compare ISISAdjacency o9987 and o9999 with a personal function - should work')
def step_impl(context):
    assert context.o9987 == context.o9999


@then(u'I create a ISISAdjacency object to test compare function with <snap> named o9988')
def step_impl(context):
    options = {
        'compare': {
            'snap': True
        }
    }
    context.o9988 = create_isis_obj_for_compare(options)


@then(u'I create a ISISAdjacency object to test compare equal to o9988 without <snap> named o9989')
def step_impl(context):
    options = {}
    context.o9989 = create_isis_obj_for_compare(options)


@then(u'I compare ISISAdjacency o9988 and o9999 with a personal function - should not work')
def step_impl(context):
    assert context.o9988 != context.o9999


@then(u'I compare ISISAdjacency o9989 and o9999 with a personal function - should work')
def step_impl(context):
    assert context.o9989 == context.o9999


def create_isis_obj_for_compare(options={}):
    return ISISAdjacency(
        session_state="Up",
        level_type=ISIS_LEVEL_2,
        circuit_type="2320741203841237401328412073847-WHAT-??????",
        local_interface_name="ge-0/0/123123-BigSwitch",
        neighbor_sys_name="vMX5",
        neighbor_ip_addr="What's-my-ip-?",
        snap="123123123",
        options=options
    )
