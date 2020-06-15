Each data models has been defined by the Netests.io Team and inspired by OpenConfig Data models.

Some values are not retrieve on many vendors.

Here the list of arguments retrieve by protocols for each vendor / OS.



## BGP

|                      | src_hostname       | peer_ip            | peer_hostname      | remote_as          | state_brief        | session_state      | state_time         | prefix_received    |
| -------------------- | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ |
| Arista API           | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Arista Netconf       | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Arista SSH           | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cumulus API          | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cumulus Netconf      | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cumulus SSH          | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Extreme VSP API      | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Extreme VSP Netconf  | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Extreme VSP SSH      | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         |
| Cisco IOS-XE API     | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco IOS-XE Netconf | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco IOS-XE SSH     | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco IOS-XR API     | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cisco IOS-XR Netconf | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         |
| Cisco IOS-XR SSH     | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         |
| Juniper API          | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         |
| Juniper Netconf      | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         |
| Juniper SSH          | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: |
| NAPALM               | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco NX-OS API      | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         |
| Cisco NX-OS Netconf  | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cisco NX-OS SSH      | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |

:white_check_mark: = Supported​

:warning: = Not Implemented

:no_entry: = Not Supported



## CDP

|                      | local_name         | local_port         | neighbor_name      | neighbor_port      | neighbor_os        | neighbor_mgmt_ip   | neighbor_type      |
| -------------------- | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ |
| Arista API           | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Arista Netconf       | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Arista SSH           | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cumulus API          | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cumulus Netconf      | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cumulus SSH          | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Extreme VSP API      | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Extreme VSP Netconf  | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Extreme VSP SSH      | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cisco IOS-XE API     | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cisco IOS-XE Netconf | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cisco IOS-XE SSH     | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco IOS-XR API     | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cisco IOS-XR Netconf | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cisco IOS-XR SSH     | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Juniper API          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Juniper Netconf      | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Juniper SSH          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| NAPALM               | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cisco NX-OS API      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco NX-OS Netconf  | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cisco NX-OS SSH      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |



## Facts

|                      | hostname           | domain             | version            | build              | serial             | base_mac           | memory             | vendor             | model              | interfaces_lst     |
| -------------------- | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ |
| Arista API           | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Arista Netconf       | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Arista SSH           | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cumulus API          | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cumulus Netconf      | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cumulus SSH          | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Extreme VSP API      | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: |
| Extreme VSP Netconf  | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Extreme VSP SSH      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco IOS-XE API     | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :no_entry:         | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco IOS-XE Netconf | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :no_entry:         | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco IOS-XE SSH     | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco IOS-XR API     | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cisco IOS-XR Netconf | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cisco IOS-XR SSH     | :white_check_mark: | :no_entry:         | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Juniper API          | :white_check_mark: | :no_entry:         | :white_check_mark: | :no_entry:         | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Juniper Netconf      | :white_check_mark: | :no_entry:         | :white_check_mark: | :no_entry:         | :white_check_mark: | :no_entry:         | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Juniper SSH          | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| NAPALM               | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :no_entry:         | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco NX-OS API      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco NX-OS Netconf  | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cisco NX-OS SSH      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |





## LLDP

|                      | local_name         | local_port         | neighbor_name      | neighbor_port      | neighbor_os        | neighbor_mgmt_ip   | neighbor_type      |
| -------------------- | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ |
| Arista API           | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Arista Netconf       | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Arista SSH           | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cumulus API          | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cumulus Netconf      | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cumulus SSH          | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Extreme VSP API      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         |
| Extreme VSP Netconf  | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Extreme VSP SSH      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco IOS-XE API     | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cisco IOS-XE Netconf | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cisco IOS-XE SSH     | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco IOS-XR API     | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cisco IOS-XR Netconf | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cisco IOS-XR SSH     | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         | :white_check_mark: |
| Juniper API          | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         |
| Juniper Netconf      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         |
| Juniper API          | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         |
| NAPALM               | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: |
| Cisco NX-OS API      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Cisco NX-OS Netconf  | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cisco NX-OS SSH      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |



## OSPF

