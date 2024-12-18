docker run --rm docker.elastic.co/beats/filebeat:8.17.0 \
    setup -E setup.kibana.host=127.0.0.1:5601 \
          -E output.elasticsearch.hosts=["127.0.0.1:9200"]