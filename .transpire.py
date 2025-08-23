from pathlib import Path

from transpire.resources import ConfigMap, Deployment, Ingress, Service, Secret
from transpire.types import Image
from transpire.utils import get_image_tag

name = "grafana"

# Create K8S objects for Grafana
def objects():
    yield Ingress(
        host="grafana.ocf.berkeley.edu",
        service_name="grafana-web",
        service_port=80,
    ).build()

    yield Secret(
        name="grafana",
        string_data={
            "PROMETHEUS_AUTH_PASSWORD": "",
            "GF_DATABASE_PASSWORD": "",
            "GF_SECURITY_ADMIN_PASSWORD": "",
            "GF_SESSION_PROVIDER_CONFIG": "",
            "GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET": "",
        }
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
            "PROMETHEUS_AUTH_USER": "ocfadmin",
        }
    ).build()
 

    deployment = Deployment(
        name="grafana",
        image=get_image_tag("grafana"),
        ports=[3000],
    )
    # We inject ConfigMap and secrets to deployment env with
    # pod_spec().with_configmap_env() and pod_spec().with_secret_env()
    deployment.pod_spec().with_configmap_env("grafana").with_secret_env("grafana")
    yield deployment.build()
    
   
    yield Service(
        name="grafana-web",
        selector=deployment.get_selector(),
        # Transpire: Port
        port_on_svc=80,
        # Transpire: Target Port
        port_on_pod=3000
    ).build()


# Add grafana image to ghcr
def images():
    yield Image(name="grafana", path=Path("/"), registry="ghcr")
