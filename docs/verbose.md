# Verbose mode utilization

Definition of verbose level.

## level1

Use for the result output.

```python
if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        PP.pprint(vrf_list)
```

```shell
<ListVRF
<VRF vrf_name=default vrf_id=1.1.1.1 vrf_type=forwarding l3_vni=NOT_SET rd=NOT_SET rt_imp=NOT_SET rt_exp=NOT_SET imp_targ=NOT_SET exp_targ=NOT_SET>
<VRF vrf_name=INTERNAL_PEERING_VRF vrf_id=0.0.0.0 vrf_type=non-forwarding l3_vni=NOT_SET rd=NOT_SET rt_imp=NOT_SET rt_exp=NOT_SET imp_targ=NOT_SET exp_targ=NOT_SET>
<VRF vrf_name=mgmt_junos vrf_id=0.0.0.0 vrf_type=forwarding l3_vni=NOT_SET rd=NOT_SET rt_imp=NOT_SET rt_exp=NOT_SET imp_targ=NOT_SET exp_targ=NOT_SET>
>
```

## level2

Use for the tasks results `print_result`.

```python
data = task.run(
    name=f"{JUNOS_GET_VRF_DETAIL}",
    task=netmiko_send_command,
    command_string=f"{JUNOS_GET_VRF_DETAIL}",
)

if verbose_mode(
    user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
    needed_value=LEVEL2
):
    printline()
    print_result(data)
```


```shell
vvvv show route instance detail | display json ** changed : False vvvvvvvvvvvvvv INFO

{
    "instance-information" : [
    {
        "attributes" : {"xmlns" : "http://xml.juniper.net/junos/18.1R2/junos-routing",
                        "junos:style" : "detail"
                       },
        "instance-core" : [
        {
            "instance-name" : [
            {
                "data" : "master"
            }
            ],
            "router-id" : [
            {
                "data" : "1.1.1.1"
            }
            ],
            "instance-type" : [
            {
                "data" : "forwarding"
            }
            ],
            "instance-state" : [
            {
                "data" : "Active"
            }
            ],
            "instance-rib" : [
            {
                "irib-name" : [
                {
                    "data" : "inet.0"
                }
                ],
                "irib-route-count" : [
                {
                    "data" : "6"
                }
                ],
                "irib-active-count" : [
                {
                    "data" : "6"
                }
                ],
                "irib-holddown-count" : [
                {
                    "data" : "0"
                }
                ],
                "irib-hidden-count" : [
                {
                    "data" : "0"
                }
                ]
            },
        ]
    }
    ]
}

^^^^ END show route instance detail | display json ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

```

## Level3

Use to print result of a command like TextFSM parsing :

```python
def _cumulus_vrf_ssh_converter(hostname: str(), cmd_output: list) -> ListVRF:
    list_vrf = ListVRF(list())

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL3
    ):  
        printline()
        print(cmd_output)
```

```shell
////////////////////////////////////////////////////////////////////////////////////////
[['mgmt', '1001']]
```

## Level4

For Debug example. In some case the strings are formatted to work with.

This is LEVEL4

```python
cmd_output = re.sub(
        pattern=r"communities:[\n\r]\s+RT",
        repl="communities:RT",
        string=cmd_output
    )

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL4
    ):
        printline()
        print(cmd_output)
```

```shell
Tue Apr  7 14:37:26.838 UTC

VRF EXTERNAL_PEERING; RD 65000:100; VPN ID not set
VRF mode: Regular
Description not set
Address family IPV4 Unicast
  Import VPN route-target communities:RT:65000:1
  Export VPN route-target communities:RT:65000:1
  No import route policy
  No export route policy
Address family IPV6 Unicast
  No import VPN route-target communities
  No export VPN route-target communities
  No import route policy
  No export route policy

VRF MGMT_VRF; RD not set; VPN ID not set
VRF mode: Regular
Description MANAGEMENT_VRF
Interfaces:
  MgmtEth0/0/CPU0/0
Address family IPV4 Unicast
  No import VPN route-target communities
  No export VPN route-target communities
  No import route policy
  No export route policy
Address family IPV6 Unicast
  No import VPN route-target communities
  No export VPN route-target communities
  No import route policy
  No export route policy
```

## Level5

*TO_DEFINED*