# netests

Create your environnement :

```shell
» python3 -m venv .
» source ./bin/activate

(netests) ------------------------------------------------------------
(master*) »

» pip install --upgrade pip
» pip --version
pip 19.2.3
```



## Capabilities (Only via SSH)

|           |      Juniper       |      Cumulus       | Arista             |        NXOS        |        IOS         | IOS-XR |    Extreme VSP     | NAPALM             |
| --------- | :----------------: | :----------------: | ------------------ | :----------------: | :----------------: | :----: | :----------------: | ------------------ |
| BGP       |        :x:         | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         |  :x:   |        :x:         | :x:                |
| OSPF      |        :x:         | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         |  :x:   |        :x:         | :x:                |
| SysInfos  | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |  :x:   | :white_check_mark: | :white_check_mark: |
| Ping      |        :x:         | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         |  :x:   |        :x:         | :x:                |
| Socket    |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |  :x:   |        :x:         | :x:                |
| Static    |        :x:         | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         |  :x:   |        :x:         | :x:                |
| VRF       |        :x:         | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         |  :x:   |        :x:         | :x:                |
| LLDP      |        :x:         | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         |  :x:   |        :x:         | :white_check_mark: |
| CDP       |        :x:         | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         |  :x:   |        :x:         | :white_check_mark: |
| IPv4      |        :x:         | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         |  :x:   |        :x:         | :x:                |
| IPv6      |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |  :x:   |        :x:         | :x:                |
| MTU       |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |  :x:   |        :x:         | :x:                |
| VTEP      |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |  :x:   |        :x:         | :x:                |
| Multicast |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |  :x:   |        :x:         | :x:                |
| VLAN      |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |  :x:   |        :x:         | :x:                |
| VXLAN     |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |  :x:   |        :x:         | :x:                |
| EVPN      |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |  :x:   |        :x:         | :x:                |
| IS-IS     |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |  :x:   |        :x:         | :x:                |

:white_check_mark: = Implemented

:x: = Not implemented​

:sleepy: = Impossible to implement



## Devices supported by NAPALM

|      Juniper       | Cumulus |       Arista       |     Cisco NXOS     |    Cisco IOS-XR    |     Cisco IOS      | Extreme |
| :----------------: | :-----: | :----------------: | :----------------: | :----------------: | :----------------: | :-----: |
| :white_check_mark: |   :x:   | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |   :x:   |
|       junos        |   ---   |        eos         |        nxos        |       iosxr        |        ios         |   ---   |

For the moment Cumulus Linux is only compatible with SSH. Utilization with REST API is int development.



## Road Map

Implement all protocols for VyOS and Extreme Network EXOS

Using Netconf / RestConf with Yang to retrieve network devices datas

Use Cumulus Linux REST API to retrieve Data



## Error / Miss

This chapter contains informations about what is missing in protocols implementation and need to be implemented or improved.

### SystemInfos

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

