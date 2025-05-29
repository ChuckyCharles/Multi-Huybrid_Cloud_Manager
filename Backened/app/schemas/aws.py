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