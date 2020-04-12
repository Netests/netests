# Created by dylan.hamel at 09.12.19
Feature: Test protocols VRF python class ./protocols/vrf.py
  # Description
  Scenario:
    # Description
    # Arista Networks ID Device = o00
    Given A network protocols named VRF defined in protocols/vrf.py
    And I create a VRF object equals to Arista manually named o0001
    And I create a VRF object from a Arista API output named o0002
    And I create a VRF object from a Arista Netconf named o0003
    And I create a VRF object from a Arista SSH output named o0004
    # Cumulus Networks ID Device = o01
    And I create a VRF object equals to Cumulus manually named o0101
    And I create a VRF object from a Cumulus API output named o0102
    And I create a VRF object from a Cumulus Netconf named o0103
    And I create a VRF object from a Cumulus SSH output named o0104
    # Extreme Networks VSP (VOSS) ID Device = o02
    And I create a VRF object equals to Extreme VSP manually named o0201
    And I create a VRF object from a Extreme VSP API output named o0204
    And I create a VRF object from a Extreme VSP Netconf output named o0204
    And I create a VRF object from a Extreme VSP SSH output named o0204
    # Cisco IOS-XE ID Device = o03
    And I create a VRF object equals to IOS manually named o0301
    And I create a VRF object from a IOS API output named o0302
    And I create a VRF object from a IOS Netconf named o0303
    And I create a VRF object from a IOS SSH named o0304
    # Cisco IOS-XR Device = o04
    And I create a VRF object equals to IOS-XR manually named o0401
    And I create a VRF object from a IOS-XR API output named o0402
    And I create a VRF object from a IOS-XR Netconf output named o403
    And I create a VRF object from a IOS-XR SSH output named o0404
    And I create a VRF object equals IOS-XR multi manually output named o0405
    And I create a VRF object from a IOS-XR multi Netconf output named o0406
    # Juniper Networks ID Device = o05
    And I create a VRF object equals to Juniper manually named o0501
    And I create a VRF object from a Juniper API output named o0502
    And I create a VRF object from a Juniper Netconf output named o0503
    And I create a VRF object from a Juniper SSH output named o0504
    # NAPALM-Automation Networks ID Device = o06
    And I create a VRF object equals to NAPALM manually named o0601
    And I create a VRF object from a NAPALM output named o0602
    # Cisco Nexus NXOS ID Device = o07
    And I create a VRF object equals to NXOS manually named o0701
    And I create a VRF object from a NXOS API output named o0702
    And I create a VRF object from a NXOS Netconf output named o0703
    And I create a VRF object from a NXOS SSH output named o0704

    # COMPARAISON
    # Arista Networks
    And VRF o0001 should be equal to o0002
    And VRF o0001 should be equal to o0003
    And VRF o0001 should be equal to o0004
    And VRF o0002 should be equal to o0003
    And VRF o0002 should be equal to o0004
    And VRF o0003 should be equal to o0004

    And VRF YAML file should be equal to o0002
    And VRF YAML file should be equal to o0003
    And VRF YAML file should be equal to o0004
    # Cumulus Networks
    And VRF o0101 should be equal to o0102
    And VRF o0101 should be equal to o0103
    And VRF o0101 should be equal to o0104
    And VRF o0102 should be equal to o0103
    And VRF o0102 should be equal to o0104
    And VRF o0103 should be equal to o0104

    And VRF YAML file should be equal to o0102
    And VRF YAML file should be equal to o0103
    And VRF YAML file should be equal to o0104
    # Extreme Networks VSP
    And VRF o0201 should be equal to o0202
    And VRF o0201 should be equal to o0203
    And VRF o0201 should be equal to o0204
    And VRF o0202 should be equal to o0203
    And VRF o0202 should be equal to o0204
    And VRF o0203 should be equal to o0204

    And VRF YAML file should be equal to o0202
    And VRF YAML file should be equal to o0203
    And VRF YAML file should be equal to o0204
    # Cisco IOS-XE
    And VRF o0301 should be equal to o0302
    And VRF o0301 should be equal to o0303
    And VRF o0301 should be equal to o0304
    And VRF o0302 should be equal to o0303
    And VRF o0302 should be equal to o0304
    And VRF o0303 should be equal to o0304

    And VRF YAML file should be equal to o0302
    And VRF YAML file should be equal to o0303
    And VRF YAML file should be equal to o0304
    # Cisco IOS-XR
    And VRF o0401 should be equal to o0402
    And VRF o0401 should be equal to o0403
    And VRF o0401 should be equal to o0404
    And VRF o0402 should be equal to o0403
    And VRF o0402 should be equal to o0404
    And VRF o0403 should be equal to o0404
      # Multiple VRF
    And VRF o0405 should be equal to o0406

    And VRF YAML file should be equal to o0402
    And VRF YAML file should be equal to o0403
    And VRF YAML file should be equal to o0404
    # Juniper Networks
    And VRF o0501 should be equal to o0502
    And VRF o0501 should be equal to o0503
    And VRF o0501 should be equal to o0504
    And VRF o0502 should be equal to o0503
    And VRF o0502 should be equal to o0504
    And VRF o0503 should be equal to o0504

    And VRF YAML file should be equal to o0502
    And VRF YAML file should be equal to o0503
    And VRF YAML file should be equal to o0504
    # NAPALM-Automation
    And VRF o0601 should be equal to o0602

    And VRF YAML file should be equal to o0601
    And VRF YAML file should be equal to o0602
    # Cisco Nexus NXOS
    And VRF o0701 should be equal to o0702
    And VRF o0701 should be equal to o0703
    And VRF o0701 should be equal to o0704
    And VRF o0702 should be equal to o0703
    And VRF o0702 should be equal to o0704
    And VRF o0703 should be equal to o0704

    And VRF YAML file should be equal to o0702
    And VRF YAML file should be equal to o0703
    And VRF YAML file should be equal to o0704
    # By Protocols
    And I Finish my test and list tests not implemented 