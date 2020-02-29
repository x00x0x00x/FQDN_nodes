import socket
import ast
import datetime
from threading import Thread
from ws import initiate_server

def fullLog(t):
    print('['+str(datetime.datetime.now())+']: '+t)

def getNodeList():
  with open('node_list', 'r') as f:
    d = f.readline()
    node_list = ast.literal_eval(d)['nodes']
  return node_list

def getConfig():
    with open('config','r') as f:
        d = f.readline()
        config = ast.literal_eval(d)['config']
    return config

def validateEstablishedNodeCandidate(fqdn, ns01, ns02):
    if fqdn[:4] != 'www.':
        fullLog('FQDN does not start with www. Skipping node: ' + fqdn)
        return False

    if len(fqdn.split('.')) > 2:
        fullLog('FQDN contains more than two dots. Skipping node: ' + fqdn)
        return False

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

    config = getConfig()
    established_nodes = []
    try:
        if config['node_type'] == 'main_node':
            established_nodes = [[config['self_FQDN'], '0.0.0.0', config['comp_node']]]
        elif config['node_type'] == 'comp_node':
            established_nodes = [[config['self_FQDN'], config['main_node'], '0.0.0.0']]
    except:
        fullLog('\n\nCould not add own node to establish_nodes. Please check your config file.')
        exit()

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