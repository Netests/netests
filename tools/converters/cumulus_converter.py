def _cumulus_bgp_converter(nornirObj):

    for host in nornirObj.inventory.hosts:
        resultBGP = dict()

        if BGP_KEY_FOR_NORNIR_HOSTS in nornirObj.inventory.hosts[host].keys():
            data = json.loads(
                nornirObj.inventory.hosts[host][BGP_KEY_FOR_NORNIR_HOSTS])
        else:
            raise Exception(
                "[_cumulus_bgp_summary_converter] - error with BGP key => check inventory hosts file")

        if "ipv4 unicast" in data.keys():
            if data['ipv4 unicast'] is None:
                resultBGP[host] = dict()
            else:
                resultBGP[host] = dict()
                resultBGP[host][BGP_KEY_FOR_ASN] = data['ipv4 unicast']['as']
                resultBGP[host]['routerId'] = data['ipv4 unicast']['routerId']
                resultBGP[host]['bestPath'] = "multiPathRelax " + \
                    data['ipv4 unicast']['bestPath']['multiPathRelax']

                resultBGP[host]['vrfName'] = data['ipv4 unicast']['vrfName']
                resultBGP[host][BGP_KEY_FOR_TOTAL_PEERS] = data['ipv4 unicast']['totalPeers']
                resultBGP[host]['interfaces'] = dict()
                for port, facts in data['ipv4 unicast']['peers'].items():
                    resultBGP[host]['interfaces'][port] = dict()
                    if 'hostname' in facts.keys():
                        resultBGP[host]['interfaces'][port]['bgp_neighbor'] = facts['hostname']
                    else:
                        resultBGP[host]['interfaces'][port]['bgp_neighbor'] = "None"
                    resultBGP[host]['interfaces'][port]['peerUptime'] = facts['peerUptime']
                    resultBGP[host]['interfaces'][port]['state'] = facts['state']

        nornirObj.inventory.hosts[host][BGP_KEY_FOR_NORNIR_HOSTS_BRIEF] = resultBGP[host]
