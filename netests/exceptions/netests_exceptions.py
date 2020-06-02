#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class NetestsException(Exception):
    pass


class NetestsFunctionNotImplemented(NetestsException):
    pass


class NetestsFunctionNotPossible(NetestsException):
    pass


class NetestsDeviceNotCompatibleWithNapalm(NetestsException):
    pass


class NetestsHTTPStatusCodeError(NetestsException):
    pass


class NetestsOverideTruthVarsKeyUnsupported(NetestsException):
    pass


class NetestsErrorWithPingExecution(NetestsException):
    pass


class NetestsPingConnectionNotPossible(NetestsException):
    pass
