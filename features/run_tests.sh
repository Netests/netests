#!/bin/bash
behave features/mtu_tests.feature
behave features/static_tests.feature
behave features/infos_tests.feature
behave features/bgp_tests.feature
behave features/ospf_tests.feature
behave features/mlag_tests.feature
behave features/ipv4_tests.feature
behave features/vlan_tests.feature