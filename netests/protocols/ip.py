#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import BaseModel
from netests.constants import NOT_SET


class IPAddress(BaseModel):
    ip_address: str = NOT_SET
    netmask: str = NOT_SET

    def __eq__(self, other):
        if not isinstance(other, IPAddress):
            raise NotImplementedError()
        else:
            return (
                self.ip_address == other.ip_address and
                self.netmask == other.netmask
            )

    def to_json(self):
        return {
            "ip_address": self.ip_address,
            "netmask": self.netmask
        }

    def __repr__(self):
        return str(
            f"<{type(self)}\n"
            f"\tip_address={self.ip_address}\n"
            f"\tnetmask={self.netmask}\n>"
        )
