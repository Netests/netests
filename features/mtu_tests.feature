# Created by dylan.hamel at 06.12.19

Feature: Test protocols MTU python class ./protocols/mtu.py
  Scenario: Create two MTU objects
    Given I create a MTU object with 4 interfaces named object_01
    And a JSON object with data to create a MTU object named object_02
    And a MTU object retrieve on a network device named object_03
    Then object_01 should be equal to object_02
    And object_03 should be equal to a MTU defintion describe in verity file
