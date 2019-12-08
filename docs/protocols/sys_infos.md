# SysInfos - Netests.io
###### <dylan.hamel@protonmail.com> - Nov. 2019


## SysInfos Definition

```python
class SystemInfos:

    hostname: str
    version: str

    # The following values are not used by the __eq__ function !!
    build: str
    serial: str
    domain: str
    base_mac: str
    memory: str
    vendor: str
    model: str
    snmp: list
    interfaces_lst: list
```



## SysInfos comparaison function `__eq__`

```python
class SystemInfos:
  
	def __eq__(self, other):
        if not isinstance(other, SystemInfos):
            return NotImplemented

        return ((str(self.hostname) == str(other.hostname)) and
                (str(self.version) == str(other.version)))
```




## SysInfos Retrieve Data

|             | hostname           | domain             | version            | build              | serial             | base_mac           | memory             | vendor             | model              | snmp_ips           | interfaces_lst     |
| ----------- | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ |
| NAPALM      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :x:                | :x:                | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: |
| Junos       | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :x:                | :white_check_mark: | SET_MAN            | :white_check_mark: | :x:                | :white_check_mark: |
| Cumulus     | :white_check_mark: | :x:                | :white_check_mark: | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Arista      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | SET_MAN            | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco Nexus | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco IOSXR | :cry:              | :cry:              | :cry:              | :cry:              | :cry:              | :cry:              | :cry:              | :cry:              | :cry:              | :cry:              | :cry:              |
| Cisco IOS   | :white_check_mark: | :x:                | :white_check_mark: | :x:                | :white_check_mark: | :x:                | :x:                | SET_MAN            | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Extreme VSP | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
|             |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |
|             |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |
|             |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |

:white_check_mark: => Implemented​

:x: => Not supported

:cry: => Not Implemented
