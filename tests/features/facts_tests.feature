# Created by dylan.hamel at 09.12.19
Feature: Test protocols Facts python class ./protocols/facts.py
    # Description
    Scenario:
        # Description
        # Arista Networks ID Device = o00
        Given A network protocols named Facts defined in protocols/facts.py
        And I create a Facts object equals to Arista manually named o0001
        And I create a Facts object from a Arista API output named o0002
        And I create a Facts object from a Arista Netconf named o0003
        And I create a Facts object from a Arista SSH output named o0004
        # Cumulus Networks ID Device = o01
        And I create a Facts object equals to Cumulus manually named o0101
        And I create a Facts object from a Cumulus API output named o0102
        And I create a Facts object from a Cumulus Netconf named o0103
        And I create a Facts object from a Cumulus SSH output named o0104
        # Extreme Networks VSP (VOSS) ID Device = o02
        And I create a Facts object equals to Extreme VSP manually named o0201
        And I create a Facts object from a Extreme VSP API output named o0202
        And I create a Facts object from a Extreme VSP Netconf output named o0203
        And I create a Facts object from a Extreme VSP SSH output named o0204
        # Cisco IOS-XE ID Device = o03
        And I create a Facts object equals to IOS manually named o0301
        And I create a Facts object from a IOS API output named o0302
        And I create a Facts object from a IOS Netconf named o0303
        And I create a Facts object from a IOS SSH named o0304

        # Cisco IOS-XR Device = o04
        And I create a Facts object equals to IOS-XR manually named o0401
        And I create a Facts object from a IOS-XR API output named o0402
        And I create a Facts object from a IOS-XR Netconf output named o403
        And I create a Facts object from a IOS-XR SSH output named o0404
        And I create a Facts object equals IOS-XR multi manually output named o0405
        And I create a Facts object from a IOS-XR multi Netconf output named o0406
        # Juniper Networks ID Device = o05
        And I create a Facts object equals to Juniper manually named o0501
        And I create a Facts object from a Juniper API output named o0502
        And I create a Facts object from a Juniper Netconf output named o0503
        And I create a Facts object from a Juniper SSH output named o0504
        # NAPALM-Automation Networks ID Device = o06
        And I create a Facts object equals to NAPALM manually named o0601
        And I create a Facts object from a NAPALM output named o0602
        # Cisco Nexus NXOS ID Device = o07
        And I create a Facts object equals to NXOS manually named o0701
        And I create a Facts object from a NXOS API output named o0702
        And I create a Facts object from a NXOS Netconf output named o0703
        And I create a Facts object from a NXOS SSH output named o0704

        # COMPARAISON
        # Arista Networks
        And Facts o0001 should be equal to o0002
        And Facts o0001 should be equal to o0003
        And Facts o0001 should be equal to o0004
        And Facts o0002 should be equal to o0003
        And Facts o0002 should be equal to o0004
        And Facts o0003 should be equal to o0004

        And Facts YAML file should be equal to o0002
        And Facts YAML file should be equal to o0003
        And Facts YAML file should be equal to o0004
        # Cumulus Networks
        And Facts o0101 should be equal to o0102
        And Facts o0101 should be equal to o0103
        And Facts o0101 should be equal to o0104
        And Facts o0102 should be equal to o0103
        And Facts o0102 should be equal to o0104
        And Facts o0103 should be equal to o0104

        And Facts YAML file should be equal to o0102
        And Facts YAML file should be equal to o0103
        And Facts YAML file should be equal to o0104
        # Extreme Networks VSP
        And Facts o0201 should be equal to o0202
        And Facts o0201 should be equal to o0203
        And Facts o0201 should be equal to o0204
        And Facts o0202 should be equal to o0203
        And Facts o0202 should be equal to o0204
        And Facts o0203 should be equal to o0204

        And Facts YAML file should be equal to o0202
        And Facts YAML file should be equal to o0203
        And Facts YAML file should be equal to o0204
        # Cisco IOS-XE
        And Facts o0301 should be equal to o0302
        And Facts o0301 should be equal to o0303
        And Facts o0301 should be equal to o0304
        And Facts o0302 should be equal to o0303
        And Facts o0302 should be equal to o0304
        And Facts o0303 should be equal to o0304

        And Facts o0311 should be equal to o0312
        And Facts o0311 should be equal to o0313
        And Facts o0311 should be equal to o0314
        And Facts o0312 should be equal to o0313
        And Facts o0312 should be equal to o0314
        And Facts o0313 should be equal to o0314

        And Facts o0321 should be equal to o0322
        And Facts o0321 should be equal to o0323
        And Facts o0321 should be equal to o0324
        And Facts o0322 should be equal to o0323
        And Facts o0322 should be equal to o0324
        And Facts o0323 should be equal to o0324

        And Facts o0331 should be equal to o0332
        And Facts o0331 should be equal to o0333
        And Facts o0331 should be equal to o0334
        And Facts o0332 should be equal to o0333
        And Facts o0332 should be equal to o0334
        And Facts o0333 should be equal to o0334

        And Facts YAML file should be equal to o0302
        And Facts YAML file should be equal to o0303
        And Facts YAML file should be equal to o0304
        # Cisco IOS-XR
        And Facts o0401 should be equal to o0402
        And Facts o0401 should be equal to o0403
        And Facts o0401 should be equal to o0404
        And Facts o0402 should be equal to o0403
        And Facts o0402 should be equal to o0404
        And Facts o0403 should be equal to o0404
        # Multiple Facts
        And Facts o0405 should be equal to o0406

        And Facts YAML file should be equal to o0402
        And Facts YAML file should be equal to o0403
        And Facts YAML file should be equal to o0404
        # Juniper Networks
        And Facts o0501 should be equal to o0502
        And Facts o0501 should be equal to o0503
        And Facts o0501 should be equal to o0504
        And Facts o0502 should be equal to o0503
        And Facts o0502 should be equal to o0504
        And Facts o0503 should be equal to o0504

        And Facts YAML file should be equal to o0502
        And Facts YAML file should be equal to o0503
        And Facts YAML file should be equal to o0504
        # NAPALM-Automation
        And Facts o0601 should be equal to o0602

        # Cisco Nexus NXOS
        And Facts o0701 should be equal to o0702
        And Facts o0701 should be equal to o0703
        And Facts o0701 should be equal to o0704
        And Facts o0702 should be equal to o0703
        And Facts o0702 should be equal to o0704
        And Facts o0703 should be equal to o0704

        And Facts YAML file should be equal to o0702
        And Facts YAML file should be equal to o0703
        And Facts YAML file should be equal to o0704
        # By Protocols
        And I Finish my Facts tests and list tests not implemented