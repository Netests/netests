# Created by dylan.hamel at 07.12.19
Feature: Test function to set verbose mode ./functions/verbose_mode.py
    # Description
    Scenario:
        # Description
        Given I create a varibale with verbose mode level1
        And I create a varibale with verbose mode level2
        And I create a varibale with verbose mode level3
        And I create a varibale with verbose mode level4
        And I create a varibale with verbose mode level5
        Then I test that function with level1 works
        And I test that function with level2 works
        And I test that function with level3 works
        And I test that function with level4 works
        And I test that function with level5 works