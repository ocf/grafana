FROM grafana/grafana:latest

COPY grafana.ini /etc/grafana
COPY provisioning /etc/grafana/provisioning
COPY dashboards /etc/grafana/dashboards

RUN /bin/bash
