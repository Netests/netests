# VLAN - Netests.io
###### <dylan.hamel@protonmail.com> - Nov. 2019



## VLAN

```python
class VLAN:

    vlan_id: str
    vrf_name: str
    ports_members: list

    # The following values are not used by the __eq__ function !!
    vlan_name: str
    vlan_descr: str
    mac_address: str
    ipv4_addresses: ListIPV4
    ipv6_addresses: ListIPV6
    fhrp_ip_address: str
```



## VLAN comparaison function `__eq__`

```python
    def __eq__(self, other):
        if not isinstance(other, VLAN):
            return NotImplemented

        # Basic
        return (str(self.vlan_id) == str(other.vlan_id) and
                (self.ports_members) == str(other.ports_members))
```

Other parameters are not included in the comparaison function and can be different.



## VLAN Retrieve Data

|             | vlan_id            | vrf_name           | vlan_name          | vlan_descr         | mac_address        | ipv4_addresses     | fhrp_ipv4_address  | ipv6_addresses     | fhrp_ipv6_address  |
| ----------- | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ |
| NAPALM      | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  |
| Junos       | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  |
| Cumulus     | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Arista      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :x:                |
| Cisco Nexus | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  |
| Cisco IOS   | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  |
| Extreme VSP | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  |
|             |                    |                    |                    |                    |                    |                    |                    |                    |                    |
|             |                    |                    |                    |                    |                    |                    |                    |                    |                    |
|             |                    |                    |                    |                    |                    |                    |                    |                    |                    |
|             |                    |                    |                    |                    |                    |                    |                    |                    |                    |

:white_check_mark: => Supported

:x: => Not Supported

:cry: => Not Implemented