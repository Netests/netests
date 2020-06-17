#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import yaml
import subprocess
from netests.constants import DATA_MODELS_PATH

@given(u'I try to execute netests --show-data-model bgp')
def step_impl(context):
    context.o0001 = subprocess.run(
        [
            "./netests/welcome.py",
            "--show-data-model",
            "bgp"]
    )

@then(u'I print BGP data model')
def step_impl(context):
    print(context.o0001)


@then(u'I can convert bgp.yml to dict with yaml')
def step_impl(context):
    print(yaml.load(f"{DATA_MODELS_PATH}bgp.yml"))


@given(u'I try to execute netests --show-data-model cdp')
def step_impl(context):
    context.o0002 = subprocess.run(
        [
            "./netests/welcome.py",
            "--show-data-model",
            "cdp"]
    )


@then(u'I print CDP data model')
def step_impl(context):
    print(context.o0002)


@then(u'I can convert cdp.yml to dict with yaml')
def step_impl(context):
    print(yaml.load(f"{DATA_MODELS_PATH}cdp.yml"))


@given(u'I try to execute netests --show-data-model facts')
def step_impl(context):
    context.o0003 = subprocess.run(
        [
            "./netests/welcome.py",
            "--show-data-model",
            "facts"]
    )


@then(u'I print Facts data model')
def step_impl(context):
    print(context.o0003)


@then(u'I can convert facts.yml to dict with yaml')
def step_impl(context):
    print(yaml.load(f"{DATA_MODELS_PATH}facts.yml"))


@given(u'I try to execute netests --show-data-model lldp')
def step_impl(context):
    context.o0004 = subprocess.run(
        [
            "./netests/welcome.py",
            "--show-data-model",
            "lldp"]
    )


@then(u'I print LLDP data model')
def step_impl(context):
    print(context.o0004)


@then(u'I can convert lldp.yml to dict with yaml')
def step_impl(context):
    print(yaml.load(f"{DATA_MODELS_PATH}lldp.yml"))


@given(u'I try to execute netests --show-data-model ospf')
def step_impl(context):
    context.o0005 = subprocess.run(
        [
            "./netests/welcome.py",
            "--show-data-model",
            "ospf"]
    )


@then(u'I print OSPF data model')
def step_impl(context):
    print(context.o0005)


@then(u'I can convert ospf.yml to dict with yaml')
def step_impl(context):
    print(yaml.load(f"{DATA_MODELS_PATH}ospf.yml"))


@given(u'I try to execute netests --show-data-model ping')
def step_impl(context):
    context.o0006 = subprocess.run(
        [
            "./netests/welcome.py",
            "--show-data-model",
            "ping"]
    )


@then(u'I print PING data model')
def step_impl(context):
    print(context.o0006)


@then(u'I can convert ping.yml to dict with yaml')
def step_impl(context):
    print(yaml.load(f"{DATA_MODELS_PATH}ping.yml"))


@given(u'I try to execute netests --show-data-model vlan')
def step_impl(context):
    context.o0007 = subprocess.run(
        [
            "./netests/welcome.py",
            "--show-data-model",
            "vlan"]
    )


@then(u'I print VLAN data model')
def step_impl(context):
    print(context.o0007)


@then(u'I can convert vlan.yml to dict with yaml')
def step_impl(context):
    print(yaml.load(f"{DATA_MODELS_PATH}vlan.yml"))


@given(u'I try to execute netests --show-data-model vrf')
def step_impl(context):
    context.o0008 = subprocess.run(
        [
            "./netests/welcome.py",
            "--show-data-model",
            "vrf"]
    )


@then(u'I print VRF data model')
def step_impl(context):
    print(context.o0008)


@then(u'I can convert vrf.yml to dict with yaml')
def step_impl(context):
    print(yaml.load(f"{DATA_MODELS_PATH}vrf.yml"))


@given(u'I get all protocols listed in netests/converters')
def step_impl(context):
    context.dirs = os.listdir('netests/converters/')
    print(context.dirs)


@given(u'I check that a data_model exist for each protocol')
def step_impl(context):
    for protocol in context.dirs:
        if "__" not in protocol:
            print(">>>>>>>>>>>>>", protocol)
            with open(f"{DATA_MODELS_PATH}{protocol}.yml", 'r') as f:
                print(f.read())

