#!/bin/bash

echo "------------------------------------------"
echo ">>> Start Syntax tests ..."
echo "------------------------------------------"

declare -i return_value=0
declare -a commands_lst=(
    'pylama netests.py'
    'pylama exceptions/'
    'pylama functions/bgp/*'
    'pylama functions/vrf/arista'
    'pylama functions/vrf/cumulus'
    'pylama functions/vrf/extreme_vsp'
    'pylama functions/vrf/ios'
    'pylama functions/vrf/iosxr'
    'pylama functions/vrf/nxos'
    'pylama functions/vrf/juniper'
    'pylama functions/vrf/napalm'
    'pylama functions/vrf/vrf_get.py'
    'pylama functions/base_selection.py'
    'pylama functions/verbose_mode.py'
    'pylama const/constants.py'
    'pylama protocols/vrf.py'
)

for command in "${commands_lst[@]}"
do
    echo "$command"
    $command
    if [ $? -ne 0 ]; then
        echo -e "\e[101 WARNING - Command has failed !!! Fix before commit and push !! \e[49m"
        echo -e "****************************************************************************"
        return_value=1
    fi
done

exit $return_value