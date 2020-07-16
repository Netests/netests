Feature: Test protocols ISIS
    # Description
    Scenario: Tests ISISAdjcency class
        Given I create a ISISAdjacency object named o0000
        Then I can print ISISAdjacency object named o0000
        And I can print ISISAdjacency object named o0000 in JSON format
        And I can print ISISAdjacency object named o0000 in dict format

    Scenario: Tests ListISISAdjcency class
        Given I create a ListISISAdjcency object named o0001
        Then I can print ListISISAdjcency object named o0001
        And I can print ListISISAdjcency object named o0001 in JSON format
        And I can print ListISISAdjcency object named o0001 in dict format

    Scenario: Tests ISISAdjcencyVRF class
        Given I create a ISISAdjcencyVRF object named o0002
        Then I can print ISISAdjcencyVRF object named o0002
        And I can print ISISAdjcencyVRF object named o0002 in JSON format
        And I can print ISISAdjcencyVRF object named o0002 in dict format

    Scenario: Verify that filter for compare and print works
        Then I create a ISISAdjacency object to test compare function named o9999

        And I create a ISISAdjacency object to test compare function with <circuit_type> named o9982
        And I create a ISISAdjacency object to test compare equal to o9982 without <circuit_type> named o9983
        And I compare ISISAdjacency o9982 and o9999 with a personal function - should not work
        And I compare ISISAdjacency o9983 and o9999 with a personal function - should work

        And I create a ISISAdjacency object to test compare function with <local_interface_name> named o9984
        And I create a ISISAdjacency object to test compare equal to o9984 without <local_interface_name> named o9985
        And I compare ISISAdjacency o9984 and o9999 with a personal function - should not work
        And I compare ISISAdjacency o9985 and o9999 with a personal function - should work

        And I create a ISISAdjacency object to test compare function with <neighbor_ip_addr> named o9986
        And I create a ISISAdjacency object to test compare equal to o9986 without <neighbor_ip_addr> named o9987
        And I compare ISISAdjacency o9986 and o9999 with a personal function - should not work
        And I compare ISISAdjacency o9987 and o9999 with a personal function - should work

        And I create a ISISAdjacency object to test compare function with <snap> named o9988
        And I create a ISISAdjacency object to test compare equal to o9988 without <snap> named o9989
        And I compare ISISAdjacency o9988 and o9999 with a personal function - should not work
        And I compare ISISAdjacency o9989 and o9999 with a personal function - should work