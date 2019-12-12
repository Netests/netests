# Netests.io

###### <dylan.hamel@protonmail.com> - November 2019 - Copyright

![logo.png](./images/logo.png)

## Install

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

E-mail me at <dylan.hamel@protonmail.com> with your Telegram ID to join the chat :smiley:.



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
| --------- | :----------------: | ------------------ | :----------------: | :----------------: | :----------------: | :----------------: | ------------------ | :----------------: |
| BGP       | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         | :white_check_mark: | :white_check_mark: |
| OSPF      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         | :white_check_mark: | :sleepy:        |
| SysInfos  | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         | :white_check_mark: | :white_check_mark: |
| Ping      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         | :white_check_mark: | :sleepy:        |
| Socket    |        :x:         | :white_check_mark:* | :x:                |        :x:         |        :x:         |        :x:         |        :x:         | :x:                |
| Static    | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         | :white_check_mark: | :sleepy:        |
| VRF       | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :white_check_mark:         | :white_check_mark: |
| LLDP      |        :x:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         | :white_check_mark: | :white_check_mark: |
| CDP       |      :sleepy:      | :white_check_mark: | :sleepy:           | :white_check_mark: | :white_check_mark: |        :x:         |      :sleepy:      | :sleepy:           |
| IPv4      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         |       :white_check_mark:         | :white_check_mark: |
| IPv6      |        :x:         |        :x:         | :x:                |        :x:         |        :x:         |        :x:         |        :x:         | :x:                |
| MTU       | :white_check_mark: |        :white_check_mark:        | :white_check_mark: | :white_check_mark: | :white_check_mark: |        :x:         | :white_check_mark: | :sleepy:*       |
| MLAG | :x: | :white_check_mark: | :x: | :x: | :x: | :x: | :x: | :sleepy: |
| L2VNI | :x: | :x: | :x: | :x: | :x: | :x: | :x: | :sleepy: |
| VLAN | :x: | :x: | :x: | :x: | :x: | :x: | :x: | :x: |
|  | | | | | | | | |
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

*`[Cumulus - Socket]` => netcat must be installed on Cumulus devices ``sudo apt install netcat``.



## Devices supported by NAPALM

|      Juniper       | Cumulus |       Arista       |     Cisco NXOS     |    Cisco IOS-XR    |     Cisco IOS      | Extreme |
| :----------------: | :-----: | :----------------: | :----------------: | :----------------: | :----------------: | :-----: |
| :white_check_mark: |   :x:   | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |   :x:   |
|       junos        |   ---   |        eos         |        nxos        |       iosxr        |        ios         |   ---   |

For the moment Cumulus Linux is only compatible with SSH. Utilization with REST API is int development.



## Road Map

Join the Telegram channel to have access to Trello



## Pipeline

|             | MTU                | MLAG               | IPv4 | IPv6 | Static             | BGP                | OSPF               | SysInfos           | CDP  | LLDP | VRF  | Ping | Socket |
| ----------- | ------------------ | ------------------ | ---- | ---- | ------------------ | ------------------ | ------------------ | ------------------ | ---- | ---- | ---- | ---- | ------ |
| Juniper     |                    |                    |      |      | :white_check_mark: |                    | :white_check_mark: |                    |      |      |      |      |        |
| Cumulus     | :white_check_mark: | :white_check_mark: |      |      |                    | :white_check_mark: | :white_check_mark: |                    |      |      |      |      |        |
| Arista      | :white_check_mark: |                    |      |      | :white_check_mark: |                    |                    |                    |      |      |      |      |        |
| Nexus       | :white_check_mark: |                    |      |      |                    |                    |                    | :white_check_mark: |      |      |      |      |        |
| IOS         |                    |                    |      |      |                    |                    | :white_check_mark: |                    |      |      |      |      |        |
| Extreme VSP |                    |                    |      |      |                    | :white_check_mark: | :white_check_mark: |                    |      |      |      |      |        |



## TextFSM templates

Some templates have be retreieve on :

**https://github.com/networktocode/ntc-templates/tree/master/templates**



## Contributor

**Become a contributor** !!!



## *NAPALM

In the documentation MTU is retrieve with `get_interfaces()` function : 
https://napalm.readthedocs.io/en/latest/base.html#napalm.base.base.NetworkDriver.get_interfaces

But actually...

```json
													'em3': {   'description': '',
                                     'is_enabled': True,
                                     'is_up': True,
                                     'last_flapped': 1506443.0,
                                     'mac_address': '50:00:00:06:00:03',
                                     'speed': 1000},
                          'em3.0': {   'description': 'TO_SPINE01',
                                       'is_enabled': True,
                                       'is_up': True,
                                       'last_flapped': 1506444.0,
                                       'mac_address': '50:00:00:06:00:03',
                                       'speed': 1000},
                          'em4': {   'description': '',
                                     'is_enabled': True,
                                     'is_up': True,
                                     'last_flapped': 1506443.0,
                                     'mac_address': '50:00:00:06:00:04',
                                     'speed': 1000},
                          'em4.32768': {   'description': '',
                                           'is_enabled': True,
                                           'is_up': True,
                                           'last_flapped': 1506444.0,
                                           'mac_address': '50:00:00:06:00:04',
                                           'speed': 1000},
```

