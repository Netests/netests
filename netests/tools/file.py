#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import yaml


def open_file(path: str()) -> dict():
    """
    This function  will open a yaml file and return is data

    Args:
        param1 (str): Path to the yaml file

    Returns:
        dict: file content
    """

    with open(path, 'r') as yamlFile:
        try:
            data = yaml.load(yamlFile, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)

    return data


def open_txt_file_as_bytes(path: str()) -> str():
    """
    This function  will open a yaml file and return is data

    Args:
        param1 (str): Path to the string file

    Returns:
        str: file content
    """

    with open(path, 'rb') as content_file:
        try:
            content = content_file.read()
        except Exception as exc:
            print(exc)

    return content


def open_txt_file(path: str()) -> str():
    """
    This function  will open a yaml file and return is data

    Args:
        param1 (str): Path to the string file

    Returns:
        str: file content
    """

    with open(path, 'r') as content_file:
        try:
            content = content_file.read()
        except Exception as exc:
            print(exc)

    return content


def open_json_file(path: str()) -> str():
    """
        This function  will open a json file and return is data

        Args:
            param1 (str): Path to the string file

        Returns:
            str: file content
        """

    with open(path, 'r') as content_file:
        try:
            content = json.loads(content_file.read())
        except yaml.YAMLError as exc:
            print(exc)

    return content
