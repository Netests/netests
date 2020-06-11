#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir import InitNornir
from netests.tools.verify import ValidateNetestsInventory


@given(u'A Nornir object based on an Ansible inventory')
def step_impl(context):
    context.nr = InitNornir(
        core={"num_workers": 10},
        inventory={
            "plugin": "nornir.plugins.inventory.ansible.AnsibleInventory",
            "options": {
                "hostsfile": "./tests/inventory/ansible/hosts"
            }
        },
        logging={
            "file": "",
            "level": "WARNING"
        }
    )
    

@given(u'A Nornir object based on an Ansible with a connexion error')
def step_impl(context):
    context.nr = create_nornir_obj(
        "./tests/inventory/bad/ansible/hosts_bad_connexion"
    )


@given(u'A Nornir object based on an Ansible with a platform error')
def step_impl(context):
    context.nr = create_nornir_obj(
        "./tests/inventory/bad/ansible/hosts_bad_platform"
    )


@given(u'A Nornir object based on an Ansible with a seucre_api error')
def step_impl(context):
    context.nr = create_nornir_obj(
        "./tests/inventory/bad/ansible/hosts_bad_secure_api"
    )


@given(u'A Nornir object based on an Ansible with a port error')
def step_impl(context):
    context.nr = create_nornir_obj(
        "./tests/inventory/bad/ansible/hosts_bad_port"
    )


@then(u'This inventory is working')
def step_impl(context):
    validate_nr = ValidateNetestsInventory(context.nr)
    assert validate_nr.get_valid()


@then(u'This inventory is not working')
def step_impl(context):
    validate_nr = ValidateNetestsInventory(context.nr)
    print(validate_nr.get_result())
    assert not validate_nr.get_valid()


def create_nornir_obj(path):
    return InitNornir(
        core={"num_workers": 10},
        inventory={
            "plugin": "nornir.plugins.inventory.ansible.AnsibleInventory",
            "options": {
                "hostsfile": f"{path}"
            }
        },
        logging={
            "file": "",
            "level": "WARNING"
        }
    )
