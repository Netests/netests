# Created by dylan.hamel at 09.12.19
Feature: Test Class NetestsCLI
    # Description
    Scenario:
        Given I create a NetestsCLI object with Ansible parameters named cli
        And I print NetestsCLI object
        
        # Tests for HELP commands
        Then I can print help

        # Tests for SELECT & UNSELECT commands
        And I can print help for select command
        And I can print help for unselect command
        And I can select * devices
        And I can unselect * devices
        And I can select only one devices
        And I can unselect only one devices
        And I can select many devices
        And I can unselect many devices

        # Tests for SELECTED commands
        And I can print help for selected commands
        And I can use selected command

        # Tests for OPTIONS commands 
        And I can print help for options commands
        And I can use the options command with many class params
        And I can use the options command with * arguments

        # Tests for MORE commands
        And I can print help for more commands
        And I can use more command
        
        # Tests for SHOW commands
        And I can print help for show commands
        And I can use show command

        # Tests for PRINT commands 
        And I can print help for print commands
        And I can print * devices
        And I can print only one devices
        And I can print many devices

        # Tests for GET commands
        And I can print help for get commands
        And I simulate a GET VRF command.
        And I simulate a GET command without parameter - Error

        # Tests for COMPARE commands
        And I can print help for compare commands

        # Tests for EXIT commands
        And I can print help for exit commands