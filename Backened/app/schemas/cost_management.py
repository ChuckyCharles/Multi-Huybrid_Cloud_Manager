from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AWSMetricValue(BaseModel):
    amount: str
    unit: str

class AWSDimension(BaseModel):
    key: str
    value: str

class AWSResultByTime(BaseModel):
    time_period_start: str
    time_period_end: str
    total_cost: AWSMetricValue
    grouped_by: List[AWSDimension]

class AWSCostExplorerData(BaseModel):
    results_by_time: List[AWSResultByTime]

class ResourceOptimizationSuggestion(BaseModel):
    id: str
    category: str # e.g., EC2, S3, RDS
    recommendation: str
    estimated_savings_usd: float
    priority: str # e.g., High, Medium, Low

class BudgetStatus(BaseModel):
    id: str
    name: str
    amount: float
    spent: float
    forecasted_spend: float
    unit: str
    status: str # e.g., OK, WARN, ALERT 