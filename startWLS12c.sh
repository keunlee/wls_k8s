. /oracle/setEnvironment.sh> /dev/null 2>&1

echo "Starting " ${SERVER_TYPE}

if [[ "${SERVER_TYPE}" == "AdminServer" ]]; then
   echo "Calling script to start the AdminServer."
   nohup java -Djava.security.egd=file:/dev/./urandom weblogic.WLST $SCRIPT_PATH/startWLS12c_admin.py &
   else if [[ "${SERVER_TYPE}" == "ManagedServer" ]]; then
   echo "Calling script to start ManagedServer"
   nohup java -Djava.security.egd=file:/dev/./urandom weblogic.WLST $SCRIPT_PATH/startWLS12c_managed.py &
        else
                echo "SERVER_TYPE needs to be defined to either <AdminServer> or <ManagedServer>"
                exit
        fi
fi

