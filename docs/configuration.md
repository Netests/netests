It is possible to define which protocol will be tested. It's not an obligation to execute some tests on all protocols supported by Netests.io.

To define which test will be executed you have to create a netests configuration file.

By default its name is `netests.yml`



## Configuration file

```yaml
config:
  protocols:
    bgp:
      test: true

    bgp_all_up:
      test: false

    cdp:
      test: false

    facts:
      test: true

    lldp:
      test: false
    
    ospf:
      test: false
      
    ping:
      test: true

    vrf:
      test: true

```

> File can be specified when you are running Netests.io from the CLI
>
> ```shell
> Options:
>   -a, --netest-config-file TEXT   Path to Netests configuration file
>                                   [default: netests.yml]
> ```



### Enable a protocol

Juste put `test: true` for the protocol.

For example to enable `lldp`

```yaml
    lldp:
      test: false
```



### Disable a protocol

Juste put `test: false` for the protocol.

For example to enable `lldp`

```yaml
    lldp:
      test: false
```



### Enable protocol for only one device

Sometime it can be useful to test a protocol only for one device.

Currently it is not possible to filter a protocol by `host` or `group` BUT there is a possibilty to bypass test.

> If there is no source of truth for a specific protocol for a device the test will be true.



#### Example

The goal is to execute LLDP test only on `leaf01` but not on `leaf02`.

1. Enable LLDP for all devices

```yaml
config:
  protocols:
    lldp:
      test: true
```

Create a source of truth only for `leaf01`.

```shell
truth_vars
├── all
│   └── ping.yml
└── hosts
    ├── leaf01
    │   ├── lldp.yml
    │   └── ping.yml
    ├── leaf02
        └── ping.yml

```

Given that `leaf02` has not source of truth for LLDP the result will be **true**.

