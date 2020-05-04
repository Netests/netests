# VRF - Netests.io
###### <dylan.hamel@protonmail.com> - Nov. 2019


## VRF Definition

```python
class VRF:

    vrf_name: str
    vrf_id: str
    vrf_type: str
    l3_vni: str
    rd: str
    rt_imp: str
    rt_exp: str
    imp_targ: str
    exp_targ: str
```


## VRF comparaison function `__eq__`

```python
    def __eq__(self, other):
        if not isinstance(other, VRF):
            return NotImplemented

        return ((str(self.vrf_name) == str(other.vrf_name)))
```

Other parameters are not included in the comparaison function and can be different.




### VRF Retrieve Data

|                 | vrf_name           | vrf_id             | vrf_type           | l3_vni             | rd                 | rt_imp             | rt_exp             | imp_targ           | exp_targ           |
| --------------- | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ |
| NAPALM          | :white_check_mark: | :x:                | :white_check_mark: | :x:                | :white_check_mark: | :x:                | :x:                | :x:                | :x:                |
| Junos SSH       | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Junos Netconf   | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Junos API       | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cumulus SSH     | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                |
| Cumulus API     | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                |
| Arista SSH      | :white_check_mark: | :x:                | :x:                | :x:                | :white_check_mark: | :x:                | :x:                | :x:                | :x:                |
| Arista Netconf  |                    |                    |                    |                    |                    |                    |                    |                    |                    |
| Arista API      |                    |                    |                    |                    |                    |                    |                    |                    |                    |
| Nexus SSH       | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :white_check_mark: | :x:                | :x:                | :x:                | :x:                |
| Nexus Netconf   | :white_check_mark: | :x:                | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                |
| Nexus API       | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                |
| IOSXR Netconf   | :white_check_mark: | :x:                | :x:                | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                |
| IOSXR SSH       | :white_check_mark: | :x:                | :white_check_mark: | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                |
| IOS SSH         | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                |
| IOS NetConf     | :white_check_mark: | :x:                | :x:                | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                |
| IOS API         | :white_check_mark: | :x:                | :x:                | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                |
| Extreme VSP SSH | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                |
| Extreme VSP API |                    |                    |                    |                    |                    |                    |                    |                    |                    |
|                 |                    |                    |                    |                    |                    |                    |                    |                    |                    |
|                 |                    |                    |                    |                    |                    |                    |                    |                    |                    |
|                 |                    |                    |                    |                    |                    |                    |                    |                    |                    |

:white_check_mark: => Supported

:x: => Not supported

:warning: => Not supported by the vendor

[EMPTY] => Not Implemented



## Error and Miss

#### Cisco Nexus

port 22 is fix

```python
    elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM:
        # Nexus get_network_instances is not Implemented by NAPALM (November 2019)
        # File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/napalm/base/base.py", line 1535, in get_network_instances
        # raise NotImplementedError
        #   NotImplementedError
```

