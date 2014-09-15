FROM centerdevice/ubuntu-14.04

#ENV JDK_URL http://download.oracle.com/otn-pub/java/jdk/7u67-b01/jdk-7u67-linux-x64.tar.gz
ENV JDK_URL http://download.oracle.com/otn-pub/java/jdk/8u20-b26/jdk-8u20-linux-x64.tar.gz

ENV JVM_HOME /usr/lib/jvm
ENV JDK_HOME $JVM_HOME/oracle-jdk-amd64
ENV JAVA_HOME $JVM_HOME/default-java

RUN mkdir -p $JDK_HOME
RUN ln -s $JDK_HOME $JAVA_HOME

RUN curl -H "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" \
         -L $JDK_URL \
         -o /tmp/jdk.tar.gz && \
    tar xzf /tmp/jdk.tar.gz -C $JDK_HOME --strip 1 && \
    rm /tmp/jdk.tar.gz

RUN update-alternatives --install /usr/bin/java java $JAVA_HOME/bin/java 1
RUN update-alternatives --install /usr/bin/javac javac $JAVA_HOME/bin/javac 1
RUN update-alternatives --install /usr/bin/javaws javaws $JAVA_HOME/bin/javaws 1
RUN update-alternatives --install /usr/bin/jar jar $JAVA_HOME/bin/jar 1
RUN update-alternatives --set java $JAVA_HOME/bin/java
RUN update-alternatives --set javac $JAVA_HOME/bin/javac
RUN update-alternatives --set javaws $JAVA_HOME/bin/javaws
RUN update-alternatives --set jar $JAVA_HOME/bin/jar

RUN echo "export JAVA_HOME=$JAVA_HOME" >> /etc/profile.d/jdk.sh
