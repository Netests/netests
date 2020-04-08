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

*TO_DEFINED*

## Level4

*TO_DEFINED*

## Level5

*TO_DEFINED*