# Created by dylan.hamel at 09.05.2020
Feature: Test protocols PING python class ./protocols/ping.py
    # Description
    Scenario:
        # Description
        Given A network protocols named PING defined in protocols/ping.py

        # Arista Networks ID Device = o00
        And A Ping output from a Arista CLI that works named o0001
        And A Ping output from a Arista CLI with wrong VRF named o0002
        And A Ping output from a Arista CLI with wrong IPv4 named o0003
        And A Ping output from a Arista CLI with unreachable IPv4 named o0004
        And A Ping output from a Arista CLI with no route to IPv4 named o0005

        And A Ping output from a Arista API that works named o0011
        And A Ping output from a Arista API with wrong VRF named o0012
        And A Ping output from a Arista API with wrong IPv4 named o0013
        And A Ping output from a Arista API with unreachable IPv4 named o0014
        And A Ping output from a Arista API with no route to IPv4 named o0015

        # Cumulus Networks ID Device = o01
        And A Ping output from a Cumulus CLI that works named o0101
        And A Ping output from a Cumulus CLI with wrong VRF named o0102
        And A Ping output from a Cumulus CLI with wrong IPv4 named o0103
        And A Ping output from a Cumulus CLI with unreachable IPv4 named o0104
        And A Ping output from a Cumulus CLI with no route to IPv4 named o0105

        # Extreme Networks VSP ID Device = o02
        And A Ping output from a Extreme VSP CLI that works named o0201
        And A Ping output from a Extreme VSP CLI with wrong VRF named o0202
        And A Ping output from a Extreme VSP CLI with wrong IPv4 named o0203
        And A Ping output from a Extreme VSP CLI with unreachable IPv4 named o0204
        And A Ping output from a Extreme VSP CLI with no route to IPv4 named o0205

        # Cisco IOS-XR ID Device = o03
        And A Ping output from a Cisco IOS-XE CLI that works named o0301
        And A Ping output from a Cisco IOS-XE CLI with wrong VRF named o0302
        And A Ping output from a Cisco IOS-XE CLI with wrong IPv4 named o0303
        And A Ping output from a Cisco IOS-XE CLI with unreachable IPv4 named o0304
        And A Ping output from a Cisco IOS-XE CLI with no route to IPv4 named o0305
        And A Ping output from a Cisco IOS-XE CLI with no src ip to IPv4 named o0306
        And A Ping output from a Cisco IOS-XE CLI with no vrf config to IPv4 named o0307

        # Cisco IOS-XR ID Device = o04
        And A Ping output from a Cisco IOS-XR CLI that works named o0401
        And A Ping output from a Cisco IOS-XR CLI with wrong VRF named o0402
        And A Ping output from a Cisco IOS-XR CLI with wrong IPv4 named o0403
        And A Ping output from a Cisco IOS-XR CLI with unreachable IPv4 named o0404
        And A Ping output from a Cisco IOS-XR CLI with no route to IPv4 named o0405

        And A Ping output from a Cisco IOS-XR Netconf that works named o0411
        And A Ping output from a Cisco IOS-XR Netconf with wrong VRF named o0412
        And A Ping output from a Cisco IOS-XR Netconf with wrong IPv4 named o0413
        And A Ping output from a Cisco IOS-XR Netconf with unreachable IPv4 named o0414
        And A Ping output from a Cisco IOS-XR Netconf with no route to IPv4 named o0415

        # Cisco IOS-XR ID Device = o04
        And A Ping output from a Cisco NXOS CLI that works named o0501
        And A Ping output from a Cisco NXOS CLI with wrong VRF named o0502
        And A Ping output from a Cisco NXOS CLI with wrong IPv4 named o0503
        And A Ping output from a Cisco NXOS CLI with unreachable IPv4 named o0504
        And A Ping output from a Cisco NXOS CLI with no route to IPv4 named o0505

        And A Ping output from a Cisco NXOS Netconf that works named o0511
        And A Ping output from a Cisco NXOS Netconf with wrong VRF named o0512
        And A Ping output from a Cisco NXOS Netconf with wrong IPv4 named o0513
        And A Ping output from a Cisco NXOS Netconf with unreachable IPv4 named o0514
        And A Ping output from a Cisco NXOS Netconf with no route to IPv4 named o0515
        
        # COMPARAISON
        # Arista Networks
        And Ping Arista CLI works does named o0001 not raise an Exception
        And Ping Arista CLI wrong VRF named o0002 raise an Exception
        And Ping Arista CLI wrong IPv4 named o0003 raise an Exception
        And Ping Arista CLI unreachable named o0004 raise an Exception
        And Ping Arista CLI no route named o0005 raise an Exception

        And Ping Arista CLI works does named o0001 not raise an Exception reverse
        And Ping Arista CLI wrong VRF named o0002 raise an Exception reverse
        And Ping Arista CLI wrong IPv4 named o0003 raise an Exception reverse
        And Ping Arista CLI unreachable named o0004 raise an Exception reverse
        And Ping Arista CLI no route named o0005 raise an Exception reverse

        And Ping Arista API works does named o0011 not raise an Exception
        And Ping Arista API wrong VRF named o0012 raise an Exception
        And Ping Arista API wrong IPv4 named o0013 raise an Exception
        And Ping Arista API unreachable named o0014 raise an Exception
        And Ping Arista API no route named o0015 raise an Exception

        And Ping Arista API works does named o0011 not raise an Exception reverse
        And Ping Arista API wrong VRF named o0012 raise an Exception reverse
        And Ping Arista API wrong IPv4 named o0013 raise an Exception reverse
        And Ping Arista API unreachable named o0014 raise an Exception reverse
        And Ping Arista API no route named o0015 raise an Exception reverse

        # Cumulus Networks
        And Ping Cumulus CLI works does named o0101 not raise an Exception
        And Ping Cumulus CLI wrong VRF named o0102 raise an Exception
        And Ping Cumulus CLI wrong IPv4 named o0103 raise an Exception
        And Ping Cumulus CLI unreachable named o0104 raise an Exception
        And Ping Cumulus CLI no route named o0105 raise an Exception

        # Extreme Networks
        And Ping Extreme VSP CLI works does named o0201 not raise an Exception
        And Ping Extreme VSP CLI wrong VRF named o0202 raise an Exception
        And Ping Extreme VSP CLI wrong IPv4 named o0203 raise an Exception
        And Ping Extreme VSP CLI unreachable named o0204 raise an Exception
        And Ping Extreme VSP CLI no route named o0205 raise an Exception

        And Ping Extreme VSP CLI works does named o0201 not raise an Exception reverse
        And Ping Extreme VSP CLI wrong VRF named o0202 raise an Exception reverse
        And Ping Extreme VSP CLI wrong IPv4 named o0203 raise an Exception reverse
        And Ping Extreme VSP CLI unreachable named o0204 raise an Exception reverse
        And Ping Extreme VSP CLI no route named o0205 raise an Exception reverse

        # Cisco IOS-XE
        And Ping Cisco IOS-XE CLI works does named o0301 not raise an Exception
        And Ping Cisco IOS-XE CLI wrong VRF named o0302 raise an Exception
        And Ping Cisco IOS-XE CLI wrong IPv4 named o0303 raise an Exception
        And Ping Cisco IOS-XE CLI unreachable named o0304 raise an Exception
        And Ping Cisco IOS-XE CLI no route named o0305 raise an Exception
        And Ping Cisco IOS-XE CLI no src ip named o0306 raise an Exception
        And Ping Cisco IOS-XE CLI no vrf config named o0307 raise an Exception

        And Ping Cisco IOS-XE CLI works does named o0301 not raise an Exception reverse
        And Ping Cisco IOS-XE CLI wrong VRF named o0302 raise an Exception reverse
        And Ping Cisco IOS-XE CLI wrong IPv4 named o0303 raise an Exception reverse
        And Ping Cisco IOS-XE CLI unreachable named o0304 raise an Exception reverse
        And Ping Cisco IOS-XE CLI no route named o0305 raise an Exception reverse
        And Ping Cisco IOS-XE CLI no src ip named o0306 raise an Exception reverse
        And Ping Cisco IOS-XE CLI no vrf config named o0307 raise an Exception reverse

        # Cisco IOS-XR
        And Ping Cisco IOS-XR CLI works does named o0401 not raise an Exception
        And Ping Cisco IOS-XR CLI wrong VRF named o0402 raise an Exception
        And Ping Cisco IOS-XR CLI wrong IPv4 named o0403 raise an Exception
        And Ping Cisco IOS-XR CLI unreachable named o0404 raise an Exception
        And Ping Cisco IOS-XR CLI no route named o0405 raise an Exception

        And Ping Cisco IOS-XR CLI works does named o0401 not raise an Exception reverse
        And Ping Cisco IOS-XR CLI wrong VRF named o0402 raise an Exception reverse
        And Ping Cisco IOS-XR CLI wrong IPv4 named o0403 raise an Exception reverse
        And Ping Cisco IOS-XR CLI unreachable named o0404 raise an Exception reverse
        And Ping Cisco IOS-XR CLI no route named o0405 raise an Exception reverse

        And Ping Cisco IOS-XR Netconf works does named o0411 not raise an Exception
        And Ping Cisco IOS-XR Netconf wrong VRF named o0412 raise an Exception
        And Ping Cisco IOS-XR Netconf wrong IPv4 named o0413 raise an Exception
        And Ping Cisco IOS-XR Netconf unreachable named o0414 raise an Exception
        And Ping Cisco IOS-XR Netconf no route named o0415 raise an Exception

        And Ping Cisco IOS-XR Netconf works does named o0411 not raise an Exception reverse
        And Ping Cisco IOS-XR Netconf wrong VRF named o0412 raise an Exception reverse
        And Ping Cisco IOS-XR Netconf wrong IPv4 named o0413 raise an Exception reverse
        And Ping Cisco IOS-XR Netconf unreachable named o0414 raise an Exception reverse
        And Ping Cisco IOS-XR Netconf no route named o0415 raise an Exception reverse

        # Cisco NXOS
        And Ping Cisco NXOS CLI works does named o0501 not raise an Exception
        And Ping Cisco NXOS CLI wrong VRF named o0502 raise an Exception
        And Ping Cisco NXOS CLI wrong IPv4 named o0503 raise an Exception
        And Ping Cisco NXOS CLI unreachable named o0504 raise an Exception
        And Ping Cisco NXOS CLI no route named o0505 raise an Exception

        And Ping Cisco NXOS CLI works does named o0501 not raise an Exception reverse
        And Ping Cisco NXOS CLI wrong VRF named o0502 raise an Exception reverse
        And Ping Cisco NXOS CLI wrong IPv4 named o0503 raise an Exception reverse
        And Ping Cisco NXOS CLI unreachable named o0504 raise an Exception reverse
        And Ping Cisco NXOS CLI no route named o0505 raise an Exception reverse

        And Ping Cisco NXOS Netconf works does named o0511 not raise an Exception
        And Ping Cisco NXOS Netconf wrong VRF named o0512 raise an Exception
        And Ping Cisco NXOS Netconf wrong IPv4 named o0513 raise an Exception
        And Ping Cisco NXOS Netconf unreachable named o0514 raise an Exception
        And Ping Cisco NXOS Netconf no route named o0515 raise an Exception

        And Ping Cisco NXOS Netconf works does named o0511 not raise an Exception reverse
        And Ping Cisco NXOS Netconf wrong VRF named o0512 raise an Exception reverse
        And Ping Cisco NXOS Netconf wrong IPv4 named o0513 raise an Exception reverse
        And Ping Cisco NXOS Netconf unreachable named o0514 raise an Exception reverse
        And Ping Cisco NXOS Netconf no route named o0515 raise an Exception reverse