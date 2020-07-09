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