|                      | peer_rid           | session_state      | peer_hostname | local_interface    | peer_ip            |
| -------------------- | ------------------ | ------------------ | ------------- | ------------------ | ------------------ |
| Arista API           | :white_check_mark: | :white_check_mark: | :no_entry:    | :white_check_mark: | :white_check_mark: |
| Arista Netconf       | :warning:          | :warning:          | :warning:     | :warning:          | :warning:          |
| Arista SSH           | :white_check_mark: | :white_check_mark: | :no_entry:    | :white_check_mark: | :white_check_mark: |
| Cumulus API          | :white_check_mark: | :white_check_mark: | :no_entry:    | :white_check_mark: | :white_check_mark: |
| Cumulus Netconf      | :warning:          | :warning:          | :warning:     | :warning:          | :warning:          |
| Cumulus SSH          | :white_check_mark: | :white_check_mark: | :no_entry:    | :white_check_mark: | :white_check_mark: |
| Extreme VSP API      | :warning:          | :warning:          | :warning:     | :warning:          | :warning:          |
| Extreme VSP Netconf  | :warning:          | :warning:          | :warning:     | :warning:          | :warning:          |
| Extreme VSP SSH      | :white_check_mark: | :white_check_mark: | :no_entry:    | :no_entry:         | :white_check_mark: |
| Cisco IOS-XE API     | :warning:          | :warning:          | :warning:     | :warning:          | :warning:          |
| Cisco IOS-XE Netconf | :warning:          | :warning:          | :warning:     | :warning:          | :warning:          |
| Cisco IOS-XE SSH     | :white_check_mark: | :white_check_mark: | :no_entry:    | :white_check_mark: | :white_check_mark: |
| Cisco IOS-XR API     | :warning:          | :warning:          | :warning:     | :warning:          | :warning:          |
| Cisco IOS-XR Netconf | :warning:          | :warning:          | :warning:     | :warning:          | :warning:          |
| Cisco IOS-XR SSH     | :warning:          | :warning:          | :warning:     | :warning:          | :warning:          |
| Juniper API          | :white_check_mark: | :white_check_mark: | :no_entry:    | :white_check_mark: | :white_check_mark: |
| Juniper Netconf      | :white_check_mark: | :white_check_mark: | :no_entry:    | :white_check_mark: | :white_check_mark: |
| Juniper SSH          | :white_check_mark: | :white_check_mark: | :no_entry:    | :white_check_mark: | :white_check_mark: |
| NAPALM               | :warning:          | :warning:          | :warning:     | :warning:          | :warning:          |
| Cisco NX-OS API      | :white_check_mark: | :white_check_mark: | :no_entry:    | :white_check_mark: | :white_check_mark: |
| Cisco NX-OS Netconf  | :warning:          | :warning:          | :warning:     | :warning:          | :warning:          |
| Cisco NX-OS SSH      | :white_check_mark: | :white_check_mark: | :no_entry:    | :white_check_mark: | :white_check_mark: |



## PING

Ping value are logically not retrieved from the devices :smiley_cat:



## VLAN

|                      | id                 | name               | vrf_name   | ipv4_addresses     | ipv6_addresses     | assigned_port |
| -------------------- | ------------------ | ------------------ | ---------- | ------------------ | ------------------ | ------------- |
| Arista API           |                    |                    |            |                    |                    |               |
| Arista Netconf       |                    |                    |            |                    |                    |               |
| Arista SSH           |                    |                    |            |                    |                    |               |
| Cumulus API          |                    |                    |            |                    |                    |               |
| Cumulus Netconf      | :warning:          | :warning:          | :warning:  | :warning:          | :warning:          | :warning:     |
| Cumulus SSH          | :white_check_mark: | :white_check_mark: | :no_entry: | :white_check_mark: | :white_check_mark: | :no_entry:    |
| Extreme VSP API      |                    |                    |            |                    |                    |               |
| Extreme VSP Netconf  |                    |                    |            |                    |                    |               |
| Extreme VSP SSH      |                    |                    |            |                    |                    |               |
| Cisco IOS-XE API     |                    |                    |            |                    |                    |               |
| Cisco IOS-XE Netconf |                    |                    |            |                    |                    |               |
| Cisco IOS-XE SSH     |                    |                    |            |                    |                    |               |
| Cisco IOS-XR API     |                    |                    |            |                    |                    |               |
| Cisco IOS-XR Netconf |                    |                    |            |                    |                    |               |
| Cisco IOS-XR SSH     |                    |                    |            |                    |                    |               |
| Juniper API          |                    |                    |            |                    |                    |               |
| Juniper Netconf      |                    |                    |            |                    |                    |               |
| Juniper SSH          |                    |                    |            |                    |                    |               |
| NAPALM               |                    |                    |            |                    |                    |               |
| Cisco NX-OS API      |                    |                    |            |                    |                    |               |
| Cisco NX-OS Netconf  |                    |                    |            |                    |                    |               |
| Cisco NX-OS SSH      |                    |                    |            |                    |                    |               |





## VRF

|                      | vrf_name           | vrf_id             | vrf_type           | l3_vni             | rd                 | rt_imp             | rt_exp             | imp_targ           | exp_targ           |
| -------------------- | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ | ------------------ |
| Arista API           | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         |
| Arista Netconf       | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         |
| Arista SSH           | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         |
| Cumulus API          | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         |
| Cumulus Netconf      | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cumulus SSH          | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         |
| Extreme VSP API      | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Extreme VSP Netconf  | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Extreme VSP SSH      | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         |
| Cisco IOS-XE API     | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         |
| Cisco IOS-XE Netconf | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         |
| Cisco IOS-XE SSH     | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         |
| Cisco IOS-XR API     | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          | :warning:          |
| Cisco IOS-XR Netconf | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         |
| Cisco IOS-XR SSH     | :white_check_mark: | :no_entry:         | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         |
| Juniper API          | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Juniper Netconf      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Juniper SSH          | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| NAPALM               | :white_check_mark: | :no_entry:         | :white_check_mark: | :no_entry:         | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         |
| Cisco NX-OS API      | :white_check_mark: | :white_check_mark: | :no_entry:         | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         |
| Cisco NX-OS Netconf  | :white_check_mark: | :no_entry:         | :no_entry:         | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         |
| Cisco NX-OS SSH      | :white_check_mark: | :white_check_mark: | :no_entry:         | :no_entry:         | :white_check_mark: | :no_entry:         | :no_entry:         | :no_entry:         | :no_entry:         |

