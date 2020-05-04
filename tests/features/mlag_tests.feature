# Created by dylan.hamel at 11.12.19
Feature: Test protocols MLAG python class ./protocols/mlag.py
  # Description
  Scenario:
    # Description
    Given I create an MLAG python object corresponding to Cumulus device manually named object_01
    And I retrieve data from a YAML file corresponding to devices to create an MLAG python object named object_02
    And I create an MLAG python object from a Cumulus output command named object_03
    # Add device
    Then MLAG object_01 should be equal to object_02
    And MLAG object_01 should be equal to object_03
    And MLAG object_03 should be equal to object_01