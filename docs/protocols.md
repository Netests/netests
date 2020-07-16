Each protocol has a different way to compare.
Only few parameters are used in the compare function by default.

You can define in Netests.io configuration file which parameter will be used in the compare function.

## Compare

Below you will find which parameters are invole in the compare function by protocol.

### BGP

In the BGP function the following parameters will be compare.

1. `src_hostname` this parameter is not important because is set based on your inventory
2. peer_ip
3. remote_as
4. `state_brief` can only be `UP` or `DOWN`

Some other parameters are also compared :

5. router_id
6. as_number
7. vrf_name

#### Parameter not compare

These values are not compare by default, it is possible to add them in the compare function

=> Check `Modify compared values`.

* peer_hostname
* session_state
* state_time
* prefix_received

These values are retrieved to have more informations and for some next features.

#### Compare function

```python
class BGPSessionsVRF:
  	def __eq__(self, other):
        if not isinstance(other, BGPSession):
            return NotImplementedError
        return (
            (str(self.src_hostname) == str(other.src_hostname)) and
            (str(self.peer_ip) == str(other.peer_ip)) and
            (str(self.state_brief) == str(other.state_brief)) and
            (str(self.remote_as) == str(other.remote_as))
        )
```

```python
class BGPSessionsVRF:
  	def __eq__(self, other):
        if not isinstance(other, BGPSessionsVRF):
            raise NotImplementedError

        return (
            (str(self.vrf_name) == str(other.vrf_name)) and
            (str(self.as_number) == str(other.as_number)) and
            (str(self.router_id) == str(other.router_id)) and
            (self.bgp_sessions == other.bgp_sessions)
```

```python
class BGP:
  	def __eq__(self, other):
        if not isinstance(other, BGP):
            raise NotImplementedError

        return (
            (str(self.hostname) == str(other.hostname)) and
           
```

#### Modify compared values

It's possible to add or remove some value from the compare function.

To do that, Modifiy Netests.io configuration file by adding `compare:` in protocols `options:`

```yaml
config:
  protocols:
    bgp:
      test: true
      options:
        compare:
          src_hostname: true
          peer_ip: true
          remote_as: true
          state_brief: true
          peer_hostname: false
          session_state: true
          state_time: false
          prefix_received: true
```

In this example `prefix_received` and `session_state` are added to BGP compare function



### CDP

In the CDP function the following parameters will be compare.

1. local_name
2. local_port
3. neighbor_name
4. neighbor_port

#### Parameter not compare

These values are not compare by default, it is possible to add them in the compare function

=> Check `Modify compared values`.

* neighbor_os
* neighbor_mgmt_ip
* neighbor_type

These values are retrieved to have more informations and for some next features.

#### Compare function

```python
class CDP(DiscoveryProtocols):
		def __eq__(self, other):
        if not isinstance(other, CDP):
            return NotImplementedError()

        return (self.local_name == other.local_name and
                self.local_port == other.local_port and
                self.neighbor_name == other.neighbor_name and
                self.neighbor_port == other.neighbor_port)
```

#### Modify compared values

It's possible to add or remove some value from the compare function.

To do that, Modifiy Netests.io configuration file by adding `compare:` in protocols `options:`

```yaml
config:
  protocols:
    cdp:
      test: true
      options:
        compare:
          local_name: true
          local_port: true
          neighbor_name: true
          neighbor_port: true
          neighbor_os: true
          neighbor_mgmt_ip: true
          neighbor_type: false
```

In this example `neighbor_os` and `neighbor_port` are added to CDP compare function



### Facts

In the Facts function the following parameters will be compare.

1. hostname
2. version

#### Parameter not compare 

These values are not compare by default, it is possible to add them in the compare function

=> Check `Modify compared values`.

* domain
* build
* serial
* base_mac
* memory
* vendor
* model
* interfaces_lst

#### Compare function

```python
class Facts:
		def __eq__(self, other):
        if not isinstance(other, Facts):
            return NotImplemented

        return ((str(self.hostname) == str(other.hostname)) and
                (str(self.version) == str(other.version)))
```

#### Modify compared values

It's possible to add or remove some value from the compare function.

To do that, Modifiy Netests.io configuration file by adding `compare:` in protocols `options:`

```yaml
config:
  protocols:
    facts:
      test: false
      options:
        compare:
          hostname: True
          domain: true
          version: True
          build: false
          serial: true
          base_mac: false
          memory: false
          vendor: false
          model: false
          interfaces_lst: false
```

In this example `serial` and `domain` are added to Facts compare function



### ISIS

In the ISIS function the following parameters will be compare.

1. session_state
2. level_type
3. neighbor_sys_name

#### Parameter not compare

These values are not compare by default, it is possible to add them in the compare function

=> Check `Modify compared values`.

* circuit_type
* local_interface_name
* neighbor_ip_addr
* snap

These values are retrieved to have more informations and for some next features.

#### Compare function

```python
class ISISAdjacency(NetestsProtocol):
    def __eq__(self, other):
        if not isinstance(other, ISISAdjacency):
            raise NotImplementedError()
        
        return (
                self.session_state == other.session_state and
                self.level_type == other.level_type and
                self.neighbor_sys_name == other.neighbor_sys_name
            )
```

#### Modify compared values

It's possible to add or remove some value from the compare function.

To do that, Modifiy Netests.io configuration file by adding `compare:` in protocols `options:`

