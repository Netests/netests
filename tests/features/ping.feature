# Created by dylan.hamel at 09.05.2020
Feature: Test protocols PING python class ./protocols/ping.py
    # Description
    Scenario:
        # Description
        # Arista Networks ID Device = o00
        Given A Ping output from a Arista CLI that works named o0001
        And A Ping output from a Arista CLI with wrong VRF named o0002
        And A Ping output from a Arista CLI with wrong IPv4 named o0003
        And A Ping output from a Arista CLI with unreachable IPv4 named o0004
        And A Ping output from a Arista CLI with no route to IPv4 named o0005

        And A Ping output from a Arista API that works named o0011
        And A Ping output from a Arista API with wrong VRF named o0012
        And A Ping output from a Arista API with wrong IPv4 named o0013
        And A Ping output from a Arista API with unreachable IPv4 named o0014
        And A Ping output from a Arista API with no route to IPv4 named o0015

        
        # COMPARAISON
        # Arista Networks
        And Ping Arista CLI works does named o0001 not raise an Exception
        And Ping Arista CLI wrong VRF named o0002 raise an Exception
        And Ping Arista CLI wrong IPv4 named o0003 raise an Exception
        And Ping Arista CLI unreachable named o0004 raise an Exception
        And Ping Arista CLI no route named o0005 raise an Exception

        And Ping Arista API works does named o0011 not raise an Exception
        And Ping Arista API wrong VRF named o0012 raise an Exception
        And Ping Arista API wrong IPv4 named o0013 raise an Exception
        And Ping Arista API unreachable named o0014 raise an Exception
        And Ping Arista API no route named o0015 raise an Exception