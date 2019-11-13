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


## Error / Miss

This chapter contains informations about what is missing in protocols implementation and need to be implemented or improved.

#### Static routes

It's not possible to have multiple identic static routes with different next-hop.

```shell
ip route 10.100.0.0 255.255.0.0 10.0.0.100 
ip route 10.100.0.0 255.255.0.0 10.0.0.101
```

To change => Change next-hop type (list) in ``static.py`` class.

Current implementation :
```Python
static_obj = Static(
    vrf_name=vrf_name,
    prefix=str(prefix)[:index_slash],
    netmask=str(prefix)[index_slash + 1:],
    nexthop=facts.get('vias')[0].get('nexthopAddr', NOT_SET),
    is_in_fib=facts.get('kernelProgrammed'),
    out_interface=facts.get('vias')[0].get('interface', NOT_SET),
    preference=facts.get('preference'),
    metric=facts.get('metric')
 )
``` 
