#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.exceptions.netests_exceptions import NetestsException


class NetestsIOSXRNetconfOutputError(NetestsException):
    pass


class NetestsIOSXRApiOutputError(NetestsException):
    pass


class NetestsIOSXRSshOutputError(NetestsException):
    pass
