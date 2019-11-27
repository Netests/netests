# BGP - Netests.io
###### <dylan.hamel@protonmail.com> - Nov. 2019



## BGP Definition

A BGP object is define as follow:

1. A BGP object contains a list of VRF instance containing VRF instance

   1. VRF instance contain a **router-id**, **vrf-name** and a **ListOfBGPSessions**.

      1. A BGP Sessions contains:

         ```python
         src_hostname: str
         peer_ip: str
         remote_as: str
         state_brief: str
         peer_hostname: str
         session_state: str
         state_time: str
         prefix_received: str
         ```

```
BGP
  hostname
	ListBGPSessionsVRF
		- vrf_name
			as_number
			router_id
			ListBGPSessions
				- src_hostname
			    peer_ip
    			remote_as
			    state_brief
			    peer_hostname
			    session_state
			    state_time
			    prefix_received
			    
		- vrf_name2
			as_number
			router_id
			ListBGPSessions
				- src_hostname
			    peer_ip
    			remote_as
			    state_brief
			    peer_hostname
			    session_state
			    state_time
			    prefix_received
			
```



## BGP comparaison function `__eq__`

```python
    def __eq__(self, other):
        if not isinstance(other, BGPSession):
            return NotImplemented

        return ((str(self.src_hostname) == str(other.src_hostname)) and
                (str(self.peer_ip) == str(other.peer_ip)) and
                (str(self.state_brief) == str(other.state_brief)) and
                (str(self.remote_as) == str(other.remote_as)))
```

Other parameters are not included in the comparaison function and can be different.



### BGP Retrieve Data

|             | src_hostname       | peer_ip            | peer_hostname | remote_as          | state_brief        | sessions_state     | state_time         | prefix_received           |
| ----------- | ------------------ | ------------------ | ------------- | ------------------ | ------------------ | ------------------ | ------------------ | ------------------------- |
| NAPALM      |                    |                    |               |                    |                    |                    |                    |                           |
| Junos       | :white_check_mark: | :white_check_mark: | :x:           | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark:  If UP |
| Cumulus     |                    |                    |               |                    |                    |                    |                    |                           |
| Arista      |                    |                    |               |                    |                    |                    |                    |                           |
| Cisco Nexus |                    |                    |               |                    |                    |                    |                    |                           |
| Cisco IOS   | :white_check_mark: | :white_check_mark: | :x:           | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                       |
|             |                    |                    |               |                    |                    |                    |                    |                           |
|             |                    |                    |               |                    |                    |                    |                    |                           |
|             |                    |                    |               |                    |                    |                    |                    |                           |
|             |                    |                    |               |                    |                    |                    |                    |                           |
|             |                    |                    |               |                    |                    |                    |                    |                           |

