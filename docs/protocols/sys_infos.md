# Facts - Netests.io
###### <dylan.hamel@protonmail.com> - Nov. 2019


## Facts Definition

```python
class Facts:

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



## Facts comparaison function `__eq__`

```python
class Facts:
  
	def __eq__(self, other):
        if not isinstance(other, Facts):
            return NotImplemented

        return ((str(self.hostname) == str(other.hostname)) and
                (str(self.version) == str(other.version)))
```




## SysInfos Retrieve Data

|                 | hostname           | domain             | version            | build              | serial             | base_mac           | memory             | vendor             | model              | interfaces_lst     |
| --------------- | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ |
| NAPALM          | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :x:                | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Junos           | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cumulus         | :white_check_mark: | :x:                | :white_check_mark: | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Arista          | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco Nexus     | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco IOSXR     | :cry:              | :cry:              | :cry:              | :cry:              | :cry:              | :cry:              | :cry:              | :cry:              | :cry:              | :cry:              |
| Cisco IOS       | :white_check_mark: | :x:                | :white_check_mark: | :x:                | :white_check_mark: | :x:                | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Extreme VSP SSH | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Extreme VSP API | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :x:                | :x:                | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: |
|                 |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |
|                 |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |
|                 |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |

:white_check_mark: => Implemented​

:x: => Not supported

:cry: => Not Implemented



## Error and Miss

#### Arista

1. Error with "memory" :

```json
{
    "memTotal": 2014640,
    "uptime": 21040.32,
    "modelName": "vEOS",
    "internalVersion": "4.23.0.1F-13860745.42301F",
    "mfgName": "",
    "serialNumber": "",
    "systemMacAddress": "50:00:00:03:37:66",
    "bootupTimestamp": 1574501433.0,
    "memFree": 1326488,
    "version": "4.23.0.1F",
    "architecture": "i686",
    "isIntlVersion": false,
    "internalBuildId": "6a1d05a3-2754-4ecf-b553-fc15f98cfe62",
    "hardwareRevision": ""
}
```

memfree is used for "memory" ....

2. Error with vendor name

Vendor value is set manually `infos_converters.py`

```python
sys_info_obj.vendor = "Arista"
```

##### NAPALM_GET_SNMP

Napalm get_snmp is not available for Arista EOS

```python
    if task.host.platform != ARISTA_PLATEFORM_NAME:
        output = task.run(
            name=f"NAPALM get_snmp_information {task.host.platform}",
            task=napalm_get,
            getters=["get_snmp_information"]
        )
        # print(output.result)

        if output.result != "":
            outputs_dict[INFOS_SNMP_DICT_KEY] = (output.result)
```

=> Error output

```python
Traceback (most recent call last):
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/nornir/core/task.py", line 67, in start
    r = self.task(self, **self.params)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/nornir/plugins/tasks/networking/napalm_get.py", line 61, in napalm_get
    result[g] = method(**options)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/napalm/eos/eos.py", line 1202, in get_snmp_information
    snmp_config = self.device.run_commands(commands, encoding='json')
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pyeapi/client.py", line 730, in run_commands
    response = self._connection.execute(commands, encoding, **kwargs)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pyeapi/eapilib.py", line 499, in execute
    response = self.send(request)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pyeapi/eapilib.py", line 418, in send
    raise CommandError(code, msg, command_error=err, output=out)
pyeapi.eapilib.CommandError: Error [1002]: CLI command 2 of 4 'show snmp chassis' failed: invalid command [This command is deprecated by 'show snmp v2-mib chassis' (at token 2: 'chassis')]
```

##### NAPALM Version

Napalm retrieve the build version as version

```shell
leaf03#show version
 vEOS
Hardware version:
Serial number:
System MAC address:  5000.0003.3766

Software image version: 4.23.0.1F
Architecture:           i686
Internal build version: 4.23.0.1F-13860745.42301F
Internal build ID:      6a1d05a3-2754-4ecf-b553-fc15f98cfe62

Uptime:                 0 weeks, 2 days, 3 hours and 10 minutes
Total memory:           2014640 kB
Free memory:            1301172 kB
```

Napalm output

```json
{ 'facts': { 'fqdn': 'leaf03.dh.local',
             'hostname': 'leaf03',
             'interface_list': [ 'Ethernet1',
                                 'Ethernet2',
                                 'Ethernet3',
                                 'Ethernet4',
                                 'Ethernet5',
                                 'Ethernet6',
                                 'Ethernet7',
                                 'Loopback1',
                                 'Management1',
                                 'Vlan1000'],
             'model': 'vEOS',
             'os_version': '4.23.0.1F-13860745.42301F',
             'serial_number': '',
             'uptime': 184439,
             'vendor': 'Arista'}}
```

=> `version=4.23.0.1F-13860745.42301F`

With SSH from Netests.

```shell
<SystemInfos hostname=leaf03 domain=dh.local version=4.23.0.1F build=4.23.0.1F-13860745.42301F serial= base_mac=NOT_SET memory=1296080 vendor=Arista model=vEOS snmp_ips=[] interfaces_lst=['Management1', 'Ethernet2', 'Ethernet3', 'Ethernet1', 'Ethernet6', 'Ethernet7', 'Ethernet4', 'Ethernet5']>
```

=> `version=4.23.0.1F`

=> `build=4.23.0.1F-13860745.42301F`



#### Cisco IOS

2. Error with vendor name

Vendor value is set manually in `infos_converters.py`

```python
sys_info_obj.hostname = value[2] if value[2] != "" else NOT_SET
                sys_info_obj.version = value[0] if value[0] != "" else NOT_SET
                sys_info_obj.model = value[10] if value[10] != "" else NOT_SET
                sys_info_obj.serial = value[7][0] if value[7][0] != "" else NOT_SET
                sys_info_obj.vendor = "Cisco IOS"
```

