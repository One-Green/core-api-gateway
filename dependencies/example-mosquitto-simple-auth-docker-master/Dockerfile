FROM eclipse-mosquitto:1.6.2

COPY docker-entrypoint.sh /
COPY config/mosquitto.conf /mosquitto/config/mosquitto.conf

ENTRYPOINT ["sh", "./docker-entrypoint.sh"]

CMD ["/usr/sbin/mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]
