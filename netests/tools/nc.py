#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import lxml
import xmltodict
from xml.etree import ElementTree


def format_xml_output(output) -> dict:
    if output is None:
        return {}
    elif isinstance(output, dict):
        return output
    elif isinstance(output, lxml.etree._Element):
        output = json.dumps(
            xmltodict.parse(
                ElementTree.tostring(output)
            )
        )
    elif isinstance(output, str):
        output = json.dumps(xmltodict.parse(output))

    elif isinstance(output, bytes):
        output = json.dumps(xmltodict.parse(str(output, 'utf-8')))

    return json.loads(output)


def bytes_to_json(output) -> dict:
    print(type(output))
    if isinstance(output, bytes):
        print(type(output))
        print(type(json.loads(output)))
        return json.loads(output)
