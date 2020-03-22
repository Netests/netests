#!/bin/bash

echo "------------------------------------------"
echo ">>> Start Syntax tests ..."
echo "------------------------------------------"

declare -i return_value=0
declare -a commands_lst=(
    'pylama netests.py'
    'pylama exceptions/'
    'pylama functions/bgp/*'
    'pylama functions/base_selection.py'
    'pylama functions/verbose_mode.py'
    'pylama const/constants.py'
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