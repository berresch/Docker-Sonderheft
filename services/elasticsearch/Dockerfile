FROM centerdevice/jdk

#ENV ES_URL https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.3.1.deb
ENV ES_URL https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.3.2.deb

RUN curl -L $ES_URL \
         -o /tmp/elasticsearch.deb && \
         dpkg -i /tmp/elasticsearch.deb && \
         rm /tmp/elasticsearch.deb

WORKDIR /usr/share/elasticsearch
ENTRYPOINT ["bin/elasticsearch"]
