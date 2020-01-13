# VRF - Netests.io
###### <dylan.hamel@protonmail.com> - Nov. 2019


## LLDP Definition

```python
class LLDP(DiscoveryProtocols):
	# [...]
  
class DiscoveryProtocols(ABC):
    local_name: str
    local_port: str
    neighbor_name: str
    neighbor_port: str

    # Following parameter is not use in compare function
    neighbor_os:str
    neighbor_mgmt_ip: str
    neighbor_type: list

```



## LLDP comparaison function `__eq__`

```python
    def __eq__(self, other):
        if not isinstance(other, LLDP):
            return NotImplemented

        return (self.local_name == other.local_name and
                self.local_port == other.local_port and
                self.neighbor_name == other.neighbor_name and
                self.neighbor_port == other.neighbor_port) or (
                self.local_name == other.neighbor_name and
                self.local_port == other.neighbor_port and
                self.neighbor_name == other.local_name and
                self.neighbor_port == other.local_port)
```



### LLDP Retrieve Data

|             | local_name         | local_port         | neighbor_name      | neighbor_port      | neighbor_os        | neighbor_mgmt_ip   | neighbor_type      |
| ----------- | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ |
| NAPALM      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: |
| Junos       | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :x:                |
| Cumulus     | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Arista      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco Nexus | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco IOSXR | :cry:              | :cry:              | :cry:              | :cry:              | :cry:              | :cry:              | :cry:              |
| Cisco IOS   | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Extreme VSP | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
|             |                    |                    |                    |                    |                    |                    |                    |
|             |                    |                    |                    |                    |                    |                    |                    |
|             |                    |                    |                    |                    |                    |                    |                    |

:white_check_mark: => Supported

:x: => Not Supported

:cry: => Not Implemented​