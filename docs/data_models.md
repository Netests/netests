### BGP

```shell
⚡ netests --show-data-model bgp
```

```yaml

default:
  as_number: 65432
  router_id: 10.100.20.1
  neighbors: {}

NETESTS_VRF:
  as_number: 65432
  router_id: 10.1.20.1
  neighbors:
    - peer_hostname: NOT_SET
      peer_ip: 10.0.0.1
      prefix_received: 0
      remote_as: 65111
      session_state: Active
      src_hostname: leaf01
      state_brief: DOWN
      state_time: 0

CUSTOMER_VRF:
  as_number: 65432
  router_id: 10.1.20.1
  neighbors:
    - peer_ip: 10.0.0.1000
      remote_as: 65100
      state_brief: DOWN

```



### CDP

```shell
⚡ netests --show-data-model cdp
```

```yaml

- local_name: leaf01
  local_port: swp1
  neighbor_name: leaf03.dh.local
  neighbor_port: Ethernet1

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



### Facts

```shell
⚡ netests --show-data-model facts
```

```yaml

base_mac: 50:00:00:d7:ee:0b
build: da8d6269-c25f-4a12-930b-c3c42c12c38a
domain: dh.local
hostname: leaf03
interfaces_lst:
  - Management1
  - Ethernet8
  - Ethernet2
  - Ethernet3
  - Ethernet1
  - Ethernet6
  - Ethernet7
  - Ethernet4
  - Ethernet5
memory: 2014424
model: vEOS
serial: UEH29DB23DH0238DH023
vendor: Arista
version: 4.24.0F

```



### ISIS

```shell
⚡ netests --show-data-model isis
```

```yaml

```



### LLDP

```shell
⚡ netests --show-data-model lldp
```

```yaml

- local_name: leaf01
  local_port: swp1
  neighbor_name: leaf03.dh.local
  neighbor_port: Ethernet1

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



### OSPF

```shell
⚡ netests --show-data-model ospf
```

```yaml

hostname: leaf01
vrfs:
  - areas: []
    router_id: 51.51.51.51
    vrf_name: default

  - router_id: 151.151.151.151
    vrf_name: NETESTS_VRF
    areas:
      - area_number: 0.0.0.0
        neighbors:
          - local_interface: swp1
            peer_hostname: NOT_SET
            peer_ip: 10.1.2.2
            peer_rid: 53.53.53.53
            session_state: FULL
          - local_interface: swp2
            peer_ip: 10.1.20.2
            peer_rid: 62.62.62.62
            session_state: FULL

```



### PING

```shell
⚡ netests --show-data-model ping
```

```yaml

- ip: 127.0.0.1
  works: true
- ip: 8.8.8.8
  works: false
- ip: 172.16.194.111
  works: false
- ip: 172.16.194.1
  vrf: mgmt
  works: false
- ip: 172.16.194.1
  vrf: ewfjweijfoeirjfer
  works: false

```



### VLAN

```shell
⚡ netests --show-data-model vlan
```

```yaml

- id: 1
  name: default
  vrf_name: default
  ipv4_addresses:
    - ip_address: 1.1.1.1
      netmask: 255.0.0.0
    - ip_address: 10.1.1.2
      netmask: 255.255.255.255
  ipv6_addresses:
    - ip_address: 2001:cafe::1
      netmask: 64
    - ip_address: 2001:c0ca::1
      netmask: 64
  assigned_ports:
    - swp1
    - swp2
    - swp3

```



### VRF

```shell
⚡ netests --show-data-model vrf
```

```yaml

- exp_targ: NOT_SET
  imp_targ: NOT_SET
  l3_vni: NOT_SET
  rd: NOT_SET
  rt_exp: NOT_SET
  rt_imp: NOT_SET
  vrf_id: 1000
  vrf_name: default
  vrf_type: NOT_SET
- vrf_name: NETESTS_VRF
- rd: 65123:1
  rt_exp: 65123:100
  rt_imp: 65123:200
  vrf_id: '1002'
  vrf_name: mgmt

```

