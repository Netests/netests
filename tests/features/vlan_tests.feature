Feature: Test protocols VLAN python class netests/protocols/vlan.py
    # Description
    Scenario:
        # Description
        # Arista Networks ID Device = o00
        Given A network protocols named VLAN defined in netests/protocols/vlan.py
        And I create a VLAN object equals to Arista manually named o0001
        And I create a VLAN object from a Arista API output named o0002
        And I create a VLAN object from a Arista Netconf named o0003
        And I create a VLAN object from a Arista SSH output named o0004

        # Cumulus Networks ID Device = o01
        And I create a VLAN object equals to Cumulus manually named o0101
        And I create a VLAN object from a Cumulus API output named o0102
        And I create a VLAN object from a Cumulus Netconf named o0103
        And I create a VLAN object from a Cumulus SSH output named o0104

        # Extreme Networks VSP (VOSS) ID Device = o02
        And I create a VLAN object equals to Extreme VSP manually named o0201
        And I create a VLAN object from a Extreme VSP API output named o0202
        And I create a VLAN object from a Extreme VSP Netconf output named o0203
        And I create a VLAN object from a Extreme VSP SSH output named o0204

        # Cisco IOS-XE ID Device = o03
        And I create a VLAN object equals to IOS manually named o0301
        And I create a VLAN object from a IOS API output named o0302
        And I create a VLAN object from a IOS Netconf named o0303
        And I create a VLAN object from a IOS SSH named o0304

        # Cisco IOS-XR Device = o04
        And I create a VLAN object equals to IOS-XR manually named o0401
        And I create a VLAN object from a IOS-XR API output named o0402
        And I create a VLAN object from a IOS-XR Netconf output named o403
        And I create a VLAN object from a IOS-XR SSH output named o0404

        # Juniper Networks ID Device = o05
        And I create a VLAN object equals to Juniper manually named o0501
        And I create a VLAN object from a Juniper API output named o0502
        And I create a VLAN object from a Juniper Netconf output named o0503
        And I create a VLAN object from a Juniper SSH output named o0504

        # NAPALM-Automation Networks ID Device = o06
        And I create a VLAN object equals to NAPALM manually named o0601
        And I create a VLAN object from a NAPALM output named o0602

        # Cisco Nexus NXOS ID Device = o07
        And I create a VLAN object equals to NXOS manually named o0701
        And I create a VLAN object from a NXOS API output named o0702
        And I create a VLAN object from a NXOS Netconf output named o0703
        And I create a VLAN object from a NXOS SSH output named o0704

        And I create a VLAN object equals to NXOS only one manually named o0711
        And I create a VLAN object from a NXOS only one API output named o0712
        And I create a VLAN object from a NXOS only one Netconf output named o0713
        And I create a VLAN object from a NXOS only one SSH output named o0714

        # COMPARAISON
        # Arista Networks
        And VLAN o0001 should be equal to o0002
        And VLAN o0001 should be equal to o0003
        And VLAN o0001 should be equal to o0004
        And VLAN o0002 should be equal to o0003
        And VLAN o0002 should be equal to o0004
        And VLAN o0003 should be equal to o0004

        And VLAN YAML file should be equal to o0002
        And VLAN YAML file should be equal to o0003
        And VLAN YAML file should be equal to o0004

        # Cumulus Networks
        And VLAN o0101 should be equal to o0102
        And VLAN o0101 should be equal to o0103
        And VLAN o0101 should be equal to o0104
        And VLAN o0102 should be equal to o0103
        And VLAN o0102 should be equal to o0104
        And VLAN o0103 should be equal to o0104

        And VLAN YAML file should be equal to o0102
        And VLAN YAML file should be equal to o0103
        And VLAN YAML file should be equal to o0104

        # Extreme Networks VSP
        And VLAN o0201 should be equal to o0202
        And VLAN o0201 should be equal to o0203
        And VLAN o0201 should be equal to o0204
        And VLAN o0202 should be equal to o0203
        And VLAN o0202 should be equal to o0204
        And VLAN o0203 should be equal to o0204

        And VLAN YAML file should be equal to o0202
        And VLAN YAML file should be equal to o0203
        And VLAN YAML file should be equal to o0204

        # Cisco IOS-XE
        And VLAN o0301 should be equal to o0302
        And VLAN o0301 should be equal to o0303
        And VLAN o0301 should be equal to o0304
        And VLAN o0302 should be equal to o0303
        And VLAN o0302 should be equal to o0304
        And VLAN o0303 should be equal to o0304

        And VLAN YAML file should be equal to o0302
        And VLAN YAML file should be equal to o0303
        And VLAN YAML file should be equal to o0304

        # Cisco IOS-XR
        And VLAN o0401 should be equal to o0402
        And VLAN o0401 should be equal to o0403
        And VLAN o0401 should be equal to o0404
        And VLAN o0402 should be equal to o0403
        And VLAN o0402 should be equal to o0404
        And VLAN o0403 should be equal to o0404

        And VLAN YAML file should be equal to o0402
        And VLAN YAML file should be equal to o0403
        And VLAN YAML file should be equal to o0404

        # Juniper Networks
        And VLAN o0501 should be equal to o0502
        And VLAN o0501 should be equal to o0503
        And VLAN o0501 should be equal to o0504
        And VLAN o0502 should be equal to o0503
        And VLAN o0502 should be equal to o0504
        And VLAN o0503 should be equal to o0504

        And VLAN YAML file should be equal to o0502
        And VLAN YAML file should be equal to o0503
        And VLAN YAML file should be equal to o0504

        # NAPALM-Automation
        And VLAN o0601 should be equal to o0602

        # Cisco Nexus NXOS
        And VLAN o0701 should be equal to o0702
        And VLAN o0701 should be equal to o0703
        And VLAN o0701 should be equal to o0704
        And VLAN o0702 should be equal to o0703
        And VLAN o0702 should be equal to o0704
        And VLAN o0703 should be equal to o0704

        And VLAN YAML file should be equal to o0702
        And VLAN YAML file should be equal to o0703
        And VLAN YAML file should be equal to o0704

        And VLAN o0711 should be equal to o0712
        And VLAN o0711 should be equal to o0713
        And VLAN o0711 should be equal to o0714
        And VLAN o0712 should be equal to o0713
        And VLAN o0712 should be equal to o0714
        And VLAN o0713 should be equal to o0714

        # Test Filter compare function
        And I create a VLAN object to test compare function named o9999

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

        # By Protocols
        And I Finish my VLAN tests and list tests not implemented