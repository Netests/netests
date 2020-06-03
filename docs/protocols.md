Each protocol has a different way to compare.
Only few parameters are used in the compare function.

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



### CDP

In the CDP function the following parameters will be compare.

1. local_name
2. local_port
3. neighbor_name
4. neighbor_port

#### Parameter not compare 

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



### Facts

In the Facts function the following parameters will be compare.

1. hostname
2. version

#### Parameter not compare 

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



### LLDP

In the LLDP function the following parameters will be compare.

1. local_name
2. local_port
3. neighbor_name
4. neighbor_port

#### Parameter not compare 

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



### OSPF

In the OSPF function the following parameters will be compare.

1. peer_rid
2. local_interface

Some other parameters are also compared :

5. area_number
6. vrf_name
7. router_id

#### Parameter not compare 

* peer_ip
* session_state
* peer_hostname
* prefix_received

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



### VRF

In the VRF function the following parameters will be compare.

1. vrf_name

#### Parameter not compare 

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



## Informations

In the next release you will be able to define in the Netests.io configuration file which parameters will be compared.

```yaml
vrf:
      test: true
      options:
        compare:
          vrf_name: true
          vrf_id: true
          vrf_type: false
          l3_vni: false
          rd: true
          rt_imp: false
          rt_exp: false
          imp_targ: false
          exp_targ: false
```

With this configuration file `rd`, `vrf_name` and `vrf_id` will be compared.