import socket
import ast
import datetime

def fullLog(t):
    print('['+str(datetime.datetime.now())+']: '+t)

def getNodeList():
  with open('node_list', 'r') as f:
    d = f.readline()
    node_list = ast.literal_eval(d)['nodes']
  return node_list

def validateEstablishedNodeCandidate(fqdn, ns01, ns02):
    try:
        socket.inet_aton(ns01)
        socket.inet_aton(ns02)
    except socket.error:
        fullLog('Could not validate NS IPs for FQDN: '+fqdn)
        return False
    return True

def establishEstablishedNodeCandidate(established_nodes, fqdn, ns01, ns02):
    established_nodes.append([fqdn, ns01, ns02])
    fullLog('Added node '+fqdn+' with IPs: ['+ns01+', '+ns02+'] to established_nodes')
    return established_nodes

def run():
    mandatory_NS_count = 2
    node_list = getNodeList()
    established_nodes = []

    for node in node_list:
        NS_assigned_to_fqdn = socket.getaddrinfo(node, 0, 0, 0, 0)
        count_NS_assignments = len(NS_assigned_to_fqdn)
        fullLog('Counted '+str(count_NS_assignments)+' nameservers for FQDN: '+node)

        if count_NS_assignments == mandatory_NS_count:
            fullLog('Mandatory of '+str(mandatory_NS_count)+' nameservers for FQDN ['+node+'] has been met. Validating and establishing IPs.')
            if validateEstablishedNodeCandidate(node, NS_assigned_to_fqdn[0][-1][0], NS_assigned_to_fqdn[1][-1][0]):
                established_nodes = establishEstablishedNodeCandidate(established_nodes, node, NS_assigned_to_fqdn[0][-1][0], NS_assigned_to_fqdn[1][-1][0])
        else:
            fullLog('Mandatory of '+str(mandatory_NS_count)+' nameservers requirement has not been met. Amount of nameservers for ['+node+']: '+str(count_NS_assignments))

run()