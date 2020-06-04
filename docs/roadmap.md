If there is some interested about Netests.io, the team had already defined some new feature that will come in the next release.

Here a list of the new features that will be integrated

### Filter 

Actually the print and the compare function are static. The values that will be compared have been defined by Netests.io Team. In the next release you will be able to define which parameters will be compared and printed.

#### Compare

Define the `compare` function directly in the Netests.io configuration file `netests.yml`

```yaml
config:
  protocols:
    bgp:
      src_hostname: false
      peer_ip: true
      peer_hostname: false
      remote_as: true
      state_brief: true
      session_state: true
      state_time: false
      prefix_received: true
```

#### Print

Define the `print` function directly in the Netests.io configuration file `netests.yml`

```yaml
config:
  protocols:
    bgp:
      src_hostname: false
      peer_ip: true
      peer_hostname: false
      remote_as: true
      state_brief: true
      session_state: true
      state_time: false
      prefix_received: true
```



### Netests-API

An API to execute test with an API call is in developement.

This api will allow you to execute :

* compare function
* Get data formated
* Execute ping from devices



### Ansible Module

We plan to develop an Ansible playbook to execute tests directly from your Ansible playbook

```yaml
- name: Netests.io Ansible module
  netests:
    truth_vars: ./truth_vars/
    protocols:
      bgp: true
      cdp: false
      facts: yes
      lldp: yes
      ospf: false
      vrf: true
```



### Protocols

Improve protocols already implemented :

- OSPF & BGP principaly

We plan to add new protocols like

* ISIS
* LDP
* MTU
* MLAG
* LACP
* etc.

We would like to offer more parameters from BGP like "AFI" & "SAFI".

> You can add your suggestion by liking some issue.
>
> Protocols with the most of "like" will be developed



### Vendors

Some others vendors will be added in the future

> You can add your suggestion by liking some issue.
>
> Vendors with the most of "like" will be developed



### Netbox

Netbox will be usable by Netests.io

##### Inventory

Inventory will be retrived directly from Netbox. 

##### Source of Truth

Netests.io will directly retrieve variables from Netbox to be the source of truth.



### Vault

Currently, Netests.io doesn't support Ansible-Vault and Vault Hashicorp. This meens that the password has to be store in plain text. In the next release we want to fix this security issue

##### Ansible-Vault

Use a system like Ansible-Vault to store, encrypt and decrypt password

##### HashiCorp Vault

Get password directly from Vault HashiCorp.