#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from netests.constants import NOT_SET


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

        return ((str(self.hostname) == str(other.hostname)) and
                (str(self.version) == str(other.version)))

    def __repr__(self):
        return f"<Facts hostname={self.hostname} " \
                f"domain={self.domain} " \
                f"version={self.version} " \
                f"build={self.build} " \
                f"serial={self.serial} " \
                f"base_mac={self.base_mac} " \
                f"memory={self.memory} "\
                f"vendor={self.vendor} " \
                f"model={self.model} "\
                f"interfaces_lst={self.interfaces_lst}>\n"

    def to_json(self):
        if 'print' in self.options.keys():
            ret = dict()
            ret['Facts'] = dict()
            if self.options.get('print').get('hostname', True):
                ret['Facts']['hostname'] = self.hostname
            if self.options.get('print').get('domain', True):
                ret['Facts']['domain'] = self.domain
            if self.options.get('print').get('version', True):
                ret['Facts']['version'] = self.version
            if self.options.get('print').get('build', True):
                ret['Facts']['build'] = self.build
            if self.options.get('print').get('serial', True):
                ret['Facts']['serial'] = self.serial
            if self.options.get('print').get('base_mac', True):
                ret['Facts']['base_mac'] = self.base_mac
            if self.options.get('print').get('memory', True):
                ret['Facts']['memory'] = self.memory
            if self.options.get('print').get('vendor', True):
                ret['Facts']['vendor'] = self.vendor
            if self.options.get('print').get('model', True):
                ret['Facts']['model'] = self.model
            if self.options.get('print').get('interfaces_lst', True):
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
