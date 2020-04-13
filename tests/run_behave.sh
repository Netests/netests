#!/bin/bash

echo "------------------------------------------"
echo ">>> Start Behave tests ..."
echo "------------------------------------------"

declare -i return_value=0
declare -a commands_lst=(
    'behave tests/features/bgp_tests.feature'
    'behave tests/features/infos_tests.feature'
    'behave tests/features/ipv4_tests.feature'
    'behave tests/features/ipv6_tests.feature'
    'behave tests/features/lldp_tests.feature'
    'behave tests/features/mlag_tests.feature'
    'behave tests/features/mtu_tests.feature'
    'behave tests/features/ospf_tests.feature'
    'behave tests/features/static_tests.feature'
    'behave tests/features/verbose.feature'
    'behave tests/features/vlan_tests.feature'
    'behave tests/features/vrf_tests.feature --no-capture'
    'behave tests/features/cli_tests.feature'
    
)

for command in "${commands_lst[@]}"
do
    $command
    if [ $? -ne 0 ]; then
        return_value=1
    fi
done

exit $return_value