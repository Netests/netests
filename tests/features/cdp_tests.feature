# Created by dylan.hamel at 09.12.19
Feature: Test protocols CDP python class netests/protocols/cdp.py
    # Description
    Scenario:
        # Description
        # Arista Networks ID Device = o00
        Given A network protocols named CDP defined in netests/protocols/cdp.py
        And I create a CDP object equals to Arista manually named o0001
        And I create a CDP object from a Arista API output named o0002
        And I create a CDP object from a Arista Netconf named o0003
        And I create a CDP object from a Arista SSH output named o0004

        # Cumulus Networks ID Device = o01
        And I create a CDP object equals to Cumulus manually named o0101
        And I create a CDP object from a Cumulus API output named o0102
        And I create a CDP object from a Cumulus Netconf named o0103
        And I create a CDP object from a Cumulus SSH output named o0104

        # Extreme Networks VSP (VOSS) ID Device = o02
        And I create a CDP object equals to Extreme VSP manually named o0201
        And I create a CDP object from a Extreme VSP API output named o0202
        And I create a CDP object from a Extreme VSP Netconf output named o0203
        And I create a CDP object from a Extreme VSP SSH output named o0204

        # Cisco IOS-XE ID Device = o03
        And I create a CDP object equals to IOS manually named o0301
        And I create a CDP object from a IOS API output named o0302
        And I create a CDP object from a IOS Netconf named o0303
        And I create a CDP object from a IOS SSH named o0304

        # Cisco IOS-XR Device = o04
        And I create a CDP object equals to IOS-XR manually named o0401
        And I create a CDP object from a IOS-XR API output named o0402
        And I create a CDP object from a IOS-XR Netconf output named o403
        And I create a CDP object from a IOS-XR SSH output named o0404
        And I create a CDP object equals IOS-XR multi manually output named o0405
        And I create a CDP object from a IOS-XR multi Netconf output named o0406

        # Juniper Networks ID Device = o05
        And I create a CDP object equals to Juniper manually named o0501
        And I create a CDP object from a Juniper API output named o0502
        And I create a CDP object from a Juniper Netconf output named o0503
        And I create a CDP object from a Juniper SSH output named o0504

        # NAPALM-Automation Networks ID Device = o06
        And I create a CDP object equals to NAPALM manually named o0601
        And I create a CDP object from a NAPALM output named o0602

        # Cisco Nexus NXOS ID Device = o07
        And I create a CDP object equals to NXOS manually named o0701
        And I create a CDP object from a NXOS API output named o0702
        And I create a CDP object from a NXOS Netconf output named o0703
        And I create a CDP object from a NXOS SSH output named o0704

        And I create a CDP object equals to NXOS only one manually named o0711
        And I create a CDP object from a NXOS only one API output named o0712
        And I create a CDP object from a NXOS only one Netconf output named o0713
        And I create a CDP object from a NXOS only one SSH output named o0714

        # COMPARAISON
        # Arista Networks
        And CDP o0001 should be equal to o0002
        And CDP o0001 should be equal to o0003
        And CDP o0001 should be equal to o0004
        And CDP o0002 should be equal to o0003
        And CDP o0002 should be equal to o0004
        And CDP o0003 should be equal to o0004

        And CDP YAML file should be equal to o0002
        And CDP YAML file should be equal to o0003
        And CDP YAML file should be equal to o0004

        # Cumulus Networks
        And CDP o0101 should be equal to o0102
        And CDP o0101 should be equal to o0103
        And CDP o0101 should be equal to o0104
        And CDP o0102 should be equal to o0103
        And CDP o0102 should be equal to o0104
        And CDP o0103 should be equal to o0104

        And CDP YAML file should be equal to o0102
        And CDP YAML file should be equal to o0103
        And CDP YAML file should be equal to o0104

        # Extreme Networks VSP
        And CDP o0201 should be equal to o0202
        And CDP o0201 should be equal to o0203
        And CDP o0201 should be equal to o0204
        And CDP o0202 should be equal to o0203
        And CDP o0202 should be equal to o0204
        And CDP o0203 should be equal to o0204

        And CDP YAML file should be equal to o0202
        And CDP YAML file should be equal to o0203
        And CDP YAML file should be equal to o0204

        # Cisco IOS-XE
        And CDP o0301 should be equal to o0302
        And CDP o0301 should be equal to o0303
        And CDP o0301 should be equal to o0304
        And CDP o0302 should be equal to o0303
        And CDP o0302 should be equal to o0304
        And CDP o0303 should be equal to o0304

        And CDP YAML file should be equal to o0302
        And CDP YAML file should be equal to o0303
        And CDP YAML file should be equal to o0304

        # Cisco IOS-XR
        And CDP o0401 should be equal to o0402
        And CDP o0401 should be equal to o0403
        And CDP o0401 should be equal to o0404
        And CDP o0402 should be equal to o0403
        And CDP o0402 should be equal to o0404
        And CDP o0403 should be equal to o0404

        And CDP YAML file should be equal to o0402
        And CDP YAML file should be equal to o0403
        And CDP YAML file should be equal to o0404

        # Juniper Networks
        And CDP o0501 should be equal to o0502
        And CDP o0501 should be equal to o0503
        And CDP o0501 should be equal to o0504
        And CDP o0502 should be equal to o0503
        And CDP o0502 should be equal to o0504
        And CDP o0503 should be equal to o0504

        And CDP YAML file should be equal to o0502
        And CDP YAML file should be equal to o0503
        And CDP YAML file should be equal to o0504

        # NAPALM-Automation
        And CDP o0601 should be equal to o0602

        # Cisco Nexus NXOS
        And CDP o0701 should be equal to o0702
        And CDP o0701 should be equal to o0703
        And CDP o0701 should be equal to o0704
        And CDP o0702 should be equal to o0703
        And CDP o0702 should be equal to o0704
        And CDP o0703 should be equal to o0704

        And CDP YAML file should be equal to o0702
        And CDP YAML file should be equal to o0703
        And CDP YAML file should be equal to o0704

        And CDP o0711 should be equal to o0712
        And CDP o0711 should be equal to o0713
        And CDP o0711 should be equal to o0714
        And CDP o0712 should be equal to o0713
        And CDP o0712 should be equal to o0714
        And CDP o0713 should be equal to o0714

        # Test Filter compare function
        And I create a CDP object to test compare function named o9999

        And I create a CDP object to test compare function with <neighbor_os> named o9982
        And I create a CDP object to test compare equal to o9982 without <neighbor_os> named o9983
        And I compare CDP o9982 and o9999 with a personal function - should not work
        And I compare CDP o9983 and o9999 with a personal function - should work

        And I create a CDP object to test compare function with <neighbor_mgmt_ip> named o9984
        And I create a CDP object to test compare equal to o9984 without <neighbor_mgmt_ip> named o9985
        And I compare CDP o9984 and o9999 with a personal function - should not work
        And I compare CDP o9985 and o9999 with a personal function - should work

        And I create a CDP object to test compare function with <neighbor_type> named o9986
        And I create a CDP object to test compare equal to o9986 without <neighbor_type> named o9987
        And I compare CDP o9986 and o9999 with a personal function - should not work
        And I compare CDP o9987 and o9999 with a personal function - should work

        # By Protocols
        And I Finish my CDP tests and list tests not implemented