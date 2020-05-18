#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functions.workers.cumulus_rest import CumulusREST
from const.constants import CUMULUS_API_GET_VRF, VRF_DATA_KEY
from functions.vrf.cumulus.api.converter import _cumulus_vrf_api_converter


class VRFCumulusREST(CumulusREST):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": CUMULUS_API_GET_VRF
                }
            },
            vrf_loop=False,
            converter=_cumulus_vrf_api_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
