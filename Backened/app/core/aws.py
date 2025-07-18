import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from fastapi import HTTPException
from app.core.config import settings
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class AWSClient:
    def __init__(self):
        self._session = None
        self._clients = {}
        self.config = Config(
            region_name=settings.AWS_REGION,
            retries=dict(
                max_attempts=3
            )
        )
        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize AWS service clients"""
        if self._session:
            # Use session credentials if available
            self.ec2 = self._session.client('ec2', config=self.config)
            self.s3 = self._session.client('s3', config=self.config)
            self.iam = self._session.client('iam', config=self.config)
            self.cloudwatch = self._session.client('cloudwatch', config=self.config)
            self.rds = self._session.client('rds', config=self.config)
            self.lambda_client = self._session.client('lambda', config=self.config)
        else:
            # Use default credentials
            self.ec2 = boto3.client('ec2', config=self.config)
            self.s3 = boto3.client('s3', config=self.config)
            self.iam = boto3.client('iam', config=self.config)
            self.cloudwatch = boto3.client('cloudwatch', config=self.config)
            self.rds = boto3.client('rds', config=self.config)
            self.lambda_client = boto3.client('lambda', config=self.config)

    def set_credentials(self, access_key_id: str, secret_access_key: str, region: str):
        """Set AWS credentials for the session"""
        self._session = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region
        )
        self._initialize_clients()

    async def handle_aws_error(self, error: ClientError):
        error_code = error.response['Error']['Code']
        error_message = error.response['Error']['Message']
        
        if error_code == 'ThrottlingException':
            raise HTTPException(
                status_code=429,
                detail="AWS API rate limit exceeded. Please try again later."
            )
        elif error_code == 'AccessDeniedException':
            raise HTTPException(
                status_code=403,
                detail="Access denied to AWS resource."
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"AWS Error: {error_message}"
            )

    async def get_ec2_instances(self) -> List[Dict]:
        try:
            response = self.ec2.describe_instances()
            instances = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instances.append({
                        'InstanceId': instance['InstanceId'],
                        'InstanceType': instance['InstanceType'],
                        'State': instance['State'],
                        'LaunchTime': instance['LaunchTime'].isoformat(),
                        'Tags': instance.get('Tags', []),
                        'PublicIpAddress': instance.get('PublicIpAddress'),
                        'PrivateIpAddress': instance.get('PrivateIpAddress')
                    })
            return instances
        except ClientError as e:
            await self.handle_aws_error(e)

    async def get_s3_buckets(self) -> List[Dict]:
        try:
            response = self.s3.list_buckets()
            buckets = []
            for bucket in response['Buckets']:
                # Get bucket location
                location = self.s3.get_bucket_location(Bucket=bucket['Name'])
                buckets.append({
                    'name': bucket['Name'],
                    'creation_date': bucket['CreationDate'].isoformat(),
                    'region': location['LocationConstraint'] or 'us-east-1'
                })
            return buckets
        except ClientError as e:
            await self.handle_aws_error(e)

    async def get_rds_instances(self) -> List[Dict]:
        try:
            response = self.rds.describe_db_instances()
            instances = []
            for instance in response['DBInstances']:
                instances.append({
                    'id': instance['DBInstanceIdentifier'],
                    'engine': instance['Engine'],
                    'status': instance['DBInstanceStatus'],
                    'size': instance['DBInstanceClass'],
                    'storage': instance['AllocatedStorage']
                })
            return instances
        except ClientError as e:
            await self.handle_aws_error(e)

    async def get_lambda_functions(self) -> List[Dict]:
        try:
            response = self.lambda_client.list_functions()
            functions = []
            for function in response['Functions']:
                functions.append({
                    'name': function['FunctionName'],
                    'runtime': function['Runtime'],
                    'memory_size': function['MemorySize'],
                    'timeout': function['Timeout'],
                    'last_modified': function['LastModified']
                })
            return functions
        except ClientError as e:
            await self.handle_aws_error(e)

    async def get_cloudwatch_metrics(self, namespace: str, metric_name: str) -> List[Dict]:
        try:
            response = self.cloudwatch.get_metric_statistics(
                Namespace=namespace,
                MetricName=metric_name,
                StartTime=datetime.utcnow() - timedelta(hours=1),
                EndTime=datetime.utcnow(),
                Period=300,
                Statistics=['Average']
            )
            return response['Datapoints']
        except ClientError as e:
            await self.handle_aws_error(e)

    async def get_vpcs(self) -> List[Dict]:
        try:
            response = self.ec2.describe_vpcs()
            vpcs = []
            for vpc in response['Vpcs']:
                vpcs.append({
                    'id': vpc['VpcId'],
                    'state': vpc['State'],
                    'cidr_block': vpc['CidrBlock']
                })
            return vpcs
        except ClientError as e:
            await self.handle_aws_error(e)

    async def launch_instance(self, image_id: str, instance_type: str, min_count: int = 1, max_count: int = 1, key_name: Optional[str] = None):
        try:
            params = {
                "ImageId": image_id,
                "InstanceType": instance_type,
                "MinCount": min_count,
                "MaxCount": max_count,
            }
            if key_name:
                params["KeyName"] = key_name
            response = self.ec2.run_instances(**params)
            return response['Instances']
        except ClientError as e:
            await self.handle_aws_error(e)

    async def get_ec2_images(self) -> List[Dict]:
        try:
            # Fetch images owned by Amazon (public AMIs) and self (private/custom AMIs)
            response = self.ec2.describe_images(
                Owners=['amazon', 'self'],
                Filters=[
                    {'Name': 'state', 'Values': ['available']},
                    {'Name': 'image-type', 'Values': ['machine']}
                ]
            )
            images = []
            for image in response['Images']:
                images.append({
                    'ImageId': image['ImageId'],
                    'Name': image.get('Name', 'N/A'),
                    'Description': image.get('Description', 'N/A'),
                    'CreationDate': image['CreationDate'],
                    'State': image['State'],
                    'Architecture': image['Architecture'],
                    'PlatformDetails': image.get('PlatformDetails', 'N/A'),
                    'UsageOperation': image.get('UsageOperation', 'N/A'),
                    'OwnerId': image['OwnerId'],
                })
            return images
        except ClientError as e:
            await self.handle_aws_error(e)

    async def create_s3_bucket(self, bucket_name: str, region: Optional[str] = None):
        try:
            if region and region != 'us-east-1':
                # For regions other than us-east-1, LocationConstraint is required
                response = self.s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            else:
                response = self.s3.create_bucket(Bucket=bucket_name)
            return response
        except ClientError as e:
            await self.handle_aws_error(e)

    async def create_rds_database(self, db_instance_identifier: str, db_instance_class: str, engine: str, master_username: str, master_user_password: str, allocated_storage: int):
        try:
            response = self.rds.create_db_instance(
                DBInstanceIdentifier=db_instance_identifier,
                DBInstanceClass=db_instance_class,
                Engine=engine,
                MasterUsername=master_username,
                MasterUserPassword=master_user_password,
                AllocatedStorage=allocated_storage,
            )
            return response['DBInstance']
        except ClientError as e:
            await self.handle_aws_error(e)

    async def upload_file_to_s3(self, bucket_name: str, object_name: str, file_content: bytes):
        try:
            response = self.s3.put_object(
                Bucket=bucket_name,
                Key=object_name,
                Body=file_content
            )
            return response
        except ClientError as e:
            await self.handle_aws_error(e)

    async def put_bucket_policy(self, bucket_name: str, policy: str):
        try:
            response = self.s3.put_bucket_policy(
                Bucket=bucket_name,
                Policy=policy
            )
            return response
        except ClientError as e:
            await self.handle_aws_error(e)

    async def delete_s3_object(self, bucket_name: str, object_name: str):
        try:
            response = self.s3.delete_object(
                Bucket=bucket_name,
                Key=object_name
            )
            return response
        except ClientError as e:
            await self.handle_aws_error(e) 