#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core import Nornir
from netests.base_protocols import MAPPING_CONNEXION_PLATFORM
from netests.constants import NOT_SET, CONNEXION_MODE, PLATFORM_SUPPORTED
import pprint
PP = pprint.PrettyPrinter(indent=4)


class ValidateNetestsInventory(object):

    nr: Nornir
    result: dict
    valid: bool

    def __init__(self, nr):
        self.nr = nr
        self.result = {}

        self._check_connexions()
        self._check_platform()
        self._check_secure_api()
        self._check_port()
        self._check_connexion_platform_compatibility()
        self.valid = self.__is_a_valid_inventory()

    def get_result(self):
        return self.result

    def get_valid(self):
        return self.valid

    def __is_a_valid_inventory(self):
        valid = True
        for key, value in self.result.items():
            if value.get('failed', False) is True:
                valid = False
        return valid

    def __generic_check(self, key, lst):
        self.result[key] = dict()
        self.result[key]['host_failed'] = list()

        error = False
        for host in self.nr.inventory.hosts:
            if self.nr.inventory.hosts.get(host).get(key, NOT_SET) not in lst:
                error = True
                self.result[key]['host_failed'].append(host)
        self.result[key]['failed'] = error

    def _check_platform(self):
        self.__generic_check('platform', PLATFORM_SUPPORTED)

    def _check_connexions(self):
        self.__generic_check('connexion', CONNEXION_MODE)

    def _check_port(self):
        self.result['port'] = dict()
        self.result['port']['host_failed'] = list()

        error = False
        for host in self.nr.inventory.hosts:
            if (
                self.nr.inventory.hosts.get(host).port < 1 or
                self.nr.inventory.hosts.get(host).port > 65535
            ):
                error = True
                self.result['port']['host_failed'].append(host)
        self.result['port']['failed'] = error

    def _check_secure_api(self):
        self.result['secure_api'] = dict()
        self.result['secure_api']['host_failed'] = list()

        error = False
        for host in self.nr.inventory.hosts:
            if 'secure_api' in self.nr.inventory.hosts.get(host).keys():
                if not isinstance(
                    self.nr.inventory.hosts.get(host).get('secure_api'),
                    bool
                ):
                    error = True
                    self.result['secure_api']['host_failed'].append(host)
        self.result['secure_api']['failed'] = error

    def _check_connexion_platform_compatibility(self):
        self.result['connexion_platform'] = dict()
        self.result['connexion_platform']['host_failed'] = list()
        error = False
        for host in self.nr.inventory.hosts:
            if self.nr.inventory \
                      .hosts \
                      .get(host) \
                      .get('platform') in MAPPING_CONNEXION_PLATFORM.keys():
                if MAPPING_CONNEXION_PLATFORM.get(
                    self.nr.inventory.hosts.get(host).get('platform')
                ).get(
                    self.nr.inventory.hosts.get(host).get('connexion')
                ) is False:
                    error = True
                    self.result.get('connexion_platform') \
                               .get('host_failed') \
                               .append(host)
            else:
                error = True
        self.result['connexion_platform']['failed'] = error

    def print_result(self):
        PP.pprint(self.result)
