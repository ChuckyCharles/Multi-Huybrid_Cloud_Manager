from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class KubernetesNode(BaseModel):
    name: str
    status: str
    roles: List[str]
    kubernetes_version: str
    os_image: str
    container_runtime_version: str
    kernel_version: str
    internal_ip: Optional[str]
    external_ip: Optional[str]
    creation_timestamp: Optional[str]

class KubernetesDeployment(BaseModel):
    name: str
    namespace: str
    replicas: int
    available_replicas: Optional[int]
    updated_replicas: Optional[int]
    ready_replicas: Optional[int]
    creation_timestamp: Optional[str]
    strategy: Optional[Dict[str, Any]]
    labels: Optional[Dict[str, str]]

class KubernetesPod(BaseModel):
    name: str
    namespace: str
    status: str
    node_name: Optional[str]
    pod_ip: Optional[str]
    host_ip: Optional[str]
    creation_timestamp: Optional[str]
    containers: List[Dict[str, Any]]
    labels: Optional[Dict[str, str]]

class KubernetesService(BaseModel):
    name: str
    namespace: str
    type: str
    cluster_ip: Optional[str]
    external_ips: Optional[List[str]]
    ports: List[Dict[str, Any]]
    creation_timestamp: Optional[str]
    selector: Optional[Dict[str, str]]

class KubernetesResourceDiscovery(BaseModel):
    nodes: List[KubernetesNode]
    deployments: List[KubernetesDeployment]
    pods: List[KubernetesPod]
    services: List[KubernetesService] 