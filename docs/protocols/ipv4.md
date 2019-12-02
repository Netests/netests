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




### VRF Retrieve Data

|             | interface_name     | ip_address         | netmask            |
| ----------- | ------------------ | ------------------ | ------------------ |
| NAPALM      | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Junos       | 😢                  | 😢                  | 😢                  |
| Cumulus     | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Arista      | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco Nexus | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco IOSXR | :cry:              | :cry:              | :cry:              |
| Cisco IOS   | :white_check_mark: | :white_check_mark: | :white_check_mark: |
|             |                    |                    |                    |
|             |                    |                    |                    |
|             |                    |                    |                    |
|             |                    |                    |                    |

:white_check_mark: => Implemented​

:cry: => Not Implemented