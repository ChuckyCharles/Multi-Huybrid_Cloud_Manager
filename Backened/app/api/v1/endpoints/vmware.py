from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from app.core.vmware import VMwareClient
from app.schemas.vmware import VMwareVirtualMachine, VMwareDatastore, VMwareNetwork

router = APIRouter()

def get_vmware_client() -> VMwareClient:
    return VMwareClient()

@router.get("/virtual-machines", response_model=List[VMwareVirtualMachine])
async def get_vmware_virtual_machines(
    vmware_client: VMwareClient = Depends(get_vmware_client)
):
    """Get all VMware virtual machines"""
    vms = await vmware_client.get_virtual_machines()
    if not vms:
        raise HTTPException(status_code=500, detail="Could not retrieve VMware virtual machines.")
    return vms

@router.get("/datastores", response_model=List[VMwareDatastore])
async def get_vmware_datastores(
    vmware_client: VMwareClient = Depends(get_vmware_client)
):
    """Get all VMware datastores"""
    datastores = await vmware_client.get_datastores()
    if not datastores:
        raise HTTPException(status_code=500, detail="Could not retrieve VMware datastores.")
    return datastores

@router.get("/networks", response_model=List[VMwareNetwork])
async def get_vmware_networks(
    vmware_client: VMwareClient = Depends(get_vmware_client)
):
    """Get all VMware networks"""
    networks = await vmware_client.get_networks()
    if not networks:
        raise HTTPException(status_code=500, detail="Could not retrieve VMware networks.")
    return networks 