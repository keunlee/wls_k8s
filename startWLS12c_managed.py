import socket
import os
import time

SCRIPT_PATH=os.environ['SCRIPT_PATH']
loadProperties(SCRIPT_PATH+'/NewDomain.properties');
hostname = socket.gethostname()
admin_url = os.environ["ADMIN_HOSTNAME"]+':'+AdminServerPort
ip_addr = os.popen("/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'").read()

def deleteMachine(hostname):
 edit()
 startEdit(10000,20000,'true')
 cd('/')
 cd('Machines')
 delete(hostname)
 save()
 activate()

def stopManagedServer(server):
  try:
   shutdown(server,'Server',force='true')
  except:
   print "Server has been already shutdown"

def scaleInCluster():
 edit()
 startEdit(10000,20000,'true')
 cd('/')
 cd('Clusters/'+DynamicClusterName+'/DynamicServers/'+DynamicClusterName)
 serverCount = cmo.getMaximumDynamicServerCount()-1
 set('MaximumDynamicServerCount',serverCount)
 print "The number of Dynamic Servers in the cluster has been decreased to: "+str(serverCount)
 save()
 activate()

print "Cleaning up the domain configuration after scaling down the cluster..."
connect(AdminUser,AdminServerPassword,'http://'+admin_url);

svrs = cmo.getServers()
domainRuntime()
for server in svrs:
  if server.getName() != 'AdminServer':
    serverConfig()
    machine = server.getMachine();
    if machine.getName() == hostname:
     print "Name of the server to remove is: "+server.getName()
     state(server.getName(), 'Server')
     stopManagedServer(server.getName())
     state(server.getName(), 'Server')
     print "Removing the server instance from the Dynamic Cluster"
     scaleInCluster()
     print "Deleting the Unix Machine from the Domain configuration"
     deleteMachine(machine.getName())
exit()

