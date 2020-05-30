#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from ncclient import manager
from nornir.core.task import Result
from ncclient.operations import RPC, RPCReply
from netests.tools.nc import format_xml_output
from netests.constants import PING_DATA_HOST_KEY
from netests.converters.ping.ping_validator import _raise_exception_on_ping_cmd


class RPC(RPC):
    def _wrap(self, subele):
        return subele


class REPLY_CLS(RPCReply):
    def parse(self):
        self._parsed = True
        return True


def _iosxr_ping_nc_exec(task):
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

        result = True
        for p in task.host[PING_DATA_HOST_KEY].ping_lst:
            RPC.REPLY_CLS = REPLY_CLS
            rpc = RPC(m._session, m._device_handler)
            lp = pl.replace("REPLACE_MSG_ID", rpc._id, 1) \
                   .replace("IP_ADDRESS_TO_PING", p.ip_address, 1) \
                   .replace("VRF_NAME_FOR_PING", p.vrf, 1)

            reply = rpc._request(lp)
            o = format_xml_output(reply.xml)

            log.debug(
                "\n"
                "Execute the following ping command on IOS-XR Netconf\n"
                f"{lp}"
                "From the following PING object :\n"
                f"{p.to_json()}"
                "Result is :\n"
                f"{o}"
            )

            if isinstance(o, dict) and 'rpc-reply' in o.keys():
                r = iosxr_netconf_validate_output(
                    output=o,
                    hostname=task.host.name,
                    platform=task.host.platform,
                    connexion=task.host.get('connexion'),
                    ping_print=p,
                    ping_works=p.works
                )

            if r is False:
                result = False

    return Result(host=task.host, result=result)


def iosxr_netconf_validate_output(
    output: dict,
    hostname: str,
    platform: str,
    connexion: str,
    ping_print: str,
    ping_works: bool
) -> None:
    _raise_exception_on_ping_cmd(
        output=output,
        hostname=hostname,
        platform=platform,
        connexion=connexion,
        ping_line=ping_print,
        must_work=ping_works
    )
