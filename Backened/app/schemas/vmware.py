from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class VMwareVirtualMachine(BaseModel):
    name: str
    status: str
    cpu: int
    memory_gb: int
    guest_os: str
    ip_address: Optional[str]
    power_state: str

class VMwareDatastore(BaseModel):
    name: str
    capacity_gb: float
    free_space_gb: float
    type: str

class VMwareNetwork(BaseModel):
    name: str
    type: str
    vlan_id: Optional[int]

class VMwareResourceDiscovery(BaseModel):
    virtual_machines: List[VMwareVirtualMachine]
    datastores: List[VMwareDatastore]
    networks: List[VMwareNetwork] 