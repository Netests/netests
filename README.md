# Netests.io

###### <dylan.hamel@protonmail.com> - November 2019 - Copyright

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



## Discuss

https://join.slack.com/t/dteamgroupe/shared_invite/enQtODQyNDY3NjQyMjkxLTJhMGE5YzM2MTY0MGJiM2M4OTBjOTc1MGMxZDU1MTk4Y2ZmYTQ4ZTc0OWI0NjliNzc1NmQ4ZDNmMzNhNjM3YWM



## How to use ??

The idea of this project is to offer a test platform for the network to allow engineers to perform tests without having to write python code (or other languages :smile:).

In addition, this platform does not consider the OS, it is possible to run tests on Cisco, Cumulus, Juniper devices without changing the data structure.

#### Define inventory

1) You have to create a Nornir or an Ansible inventory (Example based on an Ansible Inventory)

`hosts` file.

```yaml
[leaf]
leaf01	# Cumulus Networks
leaf02	# Cisco Nexus 9k
leaf03	# Arista vEOS
leaf04	# Juniper Networks
leaf05	# Cisco IOS

[spine]
spine01	# Cumulus Networks
spine02	# Extreme Networks VSP
spine03	# Cisco IOS-XR
```

2) Define device parameters in ``host_vars/inventory_hostname.yml`` files

```yaml
hostname: 10.0.5.202
username: admin
password: Ci$co123
platform: linux			# <<=== specify device OS
port: 22
connexion: ssh
```

```yaml
hostname: 10.0.5.204
username: root
password: Jun1p3r
platform: junos			# <<=== specify device OS
port: 2222
connexion: ssh
```

```yaml
hostname: 10.0.5.203
username: admin
password: admin123
platform: eos				# <<=== specify device OS
port: 443
```

If `connexion: ssh` is not specify and the OS is supported by NAPALM, NAPALM will be used.

* Cumulus --->> SSH session on port 22
* Juniper --->> SSH session on port 2222
* Arista --->> REST API call on port 443

#### Define tests

Tests are defined in the file `verity/_test_to_execute.yml`. In this file you can define which test will be executed.

```yaml
# Each test can be in 3 types.
# 1) yes || true => (Mandatory) - If test failed Pipeline will be stopped
# 2) info =>  (Informations) - If test failed you will only see a message
# 3) no || false => (Exclude) - Test will not be executed
# Check Link Discovery Protocols sessions
lldp: true
```

In the same directory you can describe which LLDP sessions you want have on devices (`verity/lldp.yml`).

```yaml
spine01:
  - local_port: swp1
    neighbor_name: leaf01
    neighbor_port: swp1
  - local_port: swp2
    neighbor_name: leaf02
    neighbor_port: Eth1/1
  - local_port: swp3
    neighbor_name: leaf03
    neighbor_port: Eth1/1

leaf02:
  - local_port: Eth1/1
    neighbor_name: spine01
    neighbor_port: swp2
  - local_port: Eth1/7
    neighbor_name: leaf03
    neighbor_port: Eth1/3

leaf03:
  - local_port: Eth1/1
    neighbor_name: spine01
    neighbor_port: swp3
  - local_port: Eth1/3
    neighbor_name: leaf02.dh.local
    neighbor_port: Eth1/7
```

The script will connect on each device and retrieve LLDP sessions informations and campre them with the data define in ``verity/lldp.yml``.

If the informations are the same the tests is OK :smile:

#### Run the script

```shell
» ./main.py --ansible=True
[netests - main.py] BGP_SESSIONS tests are not executed !!
[netests - main.py] All BGP sessions tests are not executed !!
[netests - main.py] LLDP sessions are the same that defined in ./verity/lldp.yml = True
[netests - main.py] CDP sessions tests are not executed !!
[netests - main.py] VRF tests are not executed !!
[netests - main.py] Pings have not been executed !!
[netests - main.py] OSPF have not been executed !!
[netests - main.py] IPv4 addresses have not been executed !!
[netests - main.py] Static routes have not been executed !!
[netests - main.py] System informations have not been executed !!
```



