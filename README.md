The OCF's Grafana deployment.

# Provisioned dashboards
Dashboards should go in the `/dashboards` top level directory. These can be git submodules (such as the [Node Exporter Server Metrics](https://grafana.com/dashboards/405) dashboard). If necessary, replace templated variable names in the submodule-- see https://github.com/grafana/grafana/issues/10786#issuecomment-383931147 for more information.

# Local testing
This Dockerfile can be run locally, so you can iterate quickly without touching our production deployment.
