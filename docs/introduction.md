# Documentation

```shell
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
 WELCOME TO NETESTS.IO DOCUMENTATION 
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
```

## Introduction

In our current world, the stability of networks has become something of paramount importance.

There are many solutions to define that your network is working :

* Monitoring - Get metrcis with SNMP, "show" command, Telemetry, etc.
* Logging - Manage and use logs send by devices
* Alarming - Based on metrics and logging raise an alarms if something appears on your network.

And, from a few of year **Testing**.

The goal of testing your network is to be sure that :

* Be sure that all BGP sessions are UP and the session
* Be sure that your wire is correctly connected by checking LLDP neighbors
* Execute some PING to check that some destinations are reachable
* etc.

One of the biggest problem is **How can I test my network ?** :



All these tests have to be executed after each modification to be sure that it not create an issue on your network.

Yet, the problem is **We have to write some code to automate tests ...** But *I'm Network Engineer not a developer*.

That's why **Netests.io** was created ! The idea of **Netests.io** is to offer a way of testing your network without writing some codes !



## Netests features

Netests.io is based on a source of truth. This source is used to define which you exepect on your network.

When Netests.io is run, it will connect to the device, get informations by protocols and compare to your source of truth.

If the two results are the same, Netests will return a success, otherwise a failure.



Netests.io can connect to the device with `Netconf`, `ssh`, over a `rest api` and with `NAPALM` if the vendor is supported by NAPALM.

Not all connexion type are available for all devices. Some vendors don't support Netconf or REST API.

Please before to start have a look on ``vendors_and_protocols``.



## Way of working

The network engineer job is evolving and the ways of working too.

### Current / Past

In a network (without automation) to execute a modification the next steps have to be done :

1. Execute your modification

   ```
   conf t
   router bgp 65321
     neighbors 1.1.1.1 remote as 1
     neighbors 1.1.1.1 description MY_NEW_PEER
   ```

2. Check that the configuration is applied and that the session is UP

   ```
   show ip bgp summary
   ```

3. Try to reach a network on other side to check 2 way

   ```shell
   ping 10.1.1.1
   ```



### With Netests

With network the steps are a bit differents. The verification will not be done directly one the devices.

1.  Execute your modification - Directly on the device (bad :confused:) or in a file and deploy with Ansible, Nornir etc. (good :smiley:).

   * Manually

   ```shell
   conf t
   router bgp 65321
     neighbors 1.1.1.1 remote as 1
     neighbors 1.1.1.1 description MY_NEW_PEER
   ```

   * With a configuration management tool

   ```yaml
   ---
   routing:
     bgp:
       local_as: 65321
       neighbors: 
         -  peer_ip: 1.1.1.1
            remote_as: 1
            description: MY_NEW_PEER
   ```

2. Update your test in Netests

   * Add check to verify that the BGP new session is UP in ``truth_vars/hosts/{{ hostname }}/bgp.yml``

   ```yaml
   default:
     as_number: 65321
     router_id: 172.16.0.1
     neighbors:
     - peer_ip: 1.1.1.1
       remote_as: 65535
       state_brief: UP
   ```

   * Add ping to test reachability in ``truth_vars/hosts/{{ hostname }}/ping.yml``

   ```yaml
   - ip: 17.1.1.1
     vrf: default
     works: true
   ```

3. Run ``Netests.io``

   ```shell
   ⚡ ./netests/welcome.py -x -i inventory/ansible/hosts -a netests.yml
   
   {   'bgp': {
   				Host: leaf02: True
   		},
       'bgp_all_up': {
   				Host: leaf02: True
   		},
       'cdp': None,
       'facts': {
   				Host: leaf02: True
   		},
       'lldp': None,
       'ospf': None,
       'vrf': {
   				Host: leaf02: True
   		},
   }
   ```

   > Protocols with a "None" is the protocols that had not been tested
   >
   > Don't be affraid about them :smiley:

   ```shell
   ⚡ echo $?
   0
   ```

   

### Integrate in a CI/CD pipeline

Based on the software developement good practice some companies try to develop (or already have) a CI/CD pipeline.

On of the important step is to **test** your modification. Netests can be used to do the step.

![devops.png](./images/devops.png)

In your CI/CD pipeline just add a step where you are running **netests**.

```shell
⚡ ./netests/welcome.py -x -i inventory/ansible/hosts -a netests.yml
```

The task will failed if a test will failed.