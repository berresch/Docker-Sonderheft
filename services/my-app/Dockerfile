FROM centerdevice/jdk

RUN curl -LO http://dl.bintray.com/vertx/downloads/vert.x-2.1.2.tar.gz && \
    tar -zxf vert.x-2.1.2.tar.gz && \
    rm -f vert.x-2.1.2.tar.gz

ADD server.js /server.js
ADD index.html /index.html

ENTRYPOINT /vert.x-2.1.2/bin/vertx run server.js
