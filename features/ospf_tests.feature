# Created by dylan.hamel at 11.12.19
Feature: Test protocols OSPF python class ./protocols/ospf.py
  # Description
  Scenario:
    # Description
    Given I create an OSPF python object corresponding to Cumulus device manually named object_01
    And I retrieve data from a YAML file corresponding to Cumulus device to create an OSPF python object named object_02
    And I create an OSPF python object from a Cumulus output command named object_03
    And I retrieve data from a YAML file corresponding to Juniper device to create an OSPF python object named object_04
    And I create an OSPF python object from a Juniper output command named object_05
    And I retrieve data from a YAML file corresponding to Extreme VSP device to create an OSPF python object named object_06
    And I create an OSPF python object from a Extreme VSP output command named object_07
    And I retrieve data from a YAML file corresponding to Cisco IOS device to create an OSPF python object named object_08
    And I create an OSPF python object from a Cisco IOS output command named object_09
    Then OSPF object_01 should be equal to object_02
    And OSPF object_01 should be equal to object_03
    And OSPF object_02 should be equal to object_03
    And OSPF object_04 should be equal to object_05
    And OSPF object_05 should be equal to object_04
    And OSPF object_06 should be equal to object_07
    And OSPF object_07 should be equal to object_06
    And OSPF object_08 should be equal to object_09
    And OSPF object_09 should be equal to object_08
    And OSPF object_02 should not be equal to object_04
    And OSPF object_04 should not be equal to object_06
    And OSPF object_06 should not be equal to object_08