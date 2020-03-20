#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class NetestsException(Exception):
    pass


class NetestsFunctionNotImplemented(NetestsException):
    pass


class NetestsFunctionNotPossible(NetestsException):
    pass