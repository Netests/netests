# Created by dylan.hamel at 06.12.19

Feature: Test protocols MTU python class ./protocols/mtu.py
  # Description
  Scenario: Create three MTU objects
    # Description
    Given I create a MTU object with 4 interfaces named object_01
    And a JSON object with data to create a MTU object named object_02
    And a MTU object retrieve on a network device named object_03
    And I create a MTU python object from a Cumulus output command named object_04
    And I create a MTU python object from a Arista output command named object_05
    And I create a MTU python object from a Nexus output command named object_06
    Then object_01 should be equal to object_02
    And object_03 should be equal to a MTU defintion describe in verity file
    And MTU object_02 should not be equal to object_04
    And MTU object_04 should not be equal to object_05
    And MTU object_02 should not be equal to object_06
