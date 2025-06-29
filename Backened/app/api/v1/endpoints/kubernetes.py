from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from app.core.kubernetes import KubernetesClient
from app.schemas.kubernetes import KubernetesNode, KubernetesDeployment, KubernetesPod, KubernetesService

router = APIRouter()

def get_kubernetes_client() -> KubernetesClient:
    return KubernetesClient()

@router.get("/nodes", response_model=List[KubernetesNode])
async def get_kubernetes_nodes(
    kube_client: KubernetesClient = Depends(get_kubernetes_client)
):
    """Get all Kubernetes nodes"""
    nodes = await kube_client.get_nodes()
    if not nodes:
        raise HTTPException(status_code=500, detail="Could not retrieve Kubernetes nodes. Check backend logs for details.")
    return nodes

@router.get("/deployments", response_model=List[KubernetesDeployment])
async def get_kubernetes_deployments(
    kube_client: KubernetesClient = Depends(get_kubernetes_client)
):
    """Get all Kubernetes deployments"""
    deployments = await kube_client.get_deployments()
    if not deployments:
        raise HTTPException(status_code=500, detail="Could not retrieve Kubernetes deployments. Check backend logs for details.")
    return deployments

@router.get("/pods", response_model=List[KubernetesPod])
async def get_kubernetes_pods(
    kube_client: KubernetesClient = Depends(get_kubernetes_client)
):
    """Get all Kubernetes pods"""
    pods = await kube_client.get_pods()
    if not pods:
        raise HTTPException(status_code=500, detail="Could not retrieve Kubernetes pods. Check backend logs for details.")
    return pods

@router.get("/services", response_model=List[KubernetesService])
async def get_kubernetes_services(
    kube_client: KubernetesClient = Depends(get_kubernetes_client)
):
    """Get all Kubernetes services"""
    services = await kube_client.get_services()
    if not services:
        raise HTTPException(status_code=500, detail="Could not retrieve Kubernetes services. Check backend logs for details.")
    return services 