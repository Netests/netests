# Static - Netests.io
###### <dylan.hamel@protonmail.com> - Nov. 2019



## Static Definition

StaticRoute is defined as follow:

* route is in a vrf (for example ``default``)

* route has a prefix (for example ``10.0.0.0``)

* route has a net mask (for example ``255.0.0.0``)

* route has a `ListNexthop` (`ListNexthop` is a Python Object)

  ListNexthop is defined as follow:

  * Contains a list of `Nexthop` (`Nexthop` is a Python Object)

    Nexthop is defined as follow:

    * nexthop has an ip_address

    * nexthop is connected on a physical or logical interface

    * nexthop has a preference value

    * nexthop has a metric value

    * nexthop is active or not

    * nexthop is in FIB or not

      

#### Nexthop

```python
class Nexthop:
    ip_address: str
    is_in_fib: str
    out_interface: str
    preference: str  # or distance
    metric: str
    active: str
```

#### Static

```python
class Static:
    vrf_name: str
    prefix: str
    netmask: str
    nexthop: ListNexthop
```



## Static comparaison function `__eq__`

#### Nexthop

```python
    def __eq__(self, other):
        if not isinstance(other, Static):
            return NotImplemented

        return ((str(self.vrf_name) == str(other.vrf_name)) and
                (str(self.prefix) == str(other.prefix)) and
                (str(self.netmask) == str(other.netmask)) and
                (self.nexthop == other.nexthop))
```

#### Static

```python
    def __eq__(self, other):
        if not isinstance(other, Nexthop):
            return NotImplemented

        # Basic
        return (str(self.ip_address) == str(other.ip_address))
```

Other parameters are not included in the comparaison function and can be different.



## Static Retrieve Data

|             | vrf_name           | prefix             | netmask            | nexthop            |
| ----------- | ------------------ | ------------------ | ------------------ | ------------------ |
| NAPALM      | :x:                | :x:                | :x:                | :x:                |
| Junos       | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cumulus     | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Arista      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco Nexus | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco IOS   | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Extreme VSP | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
|             |                    |                    |                    |                    |
|             |                    |                    |                    |                    |
|             |                    |                    |                    |                    |
|             |                    |                    |                    |                    |



## NextHop Retrieve Data

|             | ip_address | is_in_fib | out_interface | preference | metric | active |
| ----------- | ---------- | --------- | ------------- | ---------- | ------ | ------ |
| NAPALM      | ❌          | ❌         | ❌             | ❌          | ❌      | ❌      |
| Junos       | ✅          | :o:       | ✅             | ✅          | ✅      | :o:    |
| Cumulus     | ✅          | ✅         | ✅             | ✅          | ✅      | ✅      |
| Arista      | ✅          | :o:       | ✅             | ✅          | ✅      | :o:    |
| Cisco Nexus | ✅          | :o:       | ✅             | ✅          | ✅      | :o:    |
| Cisco IOS   | ✅          | ✅         | ✅             | ✅          | ✅      | ✅      |
| Extreme VSP | ✅          | ✅         | ❌             | ✅          | ✅      | ✅      |
|             |            |           |               |            |        |        |
|             |            |           |               |            |        |        |
|             |            |           |               |            |        |        |
|             |            |           |               |            |        |        |

✅ : Implemented

*:o: : Always True

❌ : Not supported



*Why always True ?

```python
nexthop_obj = Nexthop(
    ip_address=nexthop.get('ipnexthop', NOT_SET),
    is_in_fib=nexthop.get('always_true_in_nexus', True),
    out_interface=NOT_SET,
    preference=nexthop.get('pref', NOT_SET),
    metric=nexthop.get('metric', NOT_SET),
    active=nexthop.get('always_true_in_nexus', True),
)
```

If nexthop is not reachable, route will be not in the RIB. So if you retrieve route, the route is in the RIB



## Error, Miss & Improve

Juniper retrieve information about "inet".

```python
            "table-name" : [
            {
                "data" : "mgmt_junos.inet.0"
            }
```

Code remove `.inet.0` in ``static_converters.py``.

```python
# Example of default table route => "data" : "inet.0"
if instance_route.get("table-name")[0].get("data") == "inet.0":
    vrf_name = "default"
else:
    index_dot = instance_route.get("table-name")[0].get("data").find(".")
    vrf_name = instance_route.get("table-name")[0].get("data")[:index_dot]
```

