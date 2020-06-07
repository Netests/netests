Netests.io will be directly connected to the Ansible or Nornir inventory (Netbox is coming). You have to specify which inventory type will be used in the Netests.io running command :



### Ansible Inventory

```shell
netests -x -i inventory/ansible/hosts
```

```shell
-x, --ansible-inventory         Specify that an Ansible inventory will be
                                  used.
```

With Ansible inventory the variables defined in `host_vars`, `group_vars` will be retrieved.

```shell
⚡ cat inventory/ansible/hosts
[leaf]
leaf01
leaf02
leaf03
leaf04
leaf05

[spine]
spine01
spine02
spine03

⚡ tree inventory/ansible
inventory/ansible
├── group_vars
│   ├── leaf.yml
│   ├── spine.yml
│   └── all.yml
├── host_vars
│   ├── leaf01.yml
│   ├── leaf02.yml
│   ├── leaf03.yml
│   ├── leaf04.yml
│   ├── leaf05.yml
│   ├── spine02.yml
│   └── spine03.yml
└── hosts
```



### Nornir inventory

```shell
netests -z -i inventory/nornir/config.yml
```

```yaml
-z, --nornir-inventory          Specify that an Nornir inventory will be
                                  used.
```



### Netbox inventory

> Not supported yet

```shell
-y, --netbox-inventory          Specify that an Netbox inventory will be
                                  used.
```



## Variables needed

To establish the connexion to the device you have to define many differents variables :

* `hostname:` = device IP addresse or hostname to reach its
* `username:`
* `password:` 
* `connexion:` = Which protocol using to connect to the device
* `port:`
* `secure_api` (depends of connexion type)



### Hostname

List of device type by platform key.

##### Arista Networks

```yaml
platform: eos
```

##### Cumulus Networks

```yaml
platform: linux
```

##### Extreme Networks VSP (VOSS)

```yaml
platform: extreme_vsp
```

##### Cisco IOS / IOS-XE

```yaml
platform: ios
```

##### Cisco IOS-XR

```yaml
platform: iosxr
```

##### Cisco IOS / IOS-XE

```yaml
platform: nxos
```



### Connexion

You have to define in your inventory how Netests.io will connect to devices. 
There are actually 3 possibilities: 

* REST API

  ```yaml
  connexion: api
  secure_api: true # => https://
  secure_api: false # => http://
  ```

* NETCONF

  ```yaml
  connexion: netconf
  ```

* SSH

  ```yaml
  connexion: ssh
  ```



## Examples

Here some examples with an Ansible inventory about how structure it.

#### For each hosts

* Juniper Networks / `leaf04 ` => `host_vars/leaf01.yml`

```yaml
hostname: 172.16.194.52
platform: junos
username: juiper
password: MyJuniper
connexion: netconf
port: 830
```

* Cisco NX-OS/ `leaf02 `=> `host_vars/leaf02.yml`

```yaml
hostname: 172.16.194.53
platform: nxos
username: admin
password: Cisco12345.
connexion: api
port: 443
secure_api: true
```

* Cumulus Networks / `leaf01` / => `host_vars/leaf01.yml`

```yaml
hostname: 172.16.194.51
platform: linux
username: cumulus
password: CumulusLinux!
connexion: ssh
port: 22
```

> Vault integration (Hashicorp & Ansible-vault) is coming.



#### With common variables

Same password for all devices => `group_vars/all.yml`

```yaml
username: cumulus
password: CumulusLinux!
```

Same connexion type for all leaves (leaf) => `group_vars/leaf.yml`

```yaml
platform: linux
connexion: api
port: 8080
secure_api: false
```



## Check connectivity

Before to run the script, Netests.io can test if all devices are reachable.

Netests.io will create a TCP socket to the device. **Credentials are not tested - only TCP connexion is tested**

To tests devices reachability use `--check-connectivity`

```shell
⚡ netests -x -i hosts -a netests.yml  --check-connectivity
```

### Not reachable

```shell
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
	 Welcome to Netests.io
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
{   'leaf05': {   'connexion': 'netconf',
                  'hostname': 'ios-xe-mgmt-latest.cisco.com',
                  'platform': 'ios',
                  'port': 10001}}
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
{   'bgp': False,
    'bgp_up': False,
    'cdp': False,
    'facts': False,
    'lldp': True,
    'ospf': True,
    'ping': False,
    'vrf': False}
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
Device leaf05 is not reachable with the following infos:
	hostname=leaf05
	port=10001
	connexion=netconf

```

### Reachable

```Shell
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
	 Welcome to Netests.io
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
{   'leaf05': {   'connexion': 'netconf',
                  'hostname': 'ios-xe-mgmt-latest.cisco.com',
                  'platform': 'ios',
                  'port': 10000}}
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
{   'bgp': False,
    'bgp_up': False,
    'cdp': False,
    'facts': False,
    'lldp': True,
    'ospf': True,
    'ping': False,
    'vrf': False}
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
All devices are reachable :) !
```

> Port has changed.

