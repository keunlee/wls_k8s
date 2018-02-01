Creating a Docker image of a WebLogic Domain that can run and scale automatically on a k8s cluster

## Build the Docker image of a WebLogic domain:

### 1. Download necessary files:
In the same directory you need to download the JDK and WebLogic installation files:

jdk-8u161-linux-x64.tar.gz
--download from http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

unzip fmw_12.2.1.3.0_wls_Disk1_1of1.zip
fmw_12.2.1.3.0_wls.jar
--download from http://www.oracle.com/technetwork/middleware/weblogic/downloads/wls-for-dev-1703574.html

### 2. Configure the domain

Edit the NewDomain.properties to customize your domain. 

