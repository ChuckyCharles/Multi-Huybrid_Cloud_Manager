from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class OpenStackInstance(BaseModel):
    id: str
    name: str
    status: str
    image_name: str
    flavor_name: str
    power_state: str
    task_state: Optional[str]
    vm_state: str
    created_at: Optional[str]

class OpenStackVolume(BaseModel):
    id: str
    name: str
    status: str
    size_gb: int
    attachments: List[Dict[str, Any]]
    created_at: Optional[str]

class OpenStackNetwork(BaseModel):
    id: str
    name: str
    status: str
    subnets: List[str]
    shared: bool
    router_external: bool
    created_at: Optional[str]

class OpenStackResourceDiscovery(BaseModel):
    instances: List[OpenStackInstance]
    volumes: List[OpenStackVolume]
    networks: List[OpenStackNetwork] 