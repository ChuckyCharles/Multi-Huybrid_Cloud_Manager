from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class EC2Instance(BaseModel):
    InstanceId: str
    InstanceType: str
    State: dict
    Tags: Optional[List[dict]] = None
    LaunchTime: datetime
    PublicIpAddress: Optional[str] = None
    PrivateIpAddress: Optional[str] = None

    class Config:
        from_attributes = True

class S3Bucket(BaseModel):
    Name: str
    CreationDate: datetime
    Owner: Optional[dict] = None

    class Config:
        from_attributes = True

class CloudWatchMetric(BaseModel):
    Timestamp: datetime
    Average: float
    Unit: str
    Period: int

    class Config:
        from_attributes = True

class VPC(BaseModel):
    id: str
    state: str
    cidr_block: str

    class Config:
        from_attributes = True

class EC2LaunchRequest(BaseModel):
    image_id: str
    instance_type: str
    min_count: int = 1
    max_count: int = 1
    key_name: Optional[str] = None

class S3BucketCreateRequest(BaseModel):
    bucket_name: str
    region: Optional[str] = None

class RDSCreateDatabaseRequest(BaseModel):
    db_instance_identifier: str
    db_instance_class: str
    engine: str
    master_username: str
    master_user_password: str
    allocated_storage: int

class S3AccessPolicyRequest(BaseModel):
    bucket_name: str
    policy: str # JSON policy as a string

class S3DeleteObjectRequest(BaseModel):
    bucket_name: str
    object_name: str

class EC2Image(BaseModel):
    ImageId: str
    Name: str
    Description: Optional[str] = None
    CreationDate: datetime
    State: str
    Architecture: str
    PlatformDetails: Optional[str] = None
    UsageOperation: Optional[str] = None
    OwnerId: str

    class Config:
        from_attributes = True 