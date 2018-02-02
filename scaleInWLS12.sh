. /oracle/setEnvironment.sh> /dev/null 2>&1

echo "Scaling In the WebLogic cluster "
   echo "Calling script to stop and remove Managed Server from cluster."
   java -Djava.security.egd=file:/dev/./urandom weblogic.WLST $SCRIPT_PATH/stopWLS12c_managed.py
   echo "Deleting NodeManager leftover lock files..."
   rm -rf DomainPath+DomainName+'/nodemanager/*.lck'

