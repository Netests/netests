# Created by dylan.hamel at 08.12.19
Feature: Test protocols SystemInfos python class ./protocols/infos.py
  # Enter feature description here

  Scenario: # Enter scenario name here
    # Enter steps here
    Given I create a SystemInfos python object manually named object_01
    And I retrieve data from a YAML file to create a SystemInfos python object named object_02
    And I create a SystemInfos python object from a Nexus output command named object_03
    Then SystemInfos object_01 should be equal to object_02
    And SystemInfos object_01 should be equal to object_03
    And SystemInfos object_02 should be equal to object_03