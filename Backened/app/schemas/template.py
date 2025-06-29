from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import datetime

class CloudTemplate(BaseModel):
    id: str
    name: str
    platform: str  # e.g., AWS, Azure, GCP
    description: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]

class KubernetesTemplate(BaseModel):
    id: str
    name: str
    k8s_version: str
    description: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]

class CustomTemplate(BaseModel):
    id: str
    name: str
    template_type: str  # e.g., Ansible Playbook, CloudFormation, Terraform
    description: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]

class InfrastructureTemplatesDiscovery(BaseModel):
    cloud_templates: List[CloudTemplate]
    kubernetes_templates: List[KubernetesTemplate]
    custom_templates: List[CustomTemplate] 