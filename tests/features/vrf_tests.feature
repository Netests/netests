# Created by dylan.hamel at 09.12.19
Feature: Test protocols VRF python class ./protocols/vrf.py
  # Description
  Scenario:
    # Description
    Given I create a VRF object equals to Juniper manually named o01
    And I open YAML to create a VRF object equals to Juniper named o02
    And I create a VRF object from a Juniper Netconf output named o03
    And I create a VRF object equals to Cumulus manually named o04
    And I create a VRF object from a Cumulus API output named o05
    And I create a VRF object from a Cumulus SSH output named o06
    Then VRF object_01 should be equal to object_03
    And VRF object_01 should be equal to object_02
    And VRF object_02 should be not equal to object_03
    And VRF object_02 should be not equal to object_04
    And VRF object_02 should be not equal to object_05
    And VRF object_02 should be not equal to object_06
    And VRF object_04 should be not equal to object_05
    And VRF object_04 should be not equal to object_06