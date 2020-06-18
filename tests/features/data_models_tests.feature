Feature: Test --show-data-model xxx argument
    Scenario:
        Given I try to execute netests --show-data-model bgp
        Then I print BGP data model
        And I can convert bgp.yml to dict with yaml

    Scenario:
        Given I try to execute netests --show-data-model cdp
        Then I print CDP data model
        And I can convert cdp.yml to dict with yaml

    Scenario:
        Given I try to execute netests --show-data-model facts
        Then I print Facts data model
        And I can convert facts.yml to dict with yaml

    Scenario:
        Given I try to execute netests --show-data-model lldp
        Then I print LLDP data model
        And I can convert lldp.yml to dict with yaml

    Scenario:
        Given I try to execute netests --show-data-model ospf
        Then I print OSPF data model
        And I can convert ospf.yml to dict with yaml

    Scenario:
        Given I try to execute netests --show-data-model ping
        Then I print PING data model
        And I can convert ping.yml to dict with yaml
    
    Scenario:
        Given I try to execute netests --show-data-model vlan
        Then I print VLAN data model
        And I can convert vlan.yml to dict with yaml

    Scenario:
        Given I try to execute netests --show-data-model vrf
        Then I print VRF data model
        And I can convert vrf.yml to dict with yaml

    Scenario:
        Given I try to execute netests --show-data-model hello
        Then I check that the status code is not zero

    Scenario:
        Given I get all protocols listed in netests/converters
        And I check that a data_model exist for each protocol