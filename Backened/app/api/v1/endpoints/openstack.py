from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from app.core.openstack import OpenStackClient
from app.schemas.openstack import OpenStackInstance, OpenStackVolume, OpenStackNetwork

router = APIRouter()

def get_openstack_client() -> OpenStackClient:
    return OpenStackClient()

@router.get("/instances", response_model=List[OpenStackInstance])
async def get_openstack_instances(
    os_client: OpenStackClient = Depends(get_openstack_client)
):
    """Get all OpenStack instances (Nova)"""
    instances = await os_client.get_instances()
    if not instances:
        raise HTTPException(status_code=500, detail="Could not retrieve OpenStack instances.")
    return instances

@router.get("/volumes", response_model=List[OpenStackVolume])
async def get_openstack_volumes(
    os_client: OpenStackClient = Depends(get_openstack_client)
):
    """Get all OpenStack volumes (Cinder)"""
    volumes = await os_client.get_volumes()
    if not volumes:
        raise HTTPException(status_code=500, detail="Could not retrieve OpenStack volumes.")
    return volumes

@router.get("/networks", response_model=List[OpenStackNetwork])
async def get_openstack_networks(
    os_client: OpenStackClient = Depends(get_openstack_client)
):
    """Get all OpenStack networks (Neutron)"""
    networks = await os_client.get_networks()
    if not networks:
        raise HTTPException(status_code=500, detail="Could not retrieve OpenStack networks.")
    return networks 