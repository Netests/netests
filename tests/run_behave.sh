#!/bin/bash

echo "------------------------------------------"
echo ">>> Start Behave tests ..."
echo "------------------------------------------"

declare -i return_value=0
declare -a commands_lst=(
    #'behave tests/features/cli_tests.feature --no-capture'
    'behave tests/features/bgp_tests.feature --no-capture'
    'behave tests/features/cdp_tests.feature --no-capture'
    'behave tests/features/facts_tests.feature --no-capture'
    'behave tests/features/lldp_tests.feature --no-capture'
    'behave tests/features/ping_tests.feature --no-capture'
    'behave tests/features/vrf_tests.feature --no-capture'
)

for command in "${commands_lst[@]}"
do
    $command
    if [ $? -ne 0 ]; then
        return_value=1
    fi
done

exit $return_value