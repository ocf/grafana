from pathlib import Path

from transpire.resources import ConfigMap, Deployment, Ingress, Service, Secret
from transpire.types import Image
from transpire.utils import get_image_tag

name = "grafana"

# Add grafana image to ghcr
def images():
    yield Image(name="grafana", path=Path("/"), registry="ghcr")

# Create K8S objects for Grafana
def objects():
    yield Ingress(
        ingress_name="virtual-host-ingress",
        host="grafana.ocf.berkeley.edu",
        service_name="service",
        service_port=80,
    ).build()

    yield Secret(
        name="prometheus-auth",
        string_data={
            "username": "ocfgrafana",
            # <%=prometheus_pass>
            "password": "",
        }
    ).build()

    yield Service(
        name="service",
        selector={
            "app": "grafana",
        },
        # Transpire: Port
        port_on_svc=90,
        # Transpire: Target Port
        port_on_pod=3000
    ).build()

    yield ConfigMap(
        name="grafana",
        data={
            "GF_SERVER_ROOT_URL": "https://grafana.ocf.berkeley.edu/",
            "GF_DATABASE_TYPE": "mysql",
            "GF_DATABASE_HOST": "mysql",
            "GF_DATABASE_NAME": "ocfgrafana",
            "GF_DATABASE_USER": "ocfgrafana",
            "GF_SESSION_PROVIDER": "mysql",
            "GF_SESSION_COOKIE_SECURE": "true",
            "GF_DATABASE_PASSWORD__FILE": "/etc/secrets/mysql-pass",
            "GF_SECURITY_ADMIN_PASSWORD__FILE": "/etc/secrets/admin-pass",
            "GF_SESSION_PROVIDER_CONFIG__FILE": "/etc/secrets/provider-config",
            "GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET__FILE": "/etc/secrets/keycloak-secret",
        }
    ).build()

    # We inject ConfigMap and secrets to deployment env with
    # pod_spec().with_configmap_env() and pod_spec().with_secret_env()
    yield Deployment(
        name="grafana",
        image=get_image_tag("grafana"),
        ports=[3000],
    ).pod_spec().with_configmap_env("grafana").with_secret_env("prometheus-auth").build()

