# Created by dylan.hamel at 11.12.19
Feature: Test protocols VLAN python class ./protocols/vlan.py
  # Description
  Scenario:
    # Description
    Given I create an VLAN python object corresponding to Arista device manually named object_01
    And I retrieve data from a YAML file corresponding to devices to create an VLAN python object named object_02
    And I create an VLAN python object from a Arista output command named object_03
    And I create an VLAN python object from a Cumulus output command named object_04
    # Add device
    Then VLAN object_01 should be equal to object_02
    And VLAN object_02 should be equal to object_03
    And VLAN object_01 should be equal to object_03
    And VLAN object_03 should be equal to object_01
    And VLAN object_02 should be equal to object_04