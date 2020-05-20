#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ncclient import manager
from xml.etree import ElementTree
from abc import ABC, abstractmethod
from netests.workers.device import Device


class DeviceNC(Device, ABC):

    def __init__(
        self,
        task,
        commands,
        vrf_loop,
        converter,
        key_store,
        options={}
    ):
        super().__init__(
            task,
            commands,
            vrf_loop,
            converter,
            key_store,
            options,
        )

    def validate_xml(self, output):
        return ElementTree.fromstring(output)

    def format_rpc_output(self, output):
        return ElementTree.tostring(output, encoding='utf8', method='xml')

    def exec_call(self, task, command):
        if self.nc_method == 'get':
            return self.exec_call_get(task, command)
        elif self.nc_method == 'get_config':
            return self.exec_call_get_config(task, command)

    @abstractmethod
    def exec_call_get(self, task, command):
        pass

    def exec_call_get_config(self, task, command):
        with manager.connect(
            host=task.host.hostname,
            port=task.host.port,
            username=task.host.username,
            password=task.host.password,
            hostkey_verify=False
        ) as m:

            vrf_config = m.get_config(
                source=self.source,
                filter=(
                    'subtree',
                    (
                        command
                    )
                )
            ).data_xml
            self.validate_xml(vrf_config)
            return vrf_config
