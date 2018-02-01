import os
import sys
import socket


WL_HOME=os.environ['WL_HOME']
SCRIPT_PATH=os.environ['SCRIPT_PATH']
loadProperties(SCRIPT_PATH+'/NewDomain.properties');
hostname = socket.gethostname()

def createBootPropertiesFile(directoryPath, fileName, username, password):
 serverDir = File(directoryPath)
 bool = serverDir.mkdirs()
 fileNew=open(directoryPath + '/'+fileName, 'w')
 fileNew.write('username=%s\n' % username)
 fileNew.write('password=%s\n' % password)
 fileNew.flush()
 fileNew.close()

readTemplate(WL_HOME+'/common/templates/wls/wls.jar')
print "Set the domain administrator user and password"

cd('/')
cd('Security/base_domain/User/weblogic')
set('Name',AdminUser)
cmo.setPassword(AdminServerPassword)

cd('/')
cd('Servers/AdminServer')
print ""
print "Setting the domain properties as per the properties file"
print ""

print "Setting the Administration Server Name to: "+AdminServerName
set('Name',AdminServerName)
print "Setting the Listen Address to 0.0.0.0 and Port to: "+AdminServerPort
set('ListenAddress','')
set('ListenPort',int(AdminServerPort))
#set('Machine',hostname)

print "Write the domain, close the template and exit"

print "Creating domain "+DomainName+ " under path "+DomainPath
writeDomain(DomainPath+"/"+DomainName)
closeTemplate()

print "Creating boot.properties file..."
createBootPropertiesFile(DomainPath+"/servers/"+AdminServerName+"/security", "boot.properties", AdminUser, AdminServerPassword)

#Reading domain in Offline mode
readDomain(DomainPath+"/"+DomainName)

print "Setting the NodeManager properties..."
cd('/')
cd('NMProperties')
set('ListenAddress','')
set('LogToStderr','false')
set('LogLevel','SEVERE')
set('SecureListener',false)

print "Creating Server Template named: "+ ServerTemplate
cd('/')
create(ServerTemplate,'ServerTemplate')
cd('ServerTemplate/'+ServerTemplate)
#set('Machine',hostname)
set('ListenAddress','')
set('ListenPort',int(FirstServerPort))

print "Creating a Dynamic cluster named: "+ DynamicClusterName
cd('/')
create(DynamicClusterName,'Cluster')
cd('Cluster/'+DynamicClusterName)
create(DynamicClusterName,'DynamicServers')
cd('DynamicServers/'+DynamicClusterName)
set('ServerTemplate',ServerTemplate)
set('ServerNamePrefix',ManagedServerPrefix)
set('CalculatedMachineNames',true)
set('CalculatedListenPorts',false)
set('MachineNameMatchExpression','*')
#cmo.setClusterMessagingMode('unicast')

print "Attaching ServerTemplate to new Dynamic Cluster..."
cd('/')
cd('ServerTemplates/'+ServerTemplate)
set('Cluster',DynamicClusterName)

updateDomain()
closeDomain()

exit()