```yaml
config:
  protocols:
    isis:
      test: true
      options:
        compare:
          session_state: true
          level_type: true
          neighbor_sys_name: true
          circuit_type: true
          local_interface_name: false
          neighbor_ip_addr: false
          snap: true
```

In this example `snap` and `circuit_type` are added to ISIS compare function

### LLDP

In the LLDP function the following parameters will be compare.

1. local_name
2. local_port
3. neighbor_name
4. neighbor_port

#### Parameter not compare

These values are not compare by default, it is possible to add them in the compare function

=> Check `Modify compared values`.

* neighbor_os
* neighbor_mgmt_ip
* neighbor_type

These values are retrieved to have more informations and for some next features.

#### Compare function

```python
class LLDP(DiscoveryProtocols):
		def __eq__(self, other):
        if not isinstance(other, LLDP):
            return NotImplementedError()

        return (self.local_name == other.local_name and
                self.local_port == other.local_port and
                self.neighbor_name == other.neighbor_name and
                self.neighbor_port == other.neighbor_port)
```

#### Modify compared values

It's possible to add or remove some value from the compare function.

To do that, Modifiy Netests.io configuration file by adding `compare:` in protocols `options:`

```yaml
config:
  protocols:
    lldp:
      test: true
      options:
        compare:
          src_hostname: true
          peer_ip: true
          remote_as: true
          state_brief: true
          peer_hostname: false
          session_state: true
          state_time: false
          prefix_received: true
```

In this example `prefix_received` and `session_state` are added to LLDP compare function



### OSPF

In the OSPF function the following parameters will be compare.

1. peer_rid
2. local_interface

Some other parameters are also compared :

5. area_number
6. vrf_name
7. router_id

#### Parameter not compare

These values are not compare by default, it is possible to add them in the compare function

=> Check `Modify compared values`.

* peer_ip
* session_state
* peer_hostname

These values are retrieved to have more informations and for some next features.

#### Compare function

```python
class OSPFSession:
		def __eq__(self, other):
        if not isinstance(other, OSPFSession):
            return NotImplemented

        return (
                (str(self.local_interface) == str(other.local_interface)) and
                (str(self.peer_rid) == str(other.peer_rid))
```

```python
class OSPFSessionsArea:
  	def __eq__(self, other):
        if not isinstance(other, OSPFSessionsArea):
            raise NotImplementedError()

        return ((str(self.area_number) == str(other.area_number)) and
                (self.ospf_sessions == other.ospf_sessions))
```

```python
class OSPFSessionsVRF:
  	def __eq__(self, other):
        if not isinstance(other, OSPFSessionsVRF):
            raise NotImplementedError()

        return ((str(self.vrf_name) == str(other.vrf_name)) and
                (str(self.router_id) == str(other.router_id)) and
                (self.ospf_sessions_area_lst == other.ospf_sessions_area_lst))
           
```

#### Modify compared values

It's possible to add or remove some value from the compare function.

To do that, Modifiy Netests.io configuration file by adding `compare:` in protocols `options:`

```yaml
config:
  protocols:
    ospf:
      test: true
      options:
        compare:
          peer_rid: true
          local_interface: true
          peer_ip: true
          session_state: true
          peer_hostname: false
```

In this example `peer_ip` and `session_state` are added to OSPF compare function



### PING

The ping is validate if it works.



### VLAN

In the VLAN function the following parameters will be compare.

1. id

#### Parameter not compare

These values are not compare by default, it is possible to add them in the compare function

=> Check `Modify compared values`.

* vlan_name

* vrf_name
* ipv4_addresses
* ipv6_addresses
* assigned_ports

These values are retrieved to have more informations and for some next features.

#### Compare function

```python
class VLAN(NetestsProtocol):
    def __eq__(self, other):
      if not isinstance(other, VLAN):
            raise NotImplementedError()

      return self.id == other.id
```

#### Modify compared values

It's possible to add or remove some value from the compare function.

To do that, Modifiy Netests.io configuration file by adding `compare:` in protocols `options:`

```yaml
config:
  protocols:
    vrf:
      test: false
      options:
        compare:
          id: True
          name: True
          vrf_name: false
          ipv4_addresses: false
          ipv6_addresses: True
          assigned_ports: True
```

In this example `name`, `ipv6_addresses ` and `assigned_ports` are added to VLAN compare function



### VRF

In the VRF function the following parameters will be compare.

1. vrf_name

#### Parameter not compare

These values are not compare by default, it is possible to add them in the compare function

=> Check `Modify compared values`.

* vrf_id
* vrf_type
* l3_vni
* rd
* rt_imp
* rt_exp
* imp_targ
* exp_targ

These values are retrieved to have more informations and for some next features.

#### Compare function

```python
class VRF:
  	def __eq__(self, other):
        if not isinstance(other, VRF):
            return NotImplementedError

        return ((str(self.vrf_name) == str(other.vrf_name)))
```

#### Modify compared values

It's possible to add or remove some value from the compare function.

To do that, Modifiy Netests.io configuration file by adding `compare:` in protocols `options:`

```yaml
config:
  protocols:
    vrf:
      test: false
      options:
        compare:
          vrf_name: True
          vrf_id: True
          vrf_type: false
          l3_vni: false
          rd: True
          rt_imp: True
          rt_exp: True
          imp_targ: false
          exp_targ: false
```

In this example `rd`, `rt_imp`, `rt_exp` and `vrf_id` are added to VRF compare function