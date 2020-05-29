# Created by dylan.hamel at 09.12.19
Feature: Test protocols OSPF python class netests/protocols/bgp.py
  # Description
  Scenario:
    # Description
    # Arista Networks ID Device = o00
    Given A network protocols named OSPF defined in netests/protocols/bgp.py
    And I create a OSPF object equals to Arista manually named o0001
    And I create a OSPF object from a Arista API output named o0002
    And I create a OSPF object from a Arista Netconf named o0003
    And I create a OSPF object from a Arista SSH output named o0004
    
    # Cumulus Networks ID Device = o01
    And I create a OSPF object equals to Cumulus manually named o0101
    And I create a OSPF object from a Cumulus API output named o0102
    And I create a OSPF object from a Cumulus Netconf named o0103
    And I create a OSPF object from a Cumulus SSH output named o0104
    
    # Extreme Networks VSP (VOSS) ID Device = o02
    And I create a OSPF object equals to Extreme VSP manually named o0201
    And I create a OSPF object from a Extreme VSP API output named o0202
    And I create a OSPF object from a Extreme VSP Netconf output named o0203
    And I create a OSPF object from a Extreme VSP SSH output named o0204
    
    # Cisco IOS-XE ID Device = o03
    And I create a OSPF object equals to IOS manually named o0301
    And I create a OSPF object from a IOS API output named o0302
    And I create a OSPF object from a IOS Netconf named o0303
    And I create a OSPF object from a IOS SSH named o0304

    # Cisco IOS-XR Device = o04
    And I create a OSPF object equals to IOS-XR manually named o0401
    And I create a OSPF object from a IOS-XR API output named o0402
    And I create a OSPF object from a IOS-XR Netconf output named o0403
    And I create a OSPF object from a IOS-XR SSH output named o0404
    And I create a OSPF object equals IOS-XR multi manually output named o0405
    And I create a OSPF object from a IOS-XR multi Netconf output named o0406

    # Juniper Networks ID Device = o05
    And I create a OSPF object equals to Juniper manually named o0501
    And I create a OSPF object from a Juniper API output named o0502
    And I create a OSPF object from a Juniper Netconf output named o0503
    And I create a OSPF object from a Juniper SSH output named o0504
    
    # NAPALM-Automation Networks ID Device = o06
    And I create a OSPF object equals to NAPALM manually named o0601
    And I create a OSPF object from a NAPALM output named o0602
    
    # Cisco Nexus NXOS ID Device = o07
    And I create a OSPF object equals to NXOS manually named o0701
    And I create a OSPF object from a NXOS API output named o0702
    And I create a OSPF object from a NXOS Netconf output named o0703
    And I create a OSPF object from a NXOS SSH output named o0704

    # COMPARAISON
    # Arista Networks
    And OSPF o0001 should be equal to o0002
    And OSPF o0001 should be equal to o0003
    And OSPF o0001 should be equal to o0004
    And OSPF o0002 should be equal to o0003
    And OSPF o0002 should be equal to o0004
    And OSPF o0003 should be equal to o0004

    And OSPF YAML file should be equal to o0002
    And OSPF YAML file should be equal to o0003
    And OSPF YAML file should be equal to o0004
    
    # Cumulus Networks
    And OSPF o0101 should be equal to o0102
    And OSPF o0101 should be equal to o0103
    And OSPF o0101 should be equal to o0104
    And OSPF o0102 should be equal to o0103
    And OSPF o0102 should be equal to o0104
    And OSPF o0103 should be equal to o0104

    And OSPF YAML file should be equal to o0102
    And OSPF YAML file should be equal to o0103
    And OSPF YAML file should be equal to o0104
    
    # Extreme Networks VSP
    And OSPF o0201 should be equal to o0202
    And OSPF o0201 should be equal to o0203
    And OSPF o0201 should be equal to o0204
    And OSPF o0202 should be equal to o0203
    And OSPF o0202 should be equal to o0204
    And OSPF o0203 should be equal to o0204

    And OSPF YAML file should be equal to o0202
    And OSPF YAML file should be equal to o0203
    And OSPF YAML file should be equal to o0204
    
    # Cisco IOS-XE
    And OSPF o0301 should be equal to o0302
    And OSPF o0301 should be equal to o0303
    And OSPF o0301 should be equal to o0304
    And OSPF o0302 should be equal to o0303
    And OSPF o0302 should be equal to o0304
    And OSPF o0303 should be equal to o0304

    And OSPF YAML file should be equal to o0302
    And OSPF YAML file should be equal to o0303
    And OSPF YAML file should be equal to o0304

    # Cisco IOS-XR
    And OSPF o0401 should be equal to o0402
    And OSPF o0401 should be equal to o0403
    And OSPF o0401 should be equal to o0404
    And OSPF o0402 should be equal to o0403
    And OSPF o0402 should be equal to o0404
    And OSPF o0403 should be equal to o0404

    And OSPF YAML file should be equal to o0402
    And OSPF YAML file should be equal to o0403
    And OSPF YAML file should be equal to o0404
    
    # Juniper Networks
    And OSPF o0501 should be equal to o0502
    And OSPF o0501 should be equal to o0503
    And OSPF o0501 should be equal to o0504
    And OSPF o0502 should be equal to o0503
    And OSPF o0502 should be equal to o0504
    And OSPF o0503 should be equal to o0504

    And OSPF YAML file should be equal to o0502
    And OSPF YAML file should be equal to o0503
    And OSPF YAML file should be equal to o0504
    
    # NAPALM-Automation
    And OSPF o0601 should be equal to o0602

    # Cisco Nexus NXOS
    And OSPF o0701 should be equal to o0702
    And OSPF o0701 should be equal to o0703
    And OSPF o0701 should be equal to o0704
    And OSPF o0702 should be equal to o0703
    And OSPF o0702 should be equal to o0704
    And OSPF o0703 should be equal to o0704

    And OSPF YAML file should be equal to o0702
    And OSPF YAML file should be equal to o0703
    And OSPF YAML file should be equal to o0704
    
    # By Protocols
    And I Finish my OSPF tests and list tests not implemented