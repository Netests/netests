#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
from netests.base_cli import NetestsCLI
from netests.nornir_inventory import init_nornir


@given(u'I create a NetestsCLI object with Ansible parameters named cli')
def step_impl(context):

    nr = init_nornir(
        log_file="./nornir/nornir.log",
        log_level="debug",
        ansible_inventory=True,
        nornir_inventory=False,
        netbox_inventory=False,
        num_workers=100,
        inventory_config_file=False,
        inventory="./tests/inventory/ansible/hosts",
        nornir_groups_file="",
        nornir_defaults_file="",
        netbox_url="",
        netbox_token="",
        netbox_ssl="",
    )

    context.cli = NetestsCLI(nornir=nr)


@given(u'I print NetestsCLI object')
def step_impl(context):
    print(context.cli)


@then(u'I can print help')
def step_impl(context):
    context.cli.print_help()


@then(u'I can print help for select command')
def step_impl(context):
    context.cli.print_select_help()


@then(u'I can print help for unselect command')
def step_impl(context):
    context.cli.print_unselect_help()


@then(u'I can select * devices')
def step_impl(context):
    assert context.cli.check_input("select *")
    assert context.cli.select_action("select *")
    assert len(context.cli.devices) != 0


@then(u'I can unselect * devices')
def step_impl(context):
    assert context.cli.check_input("unselect *")
    assert context.cli.select_action("unselect *")
    assert len(context.cli.devices) == 0


@then(u'I can select only one devices')
def step_impl(context):
    assert context.cli.check_input("select leaf01")
    assert context.cli.select_action("select leaf01")
    assert len(context.cli.devices) != 0


@then(u'I can unselect only one devices')
def step_impl(context):
    assert context.cli.check_input("unselect leaf01")
    assert context.cli.select_action("unselect leaf01")
    assert len(context.cli.devices) == 0


@then(u'I can select many devices')
def step_impl(context):
    assert context.cli.check_input("select leaf01,leaf02")
    assert context.cli.select_action("select leaf01,leaf02")
    assert len(context.cli.devices) != 0

@then(u'I can unselect many devices')
def step_impl(context):
    assert context.cli.check_input("unselect leaf01,leaf02")
    assert context.cli.select_action("unselect leaf01,leaf02")
    assert len(context.cli.devices) == 0


@then(u'I can print help for selected commands')
def step_impl(context):
    context.cli.print_selected_help()


@then(u'I can use selected command')
def step_impl(context):
    assert context.cli.check_input("selected")
    assert context.cli.select_action("selected")


@then(u'I can print help for print commands')
def step_impl(context):
    context.cli.print_print_help()


@then(u'I can print help for options commands')
def step_impl(context):
    context.cli.print_options_help()


@then(u'I can use the options command with many class params')
def step_impl(context):
    assert context.cli.check_input("options vrf vrf_name,rd")
    assert context.cli.select_action("options vrf vrf_name,rd")


@then(u'I can use the options command with * arguments')
def step_impl(context):
    assert context.cli.check_input("options vrf *")
    assert context.cli.select_action("options vrf *")


@then(u'I can print help for more commands')
def step_impl(context):
    context.cli.print_more_help()


@then(u'I can use more command')
def step_impl(context):
    assert context.cli.check_input("more vrf")
    assert context.cli.select_action("more vrf")


@then(u'I can print help for show commands')
def step_impl(context):
    context.cli.print_show_help()


@then(u'I can use show command')
def step_impl(context):
    assert context.cli.check_input("show vrf")
    assert context.cli.select_action("show vrf")

@then(u'I can print * devices')
def step_impl(context):
    assert context.cli.check_input("print *")
    assert context.cli.select_action("print *")


@then(u'I can print only one devices')
def step_impl(context):
    assert context.cli.check_input("print leaf01")
    assert context.cli.select_action("print leaf01")


@then(u'I can print many devices')
def step_impl(context):
    assert context.cli.check_input("print leaf01,leaf02")
    assert context.cli.select_action("print leaf01,leaf02")


@then(u'I can print help for get commands')
def step_impl(context):
    context.cli.print_get_help()


@then(u'I simulate a GET VRF command.')
def step_impl(context):
    assert context.cli.check_input("get vrf")


@then(u'I simulate a GET command without parameter - Error')
def step_impl(context):
    assert not(context.cli.check_input("get"))


@then(u'I can print help for compare commands')
def step_impl(context):
    context.cli.print_compare_help()


@then(u'I can print help for exit commands')
def step_impl(context):
    context.cli.print_exit_help()
"""