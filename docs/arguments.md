```shell
⚡ netests --help
Usage: netests [OPTIONS]

Options:
  -a, --netest-config-file TEXT   Path to Netests configuration file
                                  [default: netests.yml]

  -b, --inventory-config-file TEXT
                                  Specify path to a Nonrnir configuration
                                  file.  [default: False]

  -c, --check-connectivity        Check if devices are reachable
  -d, --devices TEXT              Filter devices based on the hostname.Several
                                  hostname can be given separate by a ","
                                  [default: #]

  -e, --devices-number INTEGER    Define how many devices will be selected
                                  from the inventory.Can be combined with
                                  --device-group  [default: -1]

  -g, --devices-group TEXT        Filter devices based on the group.Allow you
                                  to select device only from a group.Several
                                  groups can be given separate by a ","
                                  [default: #]

  -i, --inventory TEXT            Path to Ansible inventory or Nornir
                                  hosts.yml  [default: inventory.yml]

  -j, --nornir-groups-file TEXT   Path to Nornir groups.yml  [default:
                                  groups.yml]

  -k, --nornir-defaults-file TEXT
                                  Path to Nornir defaults.yml  [default:
                                  defaults.yml]

  -l, --netbox-url TEXT           Netbox URL  [default: https://127.0.0.1]
  -m, --netbox-token TEXT         Netbox Token  [default:
                                  abcdefghijklmnopqrstuvwxyz0123456789]

  -n, --netbox-ssl TEXT           Verify the Netbox certificate  [default:
                                  True]

  -r, --reports                   If set a configuration reports will be
                                  create

  -t, --terminal                  Start the terminal Netests application
  -v, --verbose TEXT              Filter devices based on the hostname.Several
                                  hostname can be given separate by a ","
                                  [default: level0]

  -w, --num-workers INTEGER       Define the number of parallel jobs.
                                  [default: 100]

  -x, --ansible-inventory         Specify that an Ansible inventory will be
                                  used.

  -y, --netbox-inventory          Specify that an Netbox inventory will be
                                  used.

  -z, --nornir-inventory          Specify that an Nornir inventory will be
                                  used.

  -C, --compare TEXT              To compare/excute step. Will only get data
                                  or generate cmd.

  -D, --show-data-model TEXT      Show data models for a protocol. Can help
                                  you to create your SOT.

  -I, --init-data                 To create truth_vars files.
  -J, --init-folders              To create truth_vars/ folders.
  -K, --init-config-file          To create netests.yml (Netests.io
                                  configuration file).

  -V, --show-truth-vars TEXT      Show vars retrieved for a specific host. Use
                                  * to select all hosts

  --help                          Show this message and exit.
```

> Note: Some of these arguments are not totally implemented yet.