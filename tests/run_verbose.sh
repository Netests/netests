#!/bin/bash

echo "------------------------------------------"
echo ">>> Start NETESTS_VERBOSE tests ..."
echo "------------------------------------------"

declare -i return_value=0

if [ $(grep -ri '\["NETESTS_VERBOSE"' . --exclude=netests.py --exclude=./nornir/nornir.log  --exclude=./tests/run_verbose.sh | wc -l) -ne "0" ]
then
    echo 'There are some code as : os.environ["NETESTS_VERBOSE"]'
    echo 'Please replace by : os.environ.get("NETESTS_VERBOSE", NOT_SET),'
    return_value=1
else
    echo 'NETESTS_VERBOSE tests => Success'
fi

exit $return_value