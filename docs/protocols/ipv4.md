# IPv4 - Netests.io
###### <dylan.hamel@protonmail.com> - Nov. 2019


## IPv4 Definition





## IPv4 comparaison function `__eq__`



```python
class IP(ABC):

		def __eq__(self, other):
        if not isinstance(other, IP):
            return NotImplemented

        return (str(self.interface_name) == str(other.interface_name) and
                str(self.ip_address) == str(other.ip_address) and
                str(self.netmask) == str(other.netmask))
```




## VRF Retrieve Data

|             | interface_name     | ip_address         | netmask            |
| ----------- | ------------------ | ------------------ | ------------------ |
| NAPALM      | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Junos       | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cumulus     | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Arista      | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco Nexus | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco IOSXR | :cry:              | :cry:              | :cry:              |
| Cisco IOS   | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Extreme VSP | :white_check_mark: | :white_check_mark: | :white_check_mark: |
|             |                    |                    |                    |
|             |                    |                    |                    |
|             |                    |                    |                    |

:white_check_mark: => Implemented​

:cry: => Not Implemented

:x: => Not available



## Filtering

|             | Filtering available |
| ----------- | ------------------- |
| NAPALM      | :cry:               |
| Junos       | :cry:               |
| Cumulus     | ✅                   |
| Arista      | ✅                   |
| Cisco Nexus | ✅                   |
| Cisco IOSXR | :cry:               |
| Cisco IOS   | ✅                   |
| Extreme VSP | :cry:               |
|             |                     |
|             |                     |
|             |                     |

✅ => Implemented​

😢 => Not Implemented

❌ => Not available

```yaml
ipv4:
  test: true
  get_physical: true
  get_vlan: false
  get_loopback: false
  get_peerlink: false
  get_vni: false
```



## Error - must be improved

#### Juniper

Loopback interface netmask is set manually at 255.255.255.255.

```python
if "lo" in logic_interface.get("name")[0].get("data", NOT_SET) :
	ipv4_addresses_lst.ipv4_addresses_lst.append(
		IPV4(
            interface_name=_mapping_interface_name(
            	logic_interface.get("name")[0].get("data", NOT_SET)
            ),
			ip_address_with_mask=ip_addr,
			netmask="255.255.255.255"
		)
	)
else:
    ipv4_addresses_lst.ipv4_addresses_lst.append(
        IPV4(
            interface_name=_mapping_interface_name(
            	logic_interface.get("name")[0].get("data", NOT_SET)
            ),
            ip_address_with_mask=ip_addr,
        )
    )
```

