# Created by dylan.hamel at 07.12.19
Feature: Test protocols Static python class ./protocols/static.py
  # Description
  Scenario:
    # Description
    Given I create a Static python object manually named object_01
    And I retrieve data from a YAML file to create a Static python object named object_02
    And I create a Static python object from a Arista output command named object_03
    Then Static object_01 should be equal to object_02
    And Static object_01 should be equal to object_03
    And Static object_02 should be equal to object_03
