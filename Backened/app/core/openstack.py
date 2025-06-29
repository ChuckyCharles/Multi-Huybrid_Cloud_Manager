from typing import List, Dict, Any
import asyncio
import datetime

class OpenStackClient:
    def __init__(self):
        # In a real scenario, this would initialize connection to OpenStack API
        pass

    async def get_instances(self) -> List[Dict]:
        # Simulate fetching data from OpenStack Nova
        await asyncio.sleep(0.1) # Simulate network delay
        return [
            {
                "id": "inst-001",
                "name": "openstack-web-server",
                "status": "ACTIVE",
                "image_name": "Ubuntu 22.04 LTS",
                "flavor_name": "m1.small",
                "power_state": "Running",
                "task_state": None,
                "vm_state": "active",
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            },
            {
                "id": "inst-002",
                "name": "openstack-db-server",
                "status": "ACTIVE",
                "image_name": "CentOS 8",
                "flavor_name": "m1.medium",
                "power_state": "Running",
                "task_state": None,
                "vm_state": "active",
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            },
            {
                "id": "inst-003",
                "name": "openstack-build-agent",
                "status": "SHUTOFF",
                "image_name": "Fedora 37",
                "flavor_name": "m1.tiny",
                "power_state": "Shut off",
                "task_state": None,
                "vm_state": "stopped",
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
        ]

    async def get_volumes(self) -> List[Dict]:
        # Simulate fetching data from OpenStack Cinder
        await asyncio.sleep(0.1) # Simulate network delay
        return [
            {
                "id": "vol-001",
                "name": "data-volume-prod",
                "status": "in-use",
                "size_gb": 100,
                "attachments": [{"server_id": "inst-001", "device": "/dev/sdb"}],
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            },
            {
                "id": "vol-002",
                "name": "backup-volume",
                "status": "available",
                "size_gb": 500,
                "attachments": [],
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
        ]

    async def get_networks(self) -> List[Dict]:
        # Simulate fetching data from OpenStack Neutron
        await asyncio.sleep(0.1) # Simulate network delay
        return [
            {
                "id": "net-001",
                "name": "private-network",
                "status": "ACTIVE",
                "subnets": ["192.168.1.0/24"],
                "shared": False,
                "router_external": False,
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            },
            {
                "id": "net-002",
                "name": "public-network",
                "status": "ACTIVE",
                "subnets": ["10.0.0.0/24"],
                "shared": True,
                "router_external": True,
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
        ] 