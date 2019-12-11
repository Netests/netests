# OSPF - Netests.io
###### <dylan.hamel@protonmail.com> - Nov. 2019



## OSPF Definition

```python
class OSPFSession:
    hostname: str
    peer_rid: str

    # The following values are not used by the __eq__ function !!
    # But are used by th adv_eq1 function
    local_interface: str
    peer_ip: str

    # The following values are not used by the __eq__ and adv1_eq functions !!
    # But are used by th adv_eq3 function
    session_state: str

    # The following values are not used by the __eq__, adv1_eq, adv2_eq functions !!
    peer_hostname: str
```



## OSPF`__eq__`

```python
    def __eq__(self, other):
        if not isinstance(other, OSPFSession):
            return NotImplemented

        return ((str(self.hostname) == str(other.hostname)) and
                (str(self.local_interface) == str(other.local_interface)) and
                (str(self.peer_rid) == str(other.peer_rid)))
```

Other parameters are not included in the comparaison function and can be different.



### OSPF Retrieve Data

|             | hostname           | peer_rid           | local_interface    | peer_ip            | session_state      | peer_hostname |
| ----------- | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------- |
| NAPALM      | :x:                | :x:                | :x:                | :x:                | :x:                | :x:           |
| Junos       | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:           |
| Cumulus     | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:           |
| Arista      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:           |
| Cisco Nexus | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:           |
| Cisco IOS   | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:           |
| Extreme VSP | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:           |
|             |                    |                    |                    |                    |                    |               |
|             |                    |                    |                    |                    |                    |               |
|             |                    |                    |                    |                    |                    |               |
|             |                    |                    |                    |                    |                    |               |

:white_check_mark: => Supported

:x: => Not Supported

:cry: => Not Implemented

