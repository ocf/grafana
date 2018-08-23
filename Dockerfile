FROM grafana/grafana:latest

COPY grafana.ini /etc/grafana
COPY provisioning /etc/grafana/provisioning

RUN /bin/bash
