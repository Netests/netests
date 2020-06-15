Feature: Test protocols IPAddress, IPV4 and IPV6
    # Description
    Scenario:
        Given I create a IPAddress object named o0000
        And I create a IPV4 object named o0001
        And I create a wrong IPV4 object named o0002
        And I create a IPV4Interface named o0003
        And I create a wrong IPV4Interface named o0004
        And I create a IPAddress object named o0010
        And I create a IPV6 object named o0011
        And I create a wrong IPV6 object named o0012
        Then I can print IPAddress object o0000
        And I can print IPAddress object o0000 in JSON format
        And I can print IPV4 object o0001
        And I can print IPV4 object o0001 in JSON format
        And I can print IPV4 object o0003 in JSON format
        And I can print IPV6 object o0011
        And I can print IPV6 object o0011 in JSON format
        And IPAddress object o0000 is equal to IPV4 object o0001