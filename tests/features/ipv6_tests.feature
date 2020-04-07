# Created by dylan.hamel at 11.12.19
Feature: Test protocols IPv6 python class ./protocols/IPv6.py
  # Description
  Scenario:
    # Description
    Given I create an IPv6 python object corresponding to Arista device manually named object_01
    And I retrieve data from a YAML file corresponding to devices to create an IPv6 python object named object_02
    And I create an IPv6 python object from a Arista output command named object_03
    And I create an IPv6 python object from a Cumulus output command named object_04

    # Add device
    Then IPv6 object_01 should be equal to object_02
    And IPv6 object_02 should be equal to object_03
    And IPv6 object_01 should be equal to object_03
    And IPv6 object_03 should be equal to object_01
    And IPv6 object_02 should be equal to object_04
    And IPv6 object_03 should not be equal to object_04
