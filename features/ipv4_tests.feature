# Created by dylan.hamel at 11.12.19
Feature: Test protocols IPV4 python class ./protocols/ipv4.py
  # Description
  Scenario:
    # Description
    Given I create an IPV4 python object corresponding to Cumulus device manually named object_01
    And I retrieve data from a YAML file corresponding to devices to create an IPV4 python object named object_02
    And I create an IPV4 python object from a Cumulus output command named object_03
    And I create an IPV4 python object from a Cisco Nexus output command named object_04
    # Add device
    Then IPV4 object_01 should be equal to object_02
    And IPV4 object_02 should be equal to object_03
    And IPV4 object_01 should be equal to object_03
    And IPV4 object_03 should be equal to object_01
    And IPV4 object_02 should be equal to object_04