# Created by dylan.hamel at 09.12.19
Feature: Test Class NetestsCLI
    # Description
    Scenario:
        Given I create a NetestsCLI object with Ansible parameters named cli
        And I print NetestsCLI object
        
        # Print HELP xxx
        Then I can print help
        And I can print help for options commands

        # Tests Commands
        And I simulate a GET VRF command.

        # Tests ERROR Commands
        And I simulate a GET command without parameter.