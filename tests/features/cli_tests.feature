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
        And I can use selected command

        # Tests for OPTIONS commands 
        And I can print help for options commands

        # Tests for PRINT commands 
        And I can print help for print commands
        And I can print * devices
        And I can print only one devices
        And I can print many devices

        # Tests for GET commands
        And I simulate a GET VRF command.
        And I simulate a GET command without parameter.