Feature: Test protocols IPV4 python class netests/protocols/ipv4.py
    # Description
    Scenario:
        Given I create a IPAddress object named o0000
        And I create a IPV4 object named o0001
        Then I can print IPAddress object o0000
        And I can print IPAddress object o0000 in JSON format
        And I can print IPV4 object o0001
        And I can print IPV4 object o0001 in JSON format
        And IPAddress object o0000 is equal to IPV4 object o0001