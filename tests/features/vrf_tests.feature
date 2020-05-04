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

    And I create a VRF object equals to Arista no config manually named o0011
    And I create a VRF object from a Arista no config API output named o0012
    And I create a VRF object from a Arista no config Netconf named o0013
    And I create a VRF object from a Arista no config SSH output named o0014

    And I create a VRF object equals to Arista one vrf manually named o0021
    And I create a VRF object from a Arista one vrf API output named o0022
    And I create a VRF object from a Arista one vrf Netconf named o0023
    And I create a VRF object from a Arista one vrf SSH output named o0024
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

    And I create a VRF object equals to IOS no config manually named o0311
    And I create a VRF object from a IOS no config API named o0312
    And I create a VRF object from a IOS no config Netconf named o0313
    And I create a VRF object from a IOS no config SSH named o0314

    And I create a VRF object equals to IOS one vrf manually named o0321
    And I create a VRF object from a IOS one vrf API named o0322
    And I create a VRF object from a IOS one vrf Netconf named o0323
    And I create a VRF object from a IOS one vrf SSH named o0324

    And I create a VRF object equals to IOS many manually named o0331
    And I create a VRF object from a IOS many API named o0332
    And I create a VRF object from a IOS many Netconf named o0333
    And I create a VRF object from a IOS many SSH named o0334

    # Cisco IOS-XR Device = o04
    And I create a VRF object equals to IOS-XR manually named o0401
    And I create a VRF object from a IOS-XR API output named o0402
    And I create a VRF object from a IOS-XR Netconf output named o403
    And I create a VRF object from a IOS-XR SSH output named o0404
    And I create a VRF object equals IOS-XR multi manually output named o0405
    And I create a VRF object from a IOS-XR multi Netconf output named o0406

    And I create a VRF object equals to IOS-XR no config manually named o0411
    And I create a VRF object from a IOS-XR no config API named o0412
    And I create a VRF object from a IOS-XR no config Netconf named o0413
    And I create a VRF object from a IOS-XR no config SSH named o0414

    And I create a VRF object equals to IOS-XR one vrf manually named o0421
    And I create a VRF object from a IOS-XR one vrf API named o0422
    And I create a VRF object from a IOS-XR one vrf Netconf named o0423
    And I create a VRF object from a IOS-XR one vrf SSH named o0424

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

    And VRF o0011 should be equal to o0012
    And VRF o0011 should be equal to o0013
    And VRF o0011 should be equal to o0014
    And VRF o0012 should be equal to o0013
    And VRF o0012 should be equal to o0014
    And VRF o0013 should be equal to o0014

    And VRF o0021 should be equal to o0022
    And VRF o0021 should be equal to o0023
    And VRF o0021 should be equal to o0024
    And VRF o0022 should be equal to o0023
    And VRF o0022 should be equal to o0024
    And VRF o0023 should be equal to o0024

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

    And VRF o0311 should be equal to o0312
    And VRF o0311 should be equal to o0313
    And VRF o0311 should be equal to o0314
    And VRF o0312 should be equal to o0313
    And VRF o0312 should be equal to o0314
    And VRF o0313 should be equal to o0314

    And VRF o0321 should be equal to o0322
    And VRF o0321 should be equal to o0323
    And VRF o0321 should be equal to o0324
    And VRF o0322 should be equal to o0323
    And VRF o0322 should be equal to o0324
    And VRF o0323 should be equal to o0324

    And VRF o0331 should be equal to o0332
    And VRF o0331 should be equal to o0333
    And VRF o0331 should be equal to o0334
    And VRF o0332 should be equal to o0333
    And VRF o0332 should be equal to o0334
    And VRF o0333 should be equal to o0334

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

    And VRF o0411 should be equal to o0412
    And VRF o0411 should be equal to o0413
    And VRF o0411 should be equal to o0414
    And VRF o0412 should be equal to o0413
    And VRF o0412 should be equal to o0414
    And VRF o0413 should be equal to o0414

    And VRF o0421 should be equal to o0422
    And VRF o0421 should be equal to o0423
    And VRF o0421 should be equal to o0424
    And VRF o0422 should be equal to o0423
    And VRF o0422 should be equal to o0424
    And VRF o0423 should be equal to o0424

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
    And I Finish my VRF tests and list tests not implemented 