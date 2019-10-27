# netests

Create your environnement :

```shell
» python3 -m venv .
» source ./bin/activate

(netests) ------------------------------------------------------------
(master*) »

» pip install --upgrade pip
» pip --version
pip 19.2.3
```


## Output

Commands ``/main.py``

```shell
{'bgp': True, 'bgp_up': True}
{'spine01': Host: spine01, 'leaf02': Host: leaf02, 'leaf03': Host: leaf03}
start get_bgp
{'spine01': Host: spine01, 'leaf02': Host: leaf02, 'leaf03': Host: leaf03}
Start generic_get with spine01 - linux - {} dict_keys(['syslog', 'asn']) - False
Start generic_get with leaf02 - nxos - {'connexion': 'ssh'} dict_keys(['connexion', 'syslog', 'vlans']) - TrueStart _cumulus_get_bgp with spine01
Start generic_get with leaf03 - eos - {'connexion': 'ssh'} dict_keys(['connexion', 'syslog', 'vlans']) - True

Start _nexus_get_bgp with leaf02Start _arista_get_bgp with leaf03

<class 'protocols.bgp.BGP'> <BGP hostname=spine01 as_number=65100 router_id=10.255.255.101 bgp_sessions=<ListBGPSessions 
<BGPSession src_hostname=spine01 peer_ip=10.255.255.201 peer_hostname=leaf01 remote_as=65201>
<BGPSession src_hostname=spine01 peer_ip=10.255.255.202 peer_hostname=NOT_SET remote_as=65202>
<BGPSession src_hostname=spine01 peer_ip=10.255.255.203 peer_hostname=NOT_SET remote_as=65203>

>>
 
[netests - get_bgp] No plateform selected...
<class 'protocols.bgp.BGP'> <BGP hostname=leaf02 as_number=65202 router_id=10.255.255.202 bgp_sessions=<ListBGPSessions 
<BGPSession src_hostname=leaf02 peer_ip=10.255.255.101 peer_hostname=NOT_SET remote_as=65100>
<BGPSession src_hostname=leaf02 peer_ip=10.255.255.203 peer_hostname=NOT_SET remote_as=65203>

>>
 
<class 'protocols.bgp.BGP'> <BGP hostname=leaf03 as_number=65203 router_id=10.255.255.203 bgp_sessions=<ListBGPSessions 
<BGPSession src_hostname=leaf03 peer_ip=10.255.255.202 peer_hostname=NOT_SET remote_as=65202>
<BGPSession src_hostname=leaf03 peer_ip=10.255.255.101 peer_hostname=NOT_SET remote_as=65100>

```