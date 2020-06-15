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

