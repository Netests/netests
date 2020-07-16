Here is a documentation to contribute to Netests.io

## Implement new protocols

There are many steps to implement a new protocols

### Create class

First step is to create a Pyhton class to define the protocols.

This class has to implement `NetestsProtocols` that is defined in `netests/protocols/_protocols.py`

* Class has to use `pydantic` and `typing`
* Class has to implement `to_json()`
* Class has to be flexible to define "own" comparaison and print function (use `options` parameter).

```shell
class VLAN(NetestsProtocol):
    id: Optional[int] = NOT_SET
    name: Optional[str] = NOT_SET
    vrf_name: Optional[str] = NOT_SET
    ipv4_addresses: Optional[IPV4Interface] = None
    ipv6_addresses: Optional[IPV6Interface] = None
    assigned_ports: Optional[List[str]] = list()
```



### Define constants for protocol

These constants are defined in `netests/constants.py`

```python
# ISIS CONSTANTES
ISIS_DATA_HOST_KEY = "isis_data"
ISIS_WORKS_KEY = "isis_works"
```

> * ISIS_DATA_HOST_KEY will store device data formatted with {{ Protocol }} Python class
> * ISIS_WORKS_KEY will defined if Python object is equal to source of truth.



### Write Compare function

This function is defined in `netests/comparators/{{ protocol }}_compare.py`. The goal is to compare data retrived from devices to source of truth.

```python
def _compare_isis(
    host_keys,
    hostname: str,
    groups: list,
    isis_host_data: ISIS,
    test=False,
    options={},
    task=Task
) -> bool:
    if (
        'own_vars' in options.keys() and
        options.get('own_vars') is not None and
        'enable' in options.get('own_vars').keys() and
        options.get('own_vars').get('enable') is True
    ):
        raise NetestsOverideTruthVarsKeyUnsupported()
    else:
        if test:
            isis_yaml_data = open_file(
                path="tests/features/src/isis_tests.yml"
            ).get(hostname)
        else:
            isis_yaml_data = select_host_vars(
                hostname=hostname,
                groups=groups,
                protocol="isis"
            )

        verity_isis = ISIS(
            isis_vrf_lst=list()
        )

        log.debug(
            "ISIS_DATA_HOST_KEY in host_keys="
            f"{ISIS_DATA_HOST_KEY in host_keys}\n"
            "isis_yaml_data is not None="
            f"{isis_yaml_data is not None}"
        )
        if (
            ISIS_DATA_HOST_KEY in host_keys and
            isis_yaml_data is not None
        ):
            for isis_vrf in isis_yaml_data:
                isis_adj_lst = ListISISAdjacency(
                    isis_adj_lst=list()
                )

                for i in isis_vrf.get('adjacencies'):
                    isis_adj_lst.isis_adj_lst.append(
                        ISISAdjacency(
                            session_state=i.get('session_state', NOT_SET),
                            level_type=i.get('level_type', NOT_SET),
                            circuit_type=i.get('circuit_type', NOT_SET),
                            local_interface_name=i.get(
                                'local_interface_name', NOT_SET
                            ),
                            neighbor_sys_name=i.get(
                                'neighbor_sys_name', NOT_SET
                            ),
                            neighbor_ip_addr=i.get(
                                'neighbor_ip_addr', NOT_SET
                            ),
                            snap=i.get('snap', NOT_SET)
                        )
                    )

                verity_isis.isis_vrf_lst.append(
                    ISISAdjacencyVRF(
                        router_id=isis_vrf.get('router_id', NOT_SET),
                        system_id=isis_vrf.get('system_id', NOT_SET),
                        area_id=isis_vrf.get('area_id', NOT_SET),
                        vrf_name=isis_vrf.get('vrf_name', NOT_SET),
                        adjacencies=isis_adj_lst,
                    )
                )

            log_compare(verity_isis, isis_host_data, hostname, groups)
            return verity_isis == isis_host_data

        else:
            log_no_yaml_data(
                "isis",
                ISIS_DATA_HOST_KEY,
                "ISIS_DATA_HOST_KEY",
                hostname,
                groups
            )
            return True
```



### Write getter

Each protocol has its own getter. A getter initialize a MAPPING function to select which worker will be executed based on : 

* `device_type` (Arista Networks, Cumulus Networks, Juniper, etc.).
* `connexion_type` (API, Netconf, SSH)

```python
class GetterVLAN(GetterBase):

    def __init__(
        self,
        nr,
        options,
        from_cli,
        num_workers,
        verbose,
        print_task_output,
        filename,
        protocol,
        key_store
    ):
        super().__init__(
            nr,
            options,
            from_cli,
            num_workers,
            verbose,
            print_task_output,
            filename,
            protocol,
            key_store,
        )
        self.init_mapping_function()
        
		def init_mapping_function(self):
        self.MAPPING_FUNCTION = {
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.function_not_implemented
            },
            self.CUMULUS_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.function_not_implemented
            },
            self.EXTREME_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.function_not_implemented
            },
            self.CISCO_IOS_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.function_not_implemented
            },
            self.CISCO_IOSXR_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.function_not_implemented
            },
            self.JUNOS_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.function_not_implemented
            },
            self.NEXUS_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.function_not_implemented
            }
        }
```

> self.function_not_implemented have to be replaced by the correct worker

It's needed to implement `compare` and `print_result` functions

```python
def compare(self):
		log.debug(f"CALL _compare_transit_vlan num_workers={self.num_workers}")
		data = self.devices.run(
				task=_compare_transit_vlan,
        on_failed=True,
        num_workers=self.num_workers
    )
    self._compare_result(data)

def print_result(self):
		self.print_protocols_result(VLAN_DATA_HOST_KEY, "vlan")
```

> VLAN_DATA_HOST_KEY has to be defined in `netests.constants`
>
> Compare function `_compare_transit_vlan` has to be defined in `netests.comparators.protocols_compare.py`



### Add data models

In `netests/data_models/{{ protocols }}.yml`

```shell
⚡ netests --show-data-model vlan
```

> Add tests !!

```shell
⚡ behave tests/features/data_models_tests.feature --no-capture
```





### Add Protocols in netests config file

Add new protocols in `netests/data_models/netests_detailed.yml` and `netests/data_models/netests.yml`

```yaml
config:
  protocols:
    bgp:
      test: true

    bgp_up:
      test: true

    cdp:
      test: true

    facts:
      test: true

    isis:
      test: True
```

And

```yaml
config:
  protocols:
    bgp:
      test: True
      options:
        compare:
          src_hostname: True
          peer_ip: True
          remote_as: True
          state_brief: True
          peer_hostname: False
          session_state: False
          state_time: False
          prefix_received: False
        print:
          src_hostname: True
          peer_ip: True
          remote_as: True
          state_brief: True
          peer_hostname: True
          session_state: True
          state_time: True
          prefix_received: True
```



### Add in mapping function

Add the protocol in `netests/base_protocols.py`.

```python
    "isis": {
        "proto": ISIS,
        "class": GetterISIS,
        "filename": "isis.yml",
        "key_store": ISIS_DATA_HOST_KEY
    },
```

