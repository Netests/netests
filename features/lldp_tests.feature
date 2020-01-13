# Created by dylan.hamel at 13.01.20
Feature: Test protocols LLDP python class ./protocols/lldp.py
  # Description
  Scenario:
    # Description
    Given I create an LLDP python object corresponding to Juniper device manually named object_01
    And I retrieve data from a YAML file corresponding to devices to create an LLDP python object named object_02
    And I create an LLDP python object from a Juniper output command named object_03
    And I create an LLDP python object from a Cumulus output command named object_04

    # Add device
    Then LLDP object_01 should be equal to object_02
    And LLDP object_02 should be equal to object_03
    And LLDP object_01 should be equal to object_03
    And LLDP object_03 should be equal to object_01
    And LLDP object_03 should not be equal to object_04
    And LLDP object_02 should be equal to object_04
