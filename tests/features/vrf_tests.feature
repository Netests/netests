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
    And I create a VRF object equals to IOS-XR manually named o07
    And I create a VRF object from a IOS-XR SSH output named o08
    And I create a VRF object from a IOS-XR Netconf output named o09
    And I create a VRF object equals to Arista manually named o10
    And I create a VRF object from an Arista API output named o11
    And I create a VRF object from an Arista SSH output named o12
    And I create a VRF object from an Arista Netconf output named o13
    Then VRF object_01 should be equal to object_03
    And VRF object_01 should be equal to object_02
    And VRF object_02 should be equal to object_03
    And VRF object_02 should be equal to object_04
    And VRF object_02 should be equal to object_05
    And VRF object_02 should be equal to object_06
    And VRF object_04 should be equal to object_05
    And VRF object_04 should be equal to object_06
    And VRF object_02 should be equal to object_07
    And VRF object_02 should be equal to object_08
    And VRF object_07 should be equal to object_08
    And VRF object_02 should be equal to object_09
    And VRF object_07 should be equal to object_09
    And VRF object_08 should be equal to object_09