#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from ncclient import manager
from ncclient.operations import RPC, RPCReply
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.netconf_tools import format_xml_output
from exceptions.netests_exceptions import NetestsErrorWithPingExecution
from const.constants import NOT_SET, LEVEL5, PING_DATA_HOST_KEY
import pprint
PP = pprint.PrettyPrinter(indent=4)


class RPC(RPC):
    def _wrap(self, subele):
        return subele


class REPLY_CLS(RPCReply):
    def parse(self):
        self._parsed = True
        return True


def _iosxr_ping_netconf_exec(task, options={}):
    pl = '''<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"
                 message-id="REPLACE_MSG_ID">
        <ping xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ping-act">
        <destination>
        <destination>IP_ADDRESS_TO_PING</destination>
        <repeat-count>1</repeat-count>
        <vrf-name>VRF_NAME_FOR_PING</vrf-name>
        <timeout>2</timeout>
        </destination>
        </ping>
        </rpc>'''
    error_lst = list()
    with manager.connect(
        host=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        hostkey_verify=False,
        look_for_keys=False,
        allow_agent=False,
        device_params={'name': 'iosxr'}
    ) as m:

        for ping_line in task.host[PING_DATA_HOST_KEY].ping_lst:
            RPC.REPLY_CLS = REPLY_CLS
            rpc = RPC(m._session, m._device_handler)
            lp = pl.replace("REPLACE_MSG_ID", rpc._id, 1) \
                   .replace("IP_ADDRESS_TO_PING", ping_line.ip_address, 1) \
                   .replace("VRF_NAME_FOR_PING", ping_line.vrf, 1)

            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL5
            ):
                printline()
                PP.pprint(format_xml_output(lp))

            reply = rpc._request(lp)
            o = format_xml_output(reply.xml)
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL5
            ):
                printline()
                PP.pprint(o)
                PP.pprint(ping_line.to_json())

            if (
                isinstance(o, dict) and
                'rpc-reply' in o.keys() and
                'ping-response' in o.get('rpc-reply').keys() and
                'ipv4' in o.get('rpc-reply').get('ping-response').keys()
            ):
                if (
                    (
                        o.get('rpc-reply')
                         .get('ping-response')
                         .get('ipv4')
                         .get('success-rate') == '100' and
                        ping_line.works is False
                    ) or
                    (
                        o.get('rpc-reply')
                         .get('ping-response')
                         .get('ipv4')
                         .get('success-rate') == '0' and
                        ping_line.works is True
                    )
                ):
                    error_lst.append(ping_line)

    if len(error_lst) > 0:
        raise NetestsErrorWithPingExecution(error_lst)
