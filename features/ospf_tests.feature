# Created by dylan.hamel at 11.12.19
Feature: Test protocols OSPF python class ./protocols/ospf.py
  # Description
  Scenario:
    # Description
    Given I create an OSPF python object corresponding to Cumulus device manually named object_01
    And I retrieve data from a YAML file corresponding to devices to create an OSPF python object named object_02
    And I create an OSPF python object from a Cumulus output command named object_03
    And I create an OSPF python object from a Juniper output command named object_04
    And I create an OSPF python object from a Extreme VSP output command named object_05
    And I create an OSPF python object from a Cisco IOS output command named object_06
    Then OSPF object_01 should be equal to object_02
    And OSPF object_01 should be equal to object_03
    And OSPF object_03 should be equal to object_01
    And OSPF object_02 should be equal to object_03
    And OSPF object_02 should be equal to object_04
    And OSPF object_02 should be equal to object_05
    And OSPF object_02 should be equal to object_06
    And OSPF object_03 should not be equal to object_04
    And OSPF object_03 should not be equal to object_05
    And OSPF object_03 should not be equal to object_06