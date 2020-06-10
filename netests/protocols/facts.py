#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from netests.constants import COMPARE_OPTION_KEY, PRINT_OPTION_KEY, NOT_SET


class Facts:

    hostname: str
    version: str
    build: str
    serial: str
    domain: str
    base_mac: str
    memory: str
    vendor: str
    model: str
    interfaces_lst: list
    options: dict

    def __init__(
        self,
        hostname=NOT_SET,
        domain=NOT_SET,
        version=NOT_SET,
        build=NOT_SET,
        serial=NOT_SET,
        base_mac=NOT_SET,
        memory=NOT_SET,
        vendor=NOT_SET,
        model=NOT_SET,
        interfaces_lst=list(),
        options=list(),
    ):
        self.hostname = hostname
        self.domain = domain
        self.version = version
        self.build = build
        self.serial = serial
        self.base_mac = base_mac
        self.memory = memory
        self.vendor = vendor
        self.model = model
        self.interfaces_lst = interfaces_lst
        self.options = options

    def __eq__(self, other):
        if not isinstance(other, Facts):
            return NotImplemented

        if COMPARE_OPTION_KEY in self.options.keys():
            log.debug(f"Compare modified function\noptions={self.options}")

            is_equal = True
            if self.options.get(COMPARE_OPTION_KEY).get('hostname', True):
                if str(self.hostname) != str(other.hostname):
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY).get('domain', False):
                if str(self.domain) != str(other.domain):
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY).get('version', True):
                if str(self.version) != str(other.version):
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY).get('build', False):
                if str(self.build) != str(other.build):
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY).get('serial', False):
                if str(self.serial) != str(other.serial):
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY).get('base_mac', False):
                if str(self.base_mac) != str(other.base_mac):
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY).get('memory', False):
                if str(self.memory) != str(other.memory):
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY).get('vendor', False):
                if str(self.vendor) != str(other.vendor):
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY).get('model', False):
                if str(self.model) != str(other.model):
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY) \
                           .get('interfaces_lst', False):
                if str(self.interfaces_lst) != str(other.interfaces_lst):
                    is_equal = False

            log.debug(
                "Result for modified compare function\n"
                f"is_equal={is_equal}"
            )

            return is_equal
        else:
            log.debug(f"Compare standard function\noptions={self.options}")

            is_equal = (
                str(self.hostname) == str(other.hostname) and
                str(self.version) == str(other.version)
            )

            log.debug(
                "Result for standard compare function\n"
                f"is_equal={is_equal}"
            )

            return is_equal

    def __repr__(self):
        if PRINT_OPTION_KEY in self.options.keys():
            ret = "\t<Facts\n"
            if self.options.get(PRINT_OPTION_KEY).get('hostname', True):
                ret += f"\t\thostname={self.hostname}\n"
            if self.options.get(PRINT_OPTION_KEY).get('domain', True):
                ret += f"\t\tdomain={self.domain}\n"
            if self.options.get(PRINT_OPTION_KEY).get('version', True):
                ret += f"\t\tversion={self.version}\n"
            if self.options.get(PRINT_OPTION_KEY).get('build', True):
                ret += f"\t\tbuild={self.build}\n"
            if self.options.get(PRINT_OPTION_KEY).get('serial', True):
                ret += f"\t\tserial={self.serial}\n"
            if self.options.get(PRINT_OPTION_KEY).get('base_mac', True):
                ret += f"\t\tbase_mac={self.base_mac}\n"
            if self.options.get(PRINT_OPTION_KEY).get('memory', True):
                ret += f"\t\tmemory={self.memory}\n"
            if self.options.get(PRINT_OPTION_KEY).get('vendor', True):
                ret += f"\t\tvendor={self.vendor}\n"
            if self.options.get(PRINT_OPTION_KEY).get('model', True):
                ret += f"\t\tmodel={self.model}\n"
            if self.options.get(PRINT_OPTION_KEY).get('interfaces_lst', True):
                ret += f"\t\tinterfaces_lst={self.interfaces_lst}\n"
            return ret + ">\n"
        return "<Facts \n" \
               f"hostname={self.hostname}\n" \
               f"domain={self.domain}\n" \
               f"version={self.version}\n" \
               f"build={self.build}\n" \
               f"serial={self.serial}\n" \
               f"base_mac={self.base_mac}\n" \
               f"memory={self.memory}\n" \
               f"vendor={self.vendor}\n" \
               f"model={self.model}\n" \
               f"interfaces_lst={self.interfaces_lst}>\n"

    def to_json(self):
        if PRINT_OPTION_KEY in self.options.keys():
            ret = dict()
            ret['Facts'] = dict()
            if self.options.get(PRINT_OPTION_KEY).get('hostname', True):
                ret['Facts']['hostname'] = self.hostname
            if self.options.get(PRINT_OPTION_KEY).get('domain', True):
                ret['Facts']['domain'] = self.domain
            if self.options.get(PRINT_OPTION_KEY).get('version', True):
                ret['Facts']['version'] = self.version
            if self.options.get(PRINT_OPTION_KEY).get('build', True):
                ret['Facts']['build'] = self.build
            if self.options.get(PRINT_OPTION_KEY).get('serial', True):
                ret['Facts']['serial'] = self.serial
            if self.options.get(PRINT_OPTION_KEY).get('base_mac', True):
                ret['Facts']['base_mac'] = self.base_mac
            if self.options.get(PRINT_OPTION_KEY).get('memory', True):
                ret['Facts']['memory'] = self.memory
            if self.options.get(PRINT_OPTION_KEY).get('vendor', True):
                ret['Facts']['vendor'] = self.vendor
            if self.options.get(PRINT_OPTION_KEY).get('model', True):
                ret['Facts']['model'] = self.model
            if self.options.get(PRINT_OPTION_KEY).get('interfaces_lst', True):
                ret['Facts']['interfaces_lst'] = self.interfaces_lst
            return ret
        else:
            return {
                "hostname": self.hostname,
                "domain": self.domain,
                "version": self.version,
                "build": self.build,
                "serial": self.serial,
                "base_mac": self.base_mac,
                "memory": self.memory,
                "vendor": self.vendor,
                "model": self.model,
                "interfaces_lst": self.interfaces_lst
            }
