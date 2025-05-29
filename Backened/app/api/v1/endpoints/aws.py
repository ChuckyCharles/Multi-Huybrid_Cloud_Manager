from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List, Optional, Dict
from app.core.aws import AWSClient
from app.core.security import get_current_active_user
from pydantic import BaseModel
import boto3
from botocore.exceptions import ClientError
from app.schemas.aws import EC2Instance, S3Bucket, CloudWatchMetric

router = APIRouter()

def get_aws_client() -> AWSClient:
    return AWSClient()

class AWSCredentials(BaseModel):
    access_key_id: str
    secret_access_key: str
    region: str = "us-east-1"

class AWSResourceDiscovery(BaseModel):
    ec2_instances: List[Dict]
    s3_buckets: List[Dict]
    rds_instances: List[Dict]
    lambda_functions: List[Dict]
    cloudwatch_metrics: List[Dict]

@router.post("/credentials")
async def set_aws_credentials(credentials: AWSCredentials):
    """Set AWS credentials for the session"""
    try:
        # Test the credentials
        session = boto3.Session(
            aws_access_key_id=credentials.access_key_id,
            aws_secret_access_key=credentials.secret_access_key,
            region_name=credentials.region
        )
        
        # Test the credentials by making a simple API call
        sts = session.client('sts')
        sts.get_caller_identity()
        
        # Store the credentials in the AWSClient
        aws_client = AWSClient()
        aws_client.set_credentials(
            access_key_id=credentials.access_key_id,
            secret_access_key=credentials.secret_access_key,
            region=credentials.region
        )
        
        return {"message": "AWS credentials validated and stored successfully"}
    except ClientError as e:
        raise HTTPException(status_code=400, detail=f"Invalid AWS credentials: {str(e)}")

@router.get("/discover-resources", response_model=AWSResourceDiscovery)
async def discover_resources(
    aws_client: AWSClient = Depends(get_aws_client)
):
    """Discover all AWS resources in the account"""
    try:
        # Get EC2 instances
        ec2_instances = await aws_client.get_ec2_instances()
        
        # Get S3 buckets
        s3_buckets = await aws_client.get_s3_buckets()
        
        # Get RDS instances
        rds_instances = await aws_client.get_rds_instances()
        
        # Get Lambda functions
        lambda_functions = await aws_client.get_lambda_functions()
        
        # Get CloudWatch metrics
        cloudwatch_metrics = await aws_client.get_cloudwatch_metrics("AWS/EC2", "CPUUtilization")
        
        return AWSResourceDiscovery(
            ec2_instances=ec2_instances,
            s3_buckets=s3_buckets,
            rds_instances=rds_instances,
            lambda_functions=lambda_functions,
            cloudwatch_metrics=cloudwatch_metrics
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error discovering resources: {str(e)}")

@router.get("/ec2/instances", response_model=List[EC2Instance])
async def get_ec2_instances(
    current_user = Depends(get_current_active_user),
    aws_client: AWSClient = Depends(get_aws_client)
):
    """
    Get all EC2 instances from AWS
    """
    return await aws_client.get_ec2_instances()

@router.get("/s3/buckets", response_model=List[S3Bucket])
async def get_s3_buckets(
    current_user = Depends(get_current_active_user),
    aws_client: AWSClient = Depends(get_aws_client)
):
    """
    Get all S3 buckets from AWS
    """
    return await aws_client.get_s3_buckets()

@router.get("/cloudwatch/metrics/{namespace}/{metric_name}", response_model=List[CloudWatchMetric])
async def get_cloudwatch_metrics(
    namespace: str,
    metric_name: str,
    current_user = Depends(get_current_active_user),
    aws_client: AWSClient = Depends(get_aws_client)
):
    """
    Get CloudWatch metrics for a specific namespace and metric name
    """
    return await aws_client.get_cloudwatch_metrics(namespace, metric_name)

@router.post("/ec2/launch")
async def launch_ec2_instance(
    instance_type: str = Body(...),
    ami_id: str = Body(...),
    key_name: str = Body(...)
):
    aws_client = AWSClient()
    try:
        response = aws_client.ec2.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_name,
            MinCount=1,
            MaxCount=1
        )
        return {"instance_id": response["Instances"][0]["InstanceId"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 