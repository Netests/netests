#!/bin/bash

declare -i return_value=0
declare -a commands_lst=(
    'sh features/run_behave.sh'
    'sh features/run_syntax.sh'
)

for command in "${commands_lst[@]}"
do
    $command
    if [ $? -ne 0 ]; then
        return_value=1
    fi
done

exit $return_value
