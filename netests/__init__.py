#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging


log = logging.getLogger(__name__)
file_handler = logging.FileHandler('netests.log')
formatter = logging.Formatter(
    fmt=(
        "[%(asctime)s.%(msecs)03d][%(levelname)s]"
        "[%(module)s][%(funcName)s:] %(message)s"
    ),
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
log.addHandler(file_handler)
log.setLevel(logging.DEBUG)

log.debug(
    "\n"
    "******************************************************\n" +
    "*                                                    *\n" +
    "*                New Netests.io RUN                  *\n" +
    "*                                                    *\n" +
    "******************************************************\n"
)
