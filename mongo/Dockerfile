FROM mongo:latest

RUN  mkdir -p /data/db/mongodb && \
     touch /data/db/mongodb/.keep && \
     chown -R mongodb:mongodb /data/db

ADD mongodb.conf /etc/mongodb.conf

VOLUME [ "/data/db" ]

EXPOSE 27017

USER mongodb
WORKDIR /var/lib/mongodb

ENTRYPOINT ["/usr/bin/mongod", "--config", "/etc/mongodb.conf"]
CMD ["--quiet"]