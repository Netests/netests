#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import napalm_get


def _generic_cdp_napalm(task, options={}):
    pass