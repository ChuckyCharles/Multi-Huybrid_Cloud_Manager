from typing import List, Dict, Any
import asyncio
import datetime

class TemplateClient:
    def __init__(self):
        pass

    async def get_cloud_templates(self) -> List[Dict]:
        await asyncio.sleep(0.1)
        return [
            {
                "id": "cloud-tmpl-001",
                "name": "Web Server on AWS EC2",
                "platform": "AWS",
                "description": "Template for deploying a basic web server on AWS EC2.",
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            },
            {
                "id": "cloud-tmpl-002",
                "name": "Database on Azure SQL",
                "platform": "Azure",
                "description": "Template for deploying an Azure SQL Database.",
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
        ]

    async def get_kubernetes_templates(self) -> List[Dict]:
        await asyncio.sleep(0.1)
        return [
            {
                "id": "k8s-tmpl-001",
                "name": "Nginx Deployment",
                "k8s_version": "1.25",
                "description": "Kubernetes YAML for a basic Nginx deployment and service.",
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            },
            {
                "id": "k8s-tmpl-002",
                "name": "Redis StatefulSet",
                "k8s_version": "1.26",
                "description": "Kubernetes StatefulSet for a Redis instance.",
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
        ]

    async def get_custom_templates(self) -> List[Dict]:
        await asyncio.sleep(0.1)
        return [
            {
                "id": "custom-tmpl-001",
                "name": "Ansible Web Server Playbook",
                "template_type": "Ansible Playbook",
                "description": "Ansible playbook to configure a web server on Linux.",
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            },
            {
                "id": "custom-tmpl-002",
                "name": "Terraform EC2 Instance",
                "template_type": "Terraform",
                "description": "Terraform module for deploying an EC2 instance.",
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
        ] 