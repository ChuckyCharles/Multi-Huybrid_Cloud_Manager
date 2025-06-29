import boto3
from botocore.exceptions import ClientError
from typing import List, Dict, Any
import datetime
from app.core.config import settings # Import settings to get AWS credentials
import asyncio

class CostClient:
    def __init__(self):
        self.client = self._get_cost_explorer_client()

    def _get_cost_explorer_client(self):
        # Use credentials from settings or environment variables
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        aws_region = settings.AWS_REGION

        if not aws_access_key_id or not aws_secret_access_key:
            print("AWS credentials not found in settings. Make sure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set in .env or environment variables.")
            return None

        try:
            return boto3.client(
                'ce',  # Cost Explorer service
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region
            )
        except ClientError as e:
            print(f"Error initializing Cost Explorer client: {e}")
            return None

    async def get_aws_daily_costs(self, time_period_start: str, time_period_end: str) -> List[Dict]:
        if not self.client:
            return []
        
        try:
            response = self.client.get_cost_and_usage(
                TimePeriod={
                    'Start': time_period_start,
                    'End': time_period_end
                },
                Granularity='DAILY',
                Metrics=['UnblendedCost'],
                GroupBy=[
                    {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                    # Add more dimensions as needed, e.g., 'REGION', 'INSTANCE_TYPE'
                ]
            )
            
            formatted_results = []
            for result_by_time in response.get('ResultsByTime', []):
                total_cost_data = result_by_time.get('Total', {}).get('UnblendedCost', {})
                total_cost = {
                    "amount": total_cost_data.get('Amount', '0.0'),
                    "unit": total_cost_data.get('Unit', 'USD')
                }
                
                grouped_by = []
                for group in result_by_time.get('Groups', []):
                    key_list = group.get('Keys', [])
                    key = key_list[0] if key_list else "N/A Service"

                    if key and '$' in key:
                        key = key.split('$')[1].strip()

                    metrics_data = group.get('Metrics', {})
                    unblended_cost_metric = metrics_data.get('UnblendedCost', {})
                    value = unblended_cost_metric.get('Amount', '0.0')

                    grouped_by.append({
                        "key": key,
                        "value": value
                    })
                
                formatted_results.append({
                    "time_period_start": result_by_time.get('TimePeriod', {}).get('Start'),
                    "time_period_end": result_by_time.get('TimePeriod', {}).get('End'),
                    "total_cost": total_cost,
                    "grouped_by": grouped_by
                })
            return formatted_results

        except ClientError as e:
            print(f"Error fetching AWS daily costs: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

    async def get_resource_optimization_suggestions(self) -> List[Dict]:
        # Simulate fetching resource optimization suggestions
        await asyncio.sleep(0.1)
        return [
            {
                "id": "opt-001",
                "category": "EC2",
                "recommendation": "Downsize unused EC2 instances",
                "estimated_savings_usd": 150.75,
                "priority": "High"
            },
            {
                "id": "opt-002",
                "category": "S3",
                "recommendation": "Transition infrequent access S3 data to Glacier",
                "estimated_savings_usd": 50.20,
                "priority": "Medium"
            },
            {
                "id": "opt-003",
                "category": "RDS",
                "recommendation": "Delete idle RDS instances",
                "estimated_savings_usd": 200.00,
                "priority": "High"
            }
        ]

    async def get_budget_status(self) -> List[Dict]:
        # Simulate fetching budget status
        await asyncio.sleep(0.1)
        return [
            {
                "id": "bgt-001",
                "name": "Monthly Cloud Spend",
                "amount": 1000.00,
                "spent": 750.50,
                "forecasted_spend": 900.00,
                "unit": "USD",
                "status": "OK"
            },
            {
                "id": "bgt-002",
                "name": "Development Environment",
                "amount": 500.00,
                "spent": 480.00,
                "forecasted_spend": 550.00,
                "unit": "USD",
                "status": "ALERT"
            }
        ] 