#### BGP with VRF example

```yaml
---
spine01:
  default:
    asn: 65100
    router_id: 10.255.255.101
    neighbors:
      - peer_ip: 10.255.255.201
        remote_as: 65201
      - peer_ip: 10.255.255.202
        remote_as: 65202
      - peer_ip: 10.255.255.203
        remote_as: 65203
        state: DOWN
  mgmt:
    asn: 65100
    router_id: 1.1.1.1
    neighbors:
      - peer_ip: 10.0.5.203
        remote_as: 65203
        state: UP
      - peer_ip: 10.0.5.202
        remote_as: 65202
        state: DOWN


leaf02:
  default:
    asn: 65202
    router_id: 10.255.255.202
    neighbors:
      - peer_ip: 10.255.255.101
        remote_as: 65100

leaf03:
  default:
    asn: 65203
    router_id: 10.255.255.203
    neighbors:
      - peer_ip: 10.255.255.101
        remote_as: 65100
        state: UP
      - peer_ip: 10.255.255.202
        remote_as: 65202
```



## Capabilities (Only via SSH) LOT OF WORK

|           |      Juniper       |      Cumulus       | Arista             |        NXOS        |        IOS         |       IOS-XR       |    Extreme VSP     | NAPALM             |
| --------- | :----------------: | :----------------: | ------------------ | :----------------: | :----------------: | :----------------: | :----------------: | ------------------ |
| BGP       | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         |        :x:         | :white_check_mark: |
| OSPF      |        :x:         | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         |        :x:         |        :x:         | :x:                |
| SysInfos  | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         | :white_check_mark: | :white_check_mark: |
| Ping      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         | :white_check_mark: | :x:                |
| Socket    |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |        :x:         |        :x:         | :x:                |
| Static    |        :x:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         | :white_check_mark: | :x:                |
| VRF       |     :warning:      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :white_check_mark:         | :white_check_mark: |
| LLDP      |        :x:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         |        :x:         | :white_check_mark: |
| CDP       |      :sleepy:      | :white_check_mark: | :sleepy:           | :white_check_mark: | :white_check_mark: |        :x:         |      :sleepy:      | :sleepy:           |
| IPv4      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         |       :white_check_mark:         | :white_check_mark: |
| IPv6      |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |        :x:         |        :x:         | :x:                |
| MTU       |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |        :x:         |        :x:         | :x:                |
|           |                    |                    |                    |                    |                    |                    |                    |                    |
| MVP ^^^   |                    |                    |                    |                    |                    |                    |                    |                    |
|           |                    |                    |                    |                    |                    |                    |                    |                    |
| VTEP      |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |        :x:         |        :x:         | :x:                |
| Multicast |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |        :x:         |        :x:         | :x:                |
| VLAN      |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |        :x:         |        :x:         | :x:                |
| VXLAN     |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |        :x:         |        :x:         | :x:                |
| EVPN      |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |        :x:         |        :x:         | :x:                |
| IS-IS     |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |        :x:         |        :x:         | :x:                |

:white_check_mark: = Implemented

:warning: = Implemented but need to be verified

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



#### Cisco Nexus

port 22 is fix

```python
    elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM:
        # Nexus get_network_instances is not Implemented by NAPALM (November 2019)
        # File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/napalm/base/base.py", line 1535, in get_network_instances
        # raise NotImplementedError
        #   NotImplementedError
        if NEXUS_PLATEFORM_NAME == task.host.platform:
            port = task.host.port
            task.host.port = 22
            if function == 'GET':
                _nexus_get_vrf(task)
            elif function == 'LIST':
                _get_vrf_name_list(task)
            task.host.port = port
```







## TextFSM templates

Some templates have be retreieve on :

**https://github.com/networktocode/ntc-templates/tree/master/templates**



## Contributor

**Become a contributor** !!!
