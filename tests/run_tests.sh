#!/bin/bash

declare -i return_value=0
declare -a commands_lst=(
    'sh tests/run_behave.sh'
    'sh tests/run_syntax.sh'
)

for command in "${commands_lst[@]}"
do
    $command
    if [ $? -ne 0 ]; then
        return_value=1
    fi
done

exit $return_value
