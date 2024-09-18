from kubernetes import client, config
from kubernetes.client.rest import ApiException
import os

def load_kube_config():
    try:
        config.load_kube_config()
    except config.config_exception.ConfigException:
        # If running in-cluster
        config.load_incluster_config()

def create_deployment(name, image, replicas=1):
    load_kube_config()
    apps_v1 = client.AppsV1Api()
    
    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=name),
        spec=client.V1DeploymentSpec(
            replicas=replicas,
            selector=client.V1LabelSelector(
                match_labels={"app": name}
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(
                    labels={"app": name}
                ),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name=name,
                            image=image
                        )
                    ]
                )
            )
        )
    )
    
    try:
        apps_v1.create_namespaced_deployment(
            namespace="default",
            body=deployment
        )
        return True, f"Deployment {name} created successfully"
    except ApiException as e:
        return False, f"Error creating deployment: {str(e)}"

def list_deployments():
    load_kube_config()
    apps_v1 = client.AppsV1Api()
    
    try:
        deployments = apps_v1.list_namespaced_deployment(namespace="default")
        return True, [dep.metadata.name for dep in deployments.items]
    except ApiException as e:
        return False, f"Error listing deployments: {str(e)}"

def delete_deployment(name):
    load_kube_config()
    apps_v1 = client.AppsV1Api()
    
    try:
        apps_v1.delete_namespaced_deployment(
            name=name,
            namespace="default"
        )
        return True, f"Deployment {name} deleted successfully"
    except ApiException as e:
        return False, f"Error deleting deployment: {str(e)}"
