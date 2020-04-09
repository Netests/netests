#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import lxml
import xmltodict
from xml.etree import ElementTree


def format_xml_output(output) -> dict:
    if isinstance(output, lxml.etree._Element):
        output = json.dumps(
            xmltodict.parse(
                ElementTree.tostring(output)
            )
        )
    elif isinstance(output, str):
        output = json.dumps(xmltodict.parse(output))

    return json.loads(output)
