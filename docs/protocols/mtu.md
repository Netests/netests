# MTU - Netests.io
###### <dylan.hamel@protonmail.com> - Nov. 2019


## MTU Definition





## MTU comparaison function `__eq__`

```python
class InterfaceMTU:
  
def __eq__(self, other):
        if not isinstance(other, InterfaceMTU):
            return NotImplemented

        return ((str(self.interface_name) == str(other.interface_name)) and
                (str(self.mtu_size) == str(other.mtu_size)))
```



```python
class MTU:

    def __eq__(self, other):
        if not isinstance(other, MTU):
            return NotImplemented

        if self.mtu_global == NOT_SET:
            return (str(self.hostname) == str(other.hostname) and \
					(self.interface_mtu_lst) == str(other.interface_mtu_lst))
        else:
            return (str(self.hostname) == str(other.hostname) and \
					str(self.mtu_global) == str(other.mtu_global) and \
					(self.interface_mtu_lst) == str(other.interface_mtu_lst))
```




## MTU Retrieve Data

|             | interface_name     | mtu_size           |
| ----------- | ------------------ | ------------------ |
| NAPALM      | :cry:              | :cry:              |
| Junos       | :cry:              | :cry:              |
| Cumulus     | :cry:              | :cry:              |
| Arista      | :cry:              | :cry:              |
| Cisco Nexus | :cry:              | :cry:              |
| Cisco IOSXR | :cry:              | :cry:              |
| Cisco IOS   | :white_check_mark: | :white_check_mark: |
| Extreme VSP | :cry:              | :cry:              |
|             |                    |                    |
|             |                    |                    |
|             |                    |                    |

:white_check_mark: => Implemented​

:cry: => Not Implemented



## MTU compare function

MTU compare function is the only one that doesn't compare MTU object. The reason is the `global_size` value.

```python
    hostname: str
    mtu_global: str
    interface_mtu_lst: ListInterfaceMTU
```

This value is used to avoid having to set the MTU value for all interfaces.

You can define only the "exception" in `interfaces:`.

#### Example

```yaml
leaf05:
  global_mtu: 1500
  interfaces:
    lo0: 1514
```

Only the loopback interface has a MTU size of 1514. All others interfaces have a MTU size of 1500.



## Error, Miss and Exceptions

#### Cumulus

Loopback interface is not retrieve. In Cumulus Linux MTU size of an interface loopback is 65536.

```python
	for interface in cmd_output:
		if "swp" in interface or "eth" in interface:
			interface_mtu_lst.interface_mtu_lst.append(
				InterfaceMTU(
					interface_name=_mapping_interface_name(
						interface
					),
					mtu_size=cmd_output.get(interface).get('iface_obj').get('mtu', NOT_SET),
				)
			)
```

```python
<InterfaceMTU interface_name=swp5 mtu_size=1500>
<InterfaceMTU interface_name=lo mtu_size=65536>
<InterfaceMTU interface_name=swp2 mtu_size=1500>
<InterfaceMTU interface_name=swp3 mtu_size=1500>
<InterfaceMTU interface_name=swp1 mtu_size=1500>
<InterfaceMTU interface_name=swp6 mtu_size=1500>
<InterfaceMTU interface_name=swp7 mtu_size=1500>
<InterfaceMTU interface_name=swp4 mtu_size=1500>
<InterfaceMTU interface_name=eth0 mtu_size=1500>>
```

