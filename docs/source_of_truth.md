Below a brief explication how you can create your source of truth.

## Create folders

To avoir to create manually all folders. An arguments it available.

```shell
netests --init-folders
```

```shell
truth_vars
├── all
├── groups
└── hosts
```



### Create your source 

Netests.io offers an option to create all truth_vars.

If the networks is working well and to avoid to create manually each files `--init-data` is available.

This feature will connect to all devices in the inventory get all informations regarding protocols enabled in the `netests.yml` and create all files.

```shell
netests -x -i inventory/ansible/hosts -a netests.yml --init-data
```

* `hosts` (inventory file)

```shell
[leaf]
leaf01
```

* `host_vars/leaf01.yml` (that define `leaf01`)

```shell
hostname: 172.16.194.51
platform: linux
username: cumulus
password: CumulusLinux!
connexion: ssh
port: 22
```

* `netests.yml` Netests.io configuration file

```yaml
config:
  protocols:
    facts:
      test: true
    lldp:
      test: true
    ospf:
      test: true
```



#### Result:

```yaml
truth_vars
├── all
├── groups
└── hosts
    ├── leaf01
        ├── facts.yml
        ├── lldp.yml
        └── ospf.yml
```

Contents :

* `facts.yml`

```yaml
base_mac: '50:00:00:02:00:00'
build: Cumulus Linux 4.0.0
domain: NOT_SET
hostname: leaf01
interfaces_lst:
- swp5
- swp2
- swp3
- swp1
- swp6
- swp7
- swp4
- eth0
memory: 944388
model: VX
serial: '50:00:00:02:00:00'
vendor: Cumulus Networks
version: 4.0.0

```

* `lldp.yml`

```yaml
- local_name: leaf01
  local_port: swp1
  neighbor_mgmt_ip: 53.53.53.53
  neighbor_name: leaf03.dh.local
  neighbor_os: NOT_SET
  neighbor_port: Ethernet1
  neighbor_type:
  - Bridge
  - Router
- local_name: leaf01
  local_port: swp2
  neighbor_mgmt_ip: 172.16.194.62
  neighbor_name: spine02
  neighbor_os: VSP-8284XSQ (8.1.0.0)
  neighbor_port: 1/1
  neighbor_type:
  - Bridge
  - Router

```

* `ospf.yml`

```yaml
hostname: leaf01
vrfs:
- areas: []
  router_id: 51.51.51.51
  vrf_name: default
- areas:
  - area_number: 0.0.0.0
    neighbors:
    - local_interface: swp1
      peer_hostname: NOT_SET
      peer_ip: 10.1.2.2
      peer_rid: 53.53.53.53
      session_state: FULL
    - local_interface: swp2
      peer_hostname: NOT_SET
      peer_ip: 10.1.20.2
      peer_rid: 62.62.62.62
      session_state: FULL
  router_id: 151.151.151.151
  vrf_name: NETESTS_VRF

```



