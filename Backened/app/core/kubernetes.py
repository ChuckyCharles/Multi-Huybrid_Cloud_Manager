from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import List, Dict, Any, Optional
import datetime

class KubernetesClient:
    def __init__(self):
        try:
            config.load_kube_config()
            self.v1 = client.CoreV1Api()
            self.apps_v1 = client.AppsV1Api()
        except config.config_exception.ConfigException:
            print("Could not load kube config. Make sure Kubernetes is running and configured locally.")
            # Handle the case where kube config is not found (e.g., for testing or remote deployment)
            self.v1 = None
            self.apps_v1 = None

    async def get_nodes(self) -> List[Dict]:
        if not self.v1:
            return []
        try:
            nodes = self.v1.list_node().items
            formatted_nodes = []
            for node in nodes:
                status = "Unknown"
                for condition in node.status.conditions:
                    if condition.type == "Ready":
                        status = "Ready" if condition.status == "True" else "NotReady"
                        break
                
                roles = [label.split("/")[1] for label in node.metadata.labels if "node-role.kubernetes.io" in label]

                internal_ip = None
                external_ip = None
                if node.status.addresses:
                    for address in node.status.addresses:
                        if address.type == "InternalIP":
                            internal_ip = address.address
                        elif address.type == "ExternalIP":
                            external_ip = address.address

                formatted_nodes.append({
                    "name": node.metadata.name,
                    "status": status,
                    "roles": roles,
                    "kubernetes_version": node.status.node_info.kubelet_version,
                    "os_image": node.status.node_info.os_image,
                    "container_runtime_version": node.status.node_info.container_runtime_version,
                    "kernel_version": node.status.node_info.kernel_version,
                    "internal_ip": internal_ip,
                    "external_ip": external_ip,
                    "creation_timestamp": node.metadata.creation_timestamp.isoformat() if node.metadata.creation_timestamp else None
                })
            return formatted_nodes
        except ApiException as e:
            print(f"Error getting Kubernetes nodes: {e}")
            return []

    async def get_deployments(self) -> List[Dict]:
        if not self.apps_v1:
            return []
        try:
            deployments = self.apps_v1.list_deployment_for_all_namespaces().items
            formatted_deployments = []
            for deployment in deployments:
                formatted_deployments.append({
                    "name": deployment.metadata.name,
                    "namespace": deployment.metadata.namespace,
                    "replicas": deployment.spec.replicas if deployment.spec.replicas is not None else 0,
                    "available_replicas": deployment.status.available_replicas if deployment.status.available_replicas is not None else 0,
                    "updated_replicas": deployment.status.updated_replicas if deployment.status.updated_replicas is not None else 0,
                    "ready_replicas": deployment.status.ready_replicas if deployment.status.ready_replicas is not None else 0,
                    "creation_timestamp": deployment.metadata.creation_timestamp.isoformat() if deployment.metadata.creation_timestamp else None,
                    "strategy": deployment.spec.strategy.to_dict() if deployment.spec.strategy else None,
                    "labels": deployment.metadata.labels
                })
            return formatted_deployments
        except ApiException as e:
            print(f"Error getting Kubernetes deployments: {e}")
            return []

    async def get_pods(self) -> List[Dict]:
        if not self.v1:
            return []
        try:
            pods = self.v1.list_pod_for_all_namespaces().items
            formatted_pods = []
            for pod in pods:
                formatted_pods.append({
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "status": pod.status.phase,
                    "node_name": pod.spec.node_name,
                    "pod_ip": pod.status.pod_ip,
                    "host_ip": pod.status.host_ip,
                    "creation_timestamp": pod.metadata.creation_timestamp.isoformat() if pod.metadata.creation_timestamp else None,
                    "containers": [c.to_dict() for c in pod.spec.containers] if pod.spec.containers else [],
                    "labels": pod.metadata.labels
                })
            return formatted_pods
        except ApiException as e:
            print(f"Error getting Kubernetes pods: {e}")
            return []

    async def get_services(self) -> List[Dict]:
        if not self.v1:
            return []
        try:
            services = self.v1.list_service_for_all_namespaces().items
            formatted_services = []
            for service in services:
                formatted_services.append({
                    "name": service.metadata.name,
                    "namespace": service.metadata.namespace,
                    "type": service.spec.type,
                    "cluster_ip": service.spec.cluster_ip,
                    "external_ips": service.spec.external_i_ps if service.spec.external_i_ps else [],
                    "ports": [p.to_dict() for p in service.spec.ports] if service.spec.ports else [],
                    "creation_timestamp": service.metadata.creation_timestamp.isoformat() if service.metadata.creation_timestamp else None,
                    "selector": service.spec.selector if service.spec.selector else None
                })
            return formatted_services
        except ApiException as e:
            print(f"Error getting Kubernetes services: {e}")
            return [] 