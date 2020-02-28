# FQDN_nodes
 
The node starts off with a peer list, which can be manually entered in the node_list file. 
This can be a select few, as peers relay node_lists to eachother automatically.

# Run.py


Run.py currently consists out of:

- getNodeList(): reads the nodes from the node_list file and returns a list of FQDN's
- getConfig(): reads the config from the config file and returns a dict with configurations
- validateEstablishedNodeCandidate(): validates ip addresses for an fqdn
- establishEstablishedNodeCandidate(): establishes an fqdn and its two nameserver ip addresses as established_nodes
- run(): this is the main thread and enforces a mandatory_NS_count of 2


This main thread starts off by reading the FQDN's from the node_list file through the getNodeList() function

It then continues to read the config from the config file through the getConfig() function

It declares established_nodes as an empty list on boot


Depending on the node_type, as configured in the config file, the current ip address of the NS will be omitted and replaced for 0.0.0.0, its purpose is to later filter out such entry in a different process


For each and every node in the node_list, the nameservers assigned to the FQDN will be fetched through the socket.getaddrinfo method
If the length of the NS assignments == mandatory_NS_count (2), the FQDN is validated through the validateEstablishedNodeCandidate function, if valid the FQDN is added to the established_nodes list

# config
```
{'config': {'self_FQDN': 'www.nyzo.net','node_type': 'main_node', 'main_node': '175.0.0.0', 'comp_node': '176.0.0.0'}}
```

# node_list
```
{'nodes':['127.0.0.1', 'www.nyzo.net']}
```
