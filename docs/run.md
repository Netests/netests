How run Netests.io ?

This page will explain you all possibilities.



## Define inventory type

Netests.io currently supports two inventory types:

* Ansible
* Nornir

To define that Netests.io has to use an *Ansible* inventory, use `-x` arugment.

```shell
netests -x
```

To define that Netests.io has to use an *Nornir* inventory, use `-z` arugment.

```shell
netests -z
```

> `-y` is reserved for future Netbox integration



## Set path to inventory file

To complet inventory types arguments you can specify path to inventory with `-i`

### Ansible inventory

```shell
netests -x -i inventory/ansible/hosts
```

Ansible inventory file example

```shell
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
```



### Nornir inventory

```shell
netests -z -i inventory/nornir/config.yml
```

Nornir inventory file configuration example

```yaml
---
core:
    num_workers: 10

inventory:
    plugin: nornir.plugins.inventory.simple.SimpleInventory
    options:
        host_file: "inventory/nornir/hosts.yml"
        group_file: "inventory/nornir/groups.yml"
        defaults_file: "inventory/nornir/defaults.yml"
```



## Specify Netests.io configuration file

```shell
netests -x -i inventory/ansible/hosts -a path/to/netests.yml
```



## Define number of forks

Forks define how many tasks will be run in parallel

```shell
netests -x -i inventory/ansible/hosts -a path/to/netests.yml -w 1000
```

> Will run 1000 parallel tasks