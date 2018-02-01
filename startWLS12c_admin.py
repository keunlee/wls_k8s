import socket
SCRIPT_PATH=os.environ['SCRIPT_PATH']
loadProperties(SCRIPT_PATH+'/NewDomain.properties');

hostname = socket.gethostname()
print "Starting the WebLogic Administration Server for domain "+DomainName
readDomain(DomainPath+DomainName)
cd('Servers/'+AdminServerName)
set('ListenAddress','')
set('TunnelingEnabled',true)
updateDomain()
closeDomain()

startServer(AdminServerName,DomainName,'http://'+hostname+':'+AdminServerPort,AdminUser,AdminServerPassword,DomainPath+DomainName,jvmArgs=ADM_JAVA_ARGUMENTS);

exit();
