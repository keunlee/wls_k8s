import socket
import os
import time

SCRIPT_PATH=os.environ['SCRIPT_PATH']
loadProperties(SCRIPT_PATH+'/NewDomain.properties');
hostname = socket.gethostname()
admin_url = os.environ["ADMIN_HOSTNAME"]+':'+AdminServerPort
ip_addr = os.popen("/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'").read()

def addMachine():
 edit()
 startEdit(10000,20000,'true')
 cd('/')
 create(hostname,'UnixMachine')
 cd('Machines/'+hostname)
 cd('NodeManager/'+hostname)
 set('ListenAddress',ip_addr)
 set('NMType','Plain')
 save()
 activate()

def changeMachineIP():
 edit()
 startEdit(10000,20000,'true')
 cd('/')
 cd('Machines/'+hostname+'/NodeManager/'+hostname)
 set('ListenAddress',ip_addr)
 save()
 activate()

def createMS():
 edit()
 startEdit(10000,20000,'true')
 cd('/')
 cd('Clusters/'+DynamicClusterName+'/DynamicServers/'+DynamicClusterName)
 serverCount = cmo.getMaximumDynamicServerCount()+1
 set('MaximumDynamicServerCount',serverCount)
 print "The number of Dynamic Servers in the cluster has been increased to: "+str(serverCount)
 save()
 activate()

def startNM():
 #try:
 #  nmConnect(AdminUser,AdminServerPassword,str(ip_addr),5556,DomainName,DomainPath+DomainName,'plain')
 # except:
 #  print "It seems Node Manager is not running. Starting Node Manager..."
   print "Starting the Node Manager on this machine..."
   startNodeManager(NodeManagerHome=DomainPath+DomainName+'/nodemanager',PropertiesFile=DomainPath+DomainName+'/nodemanager/nodemanager.properties',verbose=false)
   print "Waiting 60 seconds for Node Manager to start..."
   Thread.sleep(60000)
   try:
    nmConnect(AdminUser,AdminServerPassword,str(ip_addr),5556,DomainName,DomainPath+DomainName,'plain')
   except:
    print "Unable to connect to Node Manager. Resuming configuration and trying again later..."

print "IP address of this Docker container is "+ip_addr
startNM()
connect(AdminUser,AdminServerPassword,'http://'+admin_url);
nmEnroll(DomainPath+DomainName,DomainPath+DomainName+'/nodemanager');

cd('/')
cd('Machines')
machines = ls()
if (machines.find(hostname) != -1):
    print "Machine with name "+hostname+" already exists in this domain"
    changeMachineIP()
    cd('/')
    cd('Clusters/'+DynamicClusterName+'/DynamicServers/'+DynamicClusterName)
    serverCount = cmo.getMaximumDynamicServerCount()
    print serverCount
    #nmConnect(AdminUser,AdminServerPassword,str(ip_addr),5556,DomainName,DomainPath+DomainName,'plain')
    start(ManagedServerPrefix+str(serverCount),'Server')
else:
    print "Adding a new machine named "+hostname+" to the domain..."
    addMachine()
    print "Adding a new Dynamic Server to the <"+DynamicClusterName+"> cluster"
    createMS()
    cd('/')
    cd('Clusters/'+DynamicClusterName+'/DynamicServers/'+DynamicClusterName)
    serverCount = cmo.getMaximumDynamicServerCount()
    print serverCount
    #nmConnect(AdminUser,AdminServerPassword,str(ip_addr),5556,DomainName,DomainPath+DomainName,'plain')
    start(ManagedServerPrefix+str(serverCount),'Server')
exit();

