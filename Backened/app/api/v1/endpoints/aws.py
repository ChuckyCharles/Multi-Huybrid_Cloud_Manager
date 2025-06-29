from fastapi import APIRouter, Depends, HTTPException, Body, File, UploadFile
from typing import List, Optional, Dict
from app.core.aws import AWSClient
from app.core.security import get_current_active_user
from pydantic import BaseModel
import boto3
from botocore.exceptions import ClientError
from app.schemas.aws import EC2Instance, S3Bucket, CloudWatchMetric, EC2LaunchRequest, S3BucketCreateRequest, RDSCreateDatabaseRequest, S3AccessPolicyRequest, S3DeleteObjectRequest, EC2Image

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
    request: EC2LaunchRequest,
    current_user = Depends(get_current_active_user),
    aws_client: AWSClient = Depends(get_aws_client)
):
    """Launch a new EC2 instance"""
    try:
        response = await aws_client.launch_instance(
            image_id=request.image_id,
            instance_type=request.instance_type,
            min_count=request.min_count,
            max_count=request.max_count,
            key_name=request.key_name
        )
        return {"message": "EC2 instance launched successfully", "instances": response}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error launching EC2 instance: {str(e)}")

@router.post("/s3/create-bucket")
async def create_s3_bucket(
    request: S3BucketCreateRequest,
    current_user = Depends(get_current_active_user),
    aws_client: AWSClient = Depends(get_aws_client)
):
    """Create a new S3 bucket"""
    try:
        response = await aws_client.create_s3_bucket(
            bucket_name=request.bucket_name,
            region=request.region
        )
        return {"message": f"S3 bucket {request.bucket_name} created successfully", "response": response}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating S3 bucket: {str(e)}")

@router.post("/rds/create-database")
async def create_rds_database(
    request: RDSCreateDatabaseRequest,
    current_user = Depends(get_current_active_user),
    aws_client: AWSClient = Depends(get_aws_client)
):
    """Create a new RDS database instance"""
    try:
        response = await aws_client.create_rds_database(
            db_instance_identifier=request.db_instance_identifier,
            db_instance_class=request.db_instance_class,
            engine=request.engine,
            master_username=request.master_username,
            master_user_password=request.master_user_password,
            allocated_storage=request.allocated_storage
        )
        return {"message": f"RDS database {request.db_instance_identifier} created successfully", "db_instance": response}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating RDS database: {str(e)}")

@router.post("/s3/upload-file")
async def upload_s3_file(
    bucket_name: str = Body(..., embed=True),
    object_name: str = Body(..., embed=True),
    file: UploadFile = File(...),
    current_user = Depends(get_current_active_user),
    aws_client: AWSClient = Depends(get_aws_client)
):
    """Upload a file to an S3 bucket"""
    try:
        file_content = await file.read()
        await aws_client.upload_file_to_s3(
            bucket_name=bucket_name,
            object_name=object_name,
            file_content=file_content
        )
        return {"message": f"File '{object_name}' uploaded to bucket '{bucket_name}' successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file to S3: {str(e)}")

@router.post("/s3/set-bucket-policy")
async def set_s3_bucket_policy(
    request: S3AccessPolicyRequest,
    current_user = Depends(get_current_active_user),
    aws_client: AWSClient = Depends(get_aws_client)
):
    """Set an S3 bucket policy"""
    try:
        await aws_client.put_bucket_policy(
            bucket_name=request.bucket_name,
            policy=request.policy
        )
        return {"message": f"Policy set for bucket '{request.bucket_name}' successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error setting S3 bucket policy: {str(e)}")

@router.post("/s3/delete-object")
async def delete_s3_object(
    request: S3DeleteObjectRequest,
    current_user = Depends(get_current_active_user),
    aws_client: AWSClient = Depends(get_aws_client)
):
    """Delete an object from an S3 bucket"""
    try:
        await aws_client.delete_s3_object(
            bucket_name=request.bucket_name,
            object_name=request.object_name
        )
        return {"message": f"Object '{request.object_name}' deleted from bucket '{request.bucket_name}' successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting S3 object: {str(e)}")

@router.get("/ec2/images", response_model=List[EC2Image])
async def get_ec2_images(
    current_user = Depends(get_current_active_user),
    aws_client: AWSClient = Depends(get_aws_client)
):
    """
    Get all EC2 images from AWS
    """
    return await aws_client.get_ec2_images() 