# VRF - Netests.io
###### <dylan.hamel@protonmail.com> - Nov. 2019


## VRF Definition





## VRF comparaison function `__eq__`

```python
    def __eq__(self, other):
        if not isinstance(other, VRF):
            return NotImplemented

        return ((str(self.vrf_name) == str(other.vrf_name)))
```

Other parameters are not included in the comparaison function and can be different.




### VRF Retrieve Data

|             | vrf_name           | vrf_id             | vrf_type           | l3_vni | rd                 | rt_imp             | rt_exp             | imp_targ           | exp_targ           |
| ----------- | ------------------ | ------------------ | ------------------ | ------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ |
| NAPALM      | :white_check_mark: | :x:                | :white_check_mark: | :x:    | :white_check_mark: | :x:                | :x:                | :x:                | :x:                |
| Junos       | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:    | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cumulus     | :white_check_mark: | :white_check_mark: | :x:                | :x:    | :x:                | :x:                | :x:                | :x:                | :x:                |
| Arista      | :white_check_mark: | :x:                | :x:                | :x:    | :white_check_mark: | :x:                | :x:                | :x:                | :x:                |
| Cisco Nexus | :white_check_mark: | :white_check_mark: | :x:                | :x:    | :x:                | :x:                | :x:                | :x:                | :x:                |
| Cisco IOSXR | :white_check_mark: | :white_check_mark: | :x:                | :x:    | :white_check_mark: | :x:                | :x:                | :x:                | :x:                |
| Cisco IOS   | :white_check_mark: | :white_check_mark: | :x:                | :x:    | :white_check_mark: | :x:                | :x:                | :x:                | :x:                |
|             |                    |                    |                    |        |                    |                    |                    |                    |                    |
|             |                    |                    |                    |        |                    |                    |                    |                    |                    |
|             |                    |                    |                    |        |                    |                    |                    |                    |                    |
|             |                    |                    |                    |        |                    |                    |                    |                    |                    |


