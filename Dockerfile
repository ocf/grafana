ARG grafana_version=latest
FROM grafana/grafana:${grafana_version}

COPY grafana.ini /etc/grafana
COPY ldap.toml /etc/grafana
COPY provisioning /etc/grafana/provisioning

RUN /bin/bash
