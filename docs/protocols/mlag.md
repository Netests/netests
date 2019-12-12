# MLAG - Netests.io
###### <dylan.hamel@protonmail.com> - Nov. 2019



## MLAG

```python
class MLAG:

    hostname: str
    local_id: str
    peer_id: str
    peer_alive: str
    peer_int: str
    peer_ip: str
    sys_mac: str

    # The following values are not used by the __eq__ function !!
    local_role: str
    peer_role: str
    local_priority: str
    peer_priority: str
    vxlan_anycast_ip: str
```



## MLAG comparaison function `__eq__`

```python
    def __eq__(self, other):
        if not isinstance(other, MLAG):
            return NotImplemented

        # Basic
        if (str(self.hostname) == str(self.hostname) and
                str(self.local_id) == str(other.local_id) and
                str(self.peer_id) == str(other.peer_id) and
                str(self.peer_int) == str(other.peer_int) and
                str(self.peer_ip) == str(other.peer_ip) and
                str(self.sys_mac) == str(other.sys_mac) and
                str(self.peer_alive) == str(other.peer_alive)):
            return True

        else:
            printline()
            print(self)
            print("IS NOT EQUAL TO\n")
            print(other)
            printline()
            return False
```

Other parameters are not included in the comparaison function and can be different.



## MLAG Retrieve Data

|             | hostname           | local_id           | peer_id            | peer_alive         | peer_int           | peer_ip            | sys_mac            | local_role         | peer_role          | local_priority     | peer_priority      | vxlan_anycast_ip   |
| ----------- | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ |
| NAPALM      | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  |
| Junos       | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  |
| Cumulus     | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Arista      | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  |
| Cisco Nexus | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  |
| Cisco IOS   | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  |
| Extreme VSP | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  | 😢                  |
|             |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |
|             |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |
|             |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |
|             |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |                    |

:white_check_mark: => Supported

:x: => Not Supported

:cry: => Not Implemented