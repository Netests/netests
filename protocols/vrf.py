#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import os
from const.constants import (
    NOT_SET,
    LEVEL1
)
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode

H = "[ListVRF - __eq__] -"


class VRF:

    vrf_name: str
    vrf_id: str
    vrf_type: str
    l3_vni: str
    rd: str
    rt_imp: str
    rt_exp: str
    imp_targ: str
    exp_targ: str

    def __init__(
        self,
        vrf_name=NOT_SET,
        vrf_id=NOT_SET,
        vrf_type=NOT_SET,
        l3_vni=NOT_SET,
        rd=NOT_SET,
        rt_imp=NOT_SET,
        rt_exp=NOT_SET,
        imp_targ=NOT_SET,
        exp_targ=NOT_SET
    ):
        self.vrf_name = vrf_name
        self.vrf_id = vrf_id
        self.vrf_type = vrf_type
        self.l3_vni = l3_vni
        self.rd = rd
        self.rt_imp = rt_imp
        self.rt_exp = rt_exp
        self.imp_targ = imp_targ
        self.exp_targ = exp_targ

    def __eq__(self, other):
        if not isinstance(other, VRF):
            return NotImplementedError

        return ((str(self.vrf_name) == str(other.vrf_name)))

    def __repr__(self):
        return f"\t<VRF vrf_name={self.vrf_name}\n" \
               f"\t\tvrf_id={self.vrf_id}\n" \
               f"\t\tvrf_type={self.vrf_type}\n" \
               f"\t\tl3_vni={self.l3_vni}\n" \
               f"\t\trd={self.rd}\n" \
               f"\t\trt_imp={self.rt_imp}\n" \
               f"\t\trt_exp={self.rt_exp}\n" \
               f"\t\timp_targ={self.imp_targ}\n" \
               f"\t\texp_targ={self.exp_targ}>\n"


class ListVRF:

    vrf_lst: list

    def __init__(self, vrf_lst: list()):
        self.vrf_lst = vrf_lst

    def __eq__(self, others):
        if not isinstance(others, ListVRF):
            raise NotImplementedError

        for vrf in self.vrf_lst:
            if vrf not in others.vrf_lst:
                if verbose_mode(
                    user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                    needed_value=LEVEL1
                ):
                    printline()
                    print(f"{H} The following VRF is not in the list \n {vrf}")
                    print(f"{H} List: \n {others.vrf_lst}")
                return False

        for vrf in others.vrf_lst:
            if vrf not in self.vrf_lst:
                if verbose_mode(
                    user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                    needed_value=LEVEL1
                ):
                    printline()
                    print(f"{H} The following VRF is not in the list \n {vrf}")
                    print(f"{H} List: \n {others.vrf_lst}")
                return False

        return True

    def __repr__(self):
        result = "<ListVRF \n"
        for vrf in self.vrf_lst:
            result = result + f"{vrf}"
        return result + ">"
