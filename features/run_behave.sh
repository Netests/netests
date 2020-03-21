#!/bin/bash

echo "------------------------------------------"
echo ">>> Start Behave tests ..."
echo "------------------------------------------"

declare -i return_value=0
declare -a commands_lst=(
    'behave features/mtu_tests.feature'
    'behave features/static_tests.feature'
    'behave features/infos_tests.feature'
    'behave features/bgp_tests.feature'
    'behave features/ospf_tests.feature'
    'behave features/mlag_tests.feature'
    'behave features/ipv4_tests.feature'
    'behave features/ipv6_tests.feature'
    'behave features/vlan_tests.feature'
    'behave features/lldp_tests.feature'
)

for command in "${commands_lst[@]}"
do
    $command
    if [ $? -ne 0 ]; then
        return_value=1
    fi
done

exit $return_value