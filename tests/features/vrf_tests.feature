# Created by dylan.hamel at 09.12.19
Feature: Test protocols VRF python class ./protocols/vrf.py
  # Description
  Scenario:
    # Description
    Given I create a VRF python object manually named o01
    And I get content of a YAML file to create a VRF object named o02
    And I create a VRF object from a Juniper Netconf output named o03
    Then VRF object_01 should be equal to object_03
    And VRF object_01 should be equal to object_02
    And VRF object_02 should be not equal to object_03