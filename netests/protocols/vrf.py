#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET


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
    options: dict

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
        exp_targ=NOT_SET,
        options={}
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
        self.options = options

    def __eq__(self, other):
        if not isinstance(other, VRF):
            return NotImplementedError

        return ((str(self.vrf_name) == str(other.vrf_name)))

    def __repr__(self):
        if 'print' in self.options.keys():
            ret = "\t<VRF \n"
            if self.options.get('print').get('vrf_name', True):
                ret += f"\t\tvrf_name={self.vrf_name}\n"
            if self.options.get('print').get('vrf_id', True):
                ret += f"\t\tvrf_id={self.vrf_id}\n"
            if self.options.get('print').get('vrf_type', True):
                ret += f"\t\tvrf_type={self.vrf_type}\n"
            if self.options.get('print').get('l3_vni', True):
                ret += f"\t\tl3_vni={self.l3_vni}\n"
            if self.options.get('print').get('rd', True):
                ret += f"\t\trd={self.rd}\n"
            if self.options.get('print').get('rt_imp', True):
                ret += f"\t\trt_imp={self.rt_imp}\n"
            if self.options.get('print').get('rt_exp', True):
                ret += f"\t\trt_exp={self.rt_exp}\n"
            if self.options.get('print').get('imp_targ', True):
                ret += f"\t\timp_targ={self.imp_targ}\n"
            if self.options.get('print').get('exp_targ', True):
                ret += f"\t\texp_targ={self.exp_targ}\n"
            return ret
        else:
            return f"\t<VRF \n" \
                   f"\t\t vrf_name={self.vrf_name}\n" \
                   f"\t\tvrf_id={self.vrf_id}\n" \
                   f"\t\tvrf_type={self.vrf_type}\n" \
                   f"\t\tl3_vni={self.l3_vni}\n" \
                   f"\t\trd={self.rd}\n" \
                   f"\t\trt_imp={self.rt_imp}\n" \
                   f"\t\trt_exp={self.rt_exp}\n" \
                   f"\t\timp_targ={self.imp_targ}\n" \
                   f"\t\texp_targ={self.exp_targ}>\n"

    def to_json(self):
        if 'print' in self.options.keys():
            ret = dict()
            ret = dict()
            if self.options.get('print').get('vrf_name', True):
                ret['vrf_name'] = self.vrf_name
            if self.options.get('print').get('vrf_id', True):
                ret['vrf_id'] = self.vrf_id
            if self.options.get('print').get('vrf_type', True):
                ret['vrf_type'] = self.vrf_type
            if self.options.get('print').get('l3_vni', True):
                ret['l3_vni'] = self.l3_vni
            if self.options.get('print').get('rd', True):
                ret['rd'] = self.rd
            if self.options.get('print').get('rt_imp', True):
                ret['rt_imp'] = self.rt_imp
            if self.options.get('print').get('rt_exp', True):
                ret['rt_exp'] = self.rt_exp
            if self.options.get('print').get('imp_targ', True):
                ret['imp_targ'] = self.imp_targ
            if self.options.get('print').get('exp_targ', True):
                ret['exp_targ'] = self.exp_targ
            return ret
        else:
            return {
                "vrf_name": self.vrf_name,
                "vrf_id": self.vrf_id,
                "vrf_type": self.vrf_type,
                "l3_vni": self.l3_vni,
                "rd": self.rd,
                "rt_imp": self.rt_imp,
                "rt_exp": self.rt_exp,
                "imp_targ": self.imp_targ,
                "exp_targ": self.exp_targ
            }


class ListVRF:

    vrf_lst: list

    def __init__(self, vrf_lst: list()):
        self.vrf_lst = vrf_lst

    def __eq__(self, others):
        if not isinstance(others, ListVRF):
            raise NotImplementedError

        for vrf in self.vrf_lst:
            if vrf not in others.vrf_lst:
                return False

        for vrf in others.vrf_lst:
            if vrf not in self.vrf_lst:
                return False

        return True

    def __repr__(self):
        result = "<ListVRF \n"
        for vrf in self.vrf_lst:
            result = result + f"{vrf}"
        return result + ">"

    def to_json(self):
        data = list()
        for vrf in self.vrf_lst:
            data.append(vrf.to_json())
        return data
