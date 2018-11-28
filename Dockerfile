FROM oraclelinux:6.6

MAINTAINER Radu Dobrinescu - <radu.dobrinescu@oraclemiddlewareblog.com>

RUN groupadd oinstall -g 501 && \
 useradd -m        -u 501 -g oinstall -d /home/oracle oracle && \
    mkdir -p /oracle/ && \
    mkdir -p /oracle/fmwhome/wlst_custom/ && \
    chown -R oracle:oinstall /oracle/ && \
    chown -R oracle:oinstall /oracle/fmwhome && \
    chown -R oracle:oinstall /home/oracle && \
    chown -R oracle:oinstall /oracle/fmwhome/wlst_custom

ENV SCRIPT_PATH /oracle/fmwhome/wlst_custom/

ADD jdk-8u192-linux-x64.tar.gz /oracle/fmwhome/

COPY oraInst.loc setEnvironment.sh responseFile /oracle/
COPY startWLS12c.sh scaleInWLS12.sh NewDomain.properties *.py $SCRIPT_PATH

RUN chown oracle:oinstall /oracle/oraInst.loc && \
    chown -R oracle:oinstall $SCRIPT_PATH && \
    chmod +x $SCRIPT_PATH/startWLS12c.sh
    
USER oracle

ENV JAVA_HOME=/oracle/fmwhome/jdk1.8.0_192/ PATH=$PATH:/oracle/fmwhome/jdk1.8.0_192/bin MW_HOME=/oracle/fmwhome/wls12c/ SCRIPT_PATH=/oracle/fmwhome/wlst_custom/
ENV CONFIG_JVM_ARGS -Djava.security.egd=file:/dev/./urandom

COPY fmw_12.2.1.3.0_wls.jar /oracle/

RUN java -jar /oracle/fmw_12.2.1.3.0_wls.jar -silent -invPtrLoc /oracle/oraInst.loc -responseFile /oracle/responseFile && \
    . ./oracle/setEnvironment.sh && \
    java -Djava.security.egd=file:/dev/./urandom weblogic.WLST $SCRIPT_PATH/createDomain.py && \
    rm -rf /oracle/fmw_12.1.3.0.0_wls.jar
