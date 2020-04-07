# Created by dylan.hamel at 09.12.19
Feature: Test protocols BGP python class ./protocols/bgp.py
  # Description
  Scenario:
    # Description
    Given I create a BGP python object manually named object_01
    And I retrieve data from a YAML file to create a BGP python object named object_02
    And I create a BGP python object from a Extreme VSP output command named object_03
    And I create a BGP python object from a Cumulus output command named object_04
    Then BGP object_01 should be equal to object_03
    And BGP object_03 should be equal to object_01
    And BGP object_02 should be equal to object_04
    And BGP object_03 should be not equal to object_04
    And BGP object_04 should be not equal to object_03