# Netconf - Model

In this file you will file the list of model used by NetConf for **Cisco IOS-XR**.

## BGP

http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-bgp-cfg"

```python
bgp_config = m.get_config(
    source='running',
    filter=NETCONF_FILTER.format(
        '<bgp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-bgp-cfg"/>'
    )
).data_xml
```