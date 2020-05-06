# Created by dylan.hamel at 09.12.19
Feature: Test protocols LLDP python class ./protocols/lldp.py
  # Description
  Scenario:
    # Description
    # Arista Networks ID Device = o00
    Given A network protocols named LLDP defined in protocols/lldp.py
    And I create a LLDP object equals to Arista manually named o0001
    And I create a LLDP object from a Arista API output named o0002
    And I create a LLDP object from a Arista Netconf named o0003
    And I create a LLDP object from a Arista SSH output named o0004

    # Cumulus Networks ID Device = o01
    And I create a LLDP object equals to Cumulus manually named o0101
    And I create a LLDP object from a Cumulus API output named o0102
    And I create a LLDP object from a Cumulus Netconf named o0103
    And I create a LLDP object from a Cumulus SSH output named o0104

    # Extreme Networks VSP (VOSS) ID Device = o02
    And I create a LLDP object equals to Extreme VSP manually named o0201
    And I create a LLDP object from a Extreme VSP API output named o0202
    And I create a LLDP object from a Extreme VSP Netconf output named o0203
    And I create a LLDP object from a Extreme VSP SSH output named o0204

    # Cisco IOS-XE ID Device = o03
    And I create a LLDP object equals to IOS manually named o0301
    And I create a LLDP object from a IOS API output named o0302
    And I create a LLDP object from a IOS Netconf named o0303
    And I create a LLDP object from a IOS SSH named o0304

    # Cisco IOS-XR Device = o04
    And I create a LLDP object equals to IOS-XR manually named o0401
    And I create a LLDP object from a IOS-XR API output named o0402
    And I create a LLDP object from a IOS-XR Netconf output named o403
    And I create a LLDP object from a IOS-XR SSH output named o0404
    And I create a LLDP object equals IOS-XR multi manually output named o0405
    And I create a LLDP object from a IOS-XR multi Netconf output named o0406

    # Juniper Networks ID Device = o05
    And I create a LLDP object equals to Juniper manually named o0501
    And I create a LLDP object from a Juniper API output named o0502
    And I create a LLDP object from a Juniper Netconf output named o0503
    And I create a LLDP object from a Juniper SSH output named o0504

    # NAPALM-Automation Networks ID Device = o06
    And I create a LLDP object equals to NAPALM manually named o0601
    And I create a LLDP object from a NAPALM output named o0602

    # Cisco Nexus NXOS ID Device = o07
    And I create a LLDP object equals to NXOS manually named o0701
    And I create a LLDP object from a NXOS API output named o0702
    And I create a LLDP object from a NXOS Netconf output named o0703
    And I create a LLDP object from a NXOS SSH output named o0704

    And I create a LLDP object equals to NXOS only one manually named o0711
    And I create a LLDP object from a NXOS only one API output named o0712
    And I create a LLDP object from a NXOS only one Netconf output named o0713
    And I create a LLDP object from a NXOS only one SSH output named o0714

    # COMPARAISON
    # Arista Networks
    And LLDP o0001 should be equal to o0002
    And LLDP o0001 should be equal to o0003
    And LLDP o0001 should be equal to o0004
    And LLDP o0002 should be equal to o0003
    And LLDP o0002 should be equal to o0004
    And LLDP o0003 should be equal to o0004

    And LLDP YAML file should be equal to o0002
    And LLDP YAML file should be equal to o0003
    And LLDP YAML file should be equal to o0004

    # Cumulus Networks
    And LLDP o0101 should be equal to o0102
    And LLDP o0101 should be equal to o0103
    And LLDP o0101 should be equal to o0104
    And LLDP o0102 should be equal to o0103
    And LLDP o0102 should be equal to o0104
    And LLDP o0103 should be equal to o0104

    And LLDP YAML file should be equal to o0102
    And LLDP YAML file should be equal to o0103
    And LLDP YAML file should be equal to o0104

    # Extreme Networks VSP
    And LLDP o0201 should be equal to o0202
    And LLDP o0201 should be equal to o0203
    And LLDP o0201 should be equal to o0204
    And LLDP o0202 should be equal to o0203
    And LLDP o0202 should be equal to o0204
    And LLDP o0203 should be equal to o0204

    And LLDP YAML file should be equal to o0202
    And LLDP YAML file should be equal to o0203
    And LLDP YAML file should be equal to o0204

    # Cisco IOS-XE
    And LLDP o0301 should be equal to o0302
    And LLDP o0301 should be equal to o0303
    And LLDP o0301 should be equal to o0304
    And LLDP o0302 should be equal to o0303
    And LLDP o0302 should be equal to o0304
    And LLDP o0303 should be equal to o0304

    And LLDP YAML file should be equal to o0302
    And LLDP YAML file should be equal to o0303
    And LLDP YAML file should be equal to o0304

    # Cisco IOS-XR
    And LLDP o0401 should be equal to o0402
    And LLDP o0401 should be equal to o0403
    And LLDP o0401 should be equal to o0404
    And LLDP o0402 should be equal to o0403
    And LLDP o0402 should be equal to o0404
    And LLDP o0403 should be equal to o0404

    And LLDP YAML file should be equal to o0402
    And LLDP YAML file should be equal to o0403
    And LLDP YAML file should be equal to o0404

    # Juniper Networks
    And LLDP o0501 should be equal to o0502
    And LLDP o0501 should be equal to o0503
    And LLDP o0501 should be equal to o0504
    And LLDP o0502 should be equal to o0503
    And LLDP o0502 should be equal to o0504
    And LLDP o0503 should be equal to o0504

    And LLDP YAML file should be equal to o0502
    And LLDP YAML file should be equal to o0503
    And LLDP YAML file should be equal to o0504

    # NAPALM-Automation
    And LLDP o0601 should be equal to o0602

    # Cisco Nexus NXOS
    And LLDP o0701 should be equal to o0702
    And LLDP o0701 should be equal to o0703
    And LLDP o0701 should be equal to o0704
    And LLDP o0702 should be equal to o0703
    And LLDP o0702 should be equal to o0704
    And LLDP o0703 should be equal to o0704

    And LLDP YAML file should be equal to o0702
    And LLDP YAML file should be equal to o0703
    And LLDP YAML file should be equal to o0704

    And LLDP o0711 should be equal to o0712
    And LLDP o0711 should be equal to o0713
    And LLDP o0711 should be equal to o0714
    And LLDP o0712 should be equal to o0713
    And LLDP o0712 should be equal to o0714
    And LLDP o0713 should be equal to o0714
    
    # By Protocols
    And I Finish my LLDP tests and list tests not implemented