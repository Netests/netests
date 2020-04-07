#!/bin/bash

declare -i return_value=0
declare -a commands_lst=(
    'sh tests/run_behave.sh'
    'sh tests/run_syntax.sh'
    'sh tests/run_verbose.sh'
)

for command in "${commands_lst[@]}"
do
    $command
    if [ $? -ne 0 ]; then
        return_value=1
    fi
done

echo "------------------------------------------"
echo ">>> Tests finished result is ... [$return_value]"
echo "[0] = Success!"
echo "[X] = Failed!"
echo "------------------------------------------"

exit $return_value
