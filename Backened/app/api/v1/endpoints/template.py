from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.core.template import TemplateClient
from app.schemas.template import CloudTemplate, KubernetesTemplate, CustomTemplate
from fastapi.responses import FileResponse, JSONResponse
from fastapi import UploadFile, File, Form
import os
import subprocess

router = APIRouter()

TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../Frontend/Charles_v3/public/templates'))

def get_template_client() -> TemplateClient:
    return TemplateClient()

@router.get("/cloud", response_model=List[CloudTemplate])
async def get_cloud_templates(
    template_client: TemplateClient = Depends(get_template_client)
):
    """Get all cloud templates"""
    templates = await template_client.get_cloud_templates()
    if not templates:
        raise HTTPException(status_code=500, detail="Could not retrieve cloud templates.")
    return templates

@router.get("/kubernetes", response_model=List[KubernetesTemplate])
async def get_kubernetes_templates(
    template_client: TemplateClient = Depends(get_template_client)
):
    """Get all Kubernetes templates"""
    templates = await template_client.get_kubernetes_templates()
    if not templates:
        raise HTTPException(status_code=500, detail="Could not retrieve Kubernetes templates.")
    return templates

@router.get("/custom", response_model=List[CustomTemplate])
async def get_custom_templates(
    template_client: TemplateClient = Depends(get_template_client)
):
    """Get all custom templates"""
    templates = await template_client.get_custom_templates()
    if not templates:
        raise HTTPException(status_code=500, detail="Could not retrieve custom templates.")
    return templates

@router.get("/content/{template_filename}")
def get_template_content(template_filename: str):
    file_path = os.path.join(TEMPLATE_DIR, template_filename)
    if not os.path.isfile(file_path):
        return JSONResponse(status_code=404, content={"error": "Template not found"})
    return FileResponse(file_path)

@router.post("/deploy/terraform")
def deploy_terraform(template_filename: str = Form(...), region: str = Form(None), ami: str = Form(None), instance_type: str = Form(None), key_name: str = Form(None)):
    """Trigger a Terraform deployment using the specified template."""
    file_path = os.path.join(TEMPLATE_DIR, template_filename)
    if not os.path.isfile(file_path):
        return JSONResponse(status_code=404, content={"error": "Template not found"})
    # Write variables.tfvars
    tfvars_content = f'region = "{region}"
ami = "{ami}"
instance_type = "{instance_type}"
key_name = "{key_name}"
'
    tfvars_path = os.path.join(TEMPLATE_DIR, 'variables.auto.tfvars')
    with open(tfvars_path, 'w') as f:
        f.write(tfvars_content)
    # Run terraform init & apply
    try:
        subprocess.run(["terraform", "init"], cwd=TEMPLATE_DIR, check=True)
        subprocess.run(["terraform", "apply", "-auto-approve"], cwd=TEMPLATE_DIR, check=True)
        return {"message": "Terraform deployment started."}
    except subprocess.CalledProcessError as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/deploy/ansible")
def deploy_ansible(template_filename: str = Form(...), hosts_file: UploadFile = File(...)):
    """Trigger an Ansible playbook deployment using the specified template."""
    file_path = os.path.join(TEMPLATE_DIR, template_filename)
    if not os.path.isfile(file_path):
        return JSONResponse(status_code=404, content={"error": "Template not found"})
    # Save hosts file
    hosts_path = os.path.join(TEMPLATE_DIR, 'hosts')
    with open(hosts_path, 'wb') as f:
        f.write(hosts_file.file.read())
    # Run ansible-playbook
    try:
        subprocess.run(["ansible-playbook", file_path, "-i", hosts_path], check=True)
        return {"message": "Ansible playbook deployment started."}
    except subprocess.CalledProcessError as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/deploy/k8s")
def deploy_k8s(template_filename: str = Form(...), kubeconfig: UploadFile = File(...)):
    """Apply a Kubernetes YAML template using kubectl and a provided kubeconfig."""
    file_path = os.path.join(TEMPLATE_DIR, template_filename)
    if not os.path.isfile(file_path):
        return JSONResponse(status_code=404, content={"error": "Template not found"})
    # Save kubeconfig
    kubeconfig_path = os.path.join(TEMPLATE_DIR, 'kubeconfig')
    with open(kubeconfig_path, 'wb') as f:
        f.write(kubeconfig.file.read())
    # Run kubectl apply
    try:
        subprocess.run(["kubectl", "--kubeconfig", kubeconfig_path, "apply", "-f", file_path], check=True)
        return {"message": "Kubernetes deployment started."}
    except subprocess.CalledProcessError as e:
        return JSONResponse(status_code=500, content={"error": str(e)}) 