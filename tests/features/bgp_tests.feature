# Created by dylan.hamel at 09.12.19
Feature: Test protocols BGP python class ./protocols/bgp.py
  # Description
  Scenario:
    # Description
    # Arista Networks ID Device = o00
    Given A network protocols named BGP defined in protocols/bgp.py
    And I create a BGP object equals to Arista manually named o0001
    And I create a BGP object from a Arista API output named o0002
    And I create a BGP object from a Arista Netconf named o0003
    And I create a BGP object from a Arista SSH output named o0004
    # Cumulus Networks ID Device = o01
    And I create a BGP object equals to Cumulus manually named o0101
    And I create a BGP object from a Cumulus API output named o0102
    And I create a BGP object from a Cumulus Netconf named o0103
    And I create a BGP object from a Cumulus SSH output named o0104
    # Extreme Networks VSP (VOSS) ID Device = o02
    And I create a BGP object equals to Extreme VSP manually named o0201
    And I create a BGP object from a Extreme VSP API output named o0202
    And I create a BGP object from a Extreme VSP Netconf output named o0203
    And I create a BGP object from a Extreme VSP SSH output named o0204
    # Cisco IOS-XE ID Device = o03
    And I create a BGP object equals to IOS manually named o0301
    And I create a BGP object from a IOS API output named o0302
    And I create a BGP object from a IOS Netconf named o0303
    And I create a BGP object from a IOS SSH named o0304

    # Cisco IOS-XR Device = o04
    And I create a BGP object equals to IOS-XR manually named o0401
    And I create a BGP object from a IOS-XR API output named o0402
    And I create a BGP object from a IOS-XR Netconf output named o403
    And I create a BGP object from a IOS-XR SSH output named o0404
    And I create a BGP object equals IOS-XR multi manually output named o0405
    And I create a BGP object from a IOS-XR multi Netconf output named o0406
    # Juniper Networks ID Device = o05
    And I create a BGP object equals to Juniper manually named o0501
    And I create a BGP object from a Juniper API output named o0502
    And I create a BGP object from a Juniper Netconf output named o0503
    And I create a BGP object from a Juniper SSH output named o0504
    # NAPALM-Automation Networks ID Device = o06
    And I create a BGP object equals to NAPALM manually named o0601
    And I create a BGP object from a NAPALM output named o0602
    # Cisco Nexus NXOS ID Device = o07
    And I create a BGP object equals to NXOS manually named o0701
    And I create a BGP object from a NXOS API output named o0702
    And I create a BGP object from a NXOS Netconf output named o0703
    And I create a BGP object from a NXOS SSH output named o0704

    # COMPARAISON
    # Arista Networks
    And BGP o0001 should be equal to o0002
    And BGP o0001 should be equal to o0003
    And BGP o0001 should be equal to o0004
    And BGP o0002 should be equal to o0003
    And BGP o0002 should be equal to o0004
    And BGP o0003 should be equal to o0004

    And BGP YAML file should be equal to o0002
    And BGP YAML file should be equal to o0003
    And BGP YAML file should be equal to o0004
    # Cumulus Networks
    And BGP o0101 should be equal to o0102
    And BGP o0101 should be equal to o0103
    And BGP o0101 should be equal to o0104
    And BGP o0102 should be equal to o0103
    And BGP o0102 should be equal to o0104
    And BGP o0103 should be equal to o0104

    And BGP YAML file should be equal to o0102
    And BGP YAML file should be equal to o0103
    And BGP YAML file should be equal to o0104
    # Extreme Networks VSP
    And BGP o0201 should be equal to o0202
    And BGP o0201 should be equal to o0203
    And BGP o0201 should be equal to o0204
    And BGP o0202 should be equal to o0203
    And BGP o0202 should be equal to o0204
    And BGP o0203 should be equal to o0204

    And BGP YAML file should be equal to o0202
    And BGP YAML file should be equal to o0203
    And BGP YAML file should be equal to o0204
    # Cisco IOS-XE
    And BGP o0301 should be equal to o0302
    And BGP o0301 should be equal to o0303
    And BGP o0301 should be equal to o0304
    And BGP o0302 should be equal to o0303
    And BGP o0302 should be equal to o0304
    And BGP o0303 should be equal to o0304

    And BGP YAML file should be equal to o0302
    And BGP YAML file should be equal to o0303
    And BGP YAML file should be equal to o0304
    # Cisco IOS-XR
    And BGP o0401 should be equal to o0402
    And BGP o0401 should be equal to o0403
    And BGP o0401 should be equal to o0404
    And BGP o0402 should be equal to o0403
    And BGP o0402 should be equal to o0404
    And BGP o0403 should be equal to o0404
    # Multiple BGP
    And BGP o0405 should be equal to o0406

    And BGP YAML file should be equal to o0402
    And BGP YAML file should be equal to o0403
    And BGP YAML file should be equal to o0404
    # Juniper Networks
    And BGP o0501 should be equal to o0502
    And BGP o0501 should be equal to o0503
    And BGP o0501 should be equal to o0504
    And BGP o0502 should be equal to o0503
    And BGP o0502 should be equal to o0504
    And BGP o0503 should be equal to o0504

    And BGP YAML file should be equal to o0502
    And BGP YAML file should be equal to o0503
    And BGP YAML file should be equal to o0504
    # NAPALM-Automation
    And BGP o0601 should be equal to o0602

    # Cisco Nexus NXOS
    And BGP o0701 should be equal to o0702
    And BGP o0701 should be equal to o0703
    And BGP o0701 should be equal to o0704
    And BGP o0702 should be equal to o0703
    And BGP o0702 should be equal to o0704
    And BGP o0703 should be equal to o0704

    And BGP YAML file should be equal to o0702
    And BGP YAML file should be equal to o0703
    And BGP YAML file should be equal to o0704
    # By Protocols
    And I Finish my BGP tests and list tests not implemented