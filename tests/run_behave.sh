#!/bin/bash

echo "------------------------------------------"
echo ">>> Start Behave tests ..."
echo "------------------------------------------"

declare -i return_value=0
declare -a commands_lst=(
    'behave tests/features/ --no-capture'
)

for command in "${commands_lst[@]}"
do
    $command
    if [ $? -ne 0 ]; then
        return_value=1
    fi
done

exit $return_value