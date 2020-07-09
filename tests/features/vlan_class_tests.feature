Feature: Test protocols VLAN
    # Description
    Scenario:
        Given I create a VLAN object named o0000
        Then I can print VLAN object named o0000
        And I can print VLAN object named o0000 in JSON format

    Scenario:
        Then I create a VLAN object to test compare function named o9999

        And I create a VLAN object to test compare function with <name> named o9982
        And I create a VLAN object to test compare equal to o9982 without <name> named o9983
        And I compare VLAN o9982 and o9999 with a personal function - should not work
        And I compare VLAN o9983 and o9999 with a personal function - should work

        And I create a VLAN object to test compare function with <vrf_name> named o9984
        And I create a VLAN object to test compare equal to o9984 without <vrf_name> named o9985
        And I compare VLAN o9984 and o9999 with a personal function - should not work
        And I compare VLAN o9985 and o9999 with a personal function - should work

        And I create a VLAN object to test compare function with <ipv4_addresses> named o9986
        And I create a VLAN object to test compare equal to o9986 without <ipv4_addresses> named o9987
        And I compare VLAN o9986 and o9999 with a personal function - should not work
        And I compare VLAN o9987 and o9999 with a personal function - should work

        And I create a VLAN object to test compare function with <ipv6_addresses> named o9988
        And I create a VLAN object to test compare equal to o9988 without <ipv6_addresses> named o9989
        And I compare VLAN o9988 and o9999 with a personal function - should not work
        And I compare VLAN o9989 and o9999 with a personal function - should work

        And I create a VLAN object to test compare function with <assigned_ports> named o9990
        And I create a VLAN object to test compare equal to o9990 without <assigned_ports> named o9991
        And I compare VLAN o9990 and o9999 with a personal function - should not work
        And I compare VLAN o9991 and o9999 with a personal function - should work