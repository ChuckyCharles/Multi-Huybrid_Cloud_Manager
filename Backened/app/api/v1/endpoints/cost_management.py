from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any
from app.core.cost_management import CostClient
from app.schemas.cost_management import AWSCostExplorerData, ResourceOptimizationSuggestion, BudgetStatus
from datetime import date, timedelta

router = APIRouter()

def get_cost_client() -> CostClient:
    return CostClient()

@router.get("/aws/daily-costs", response_model=AWSCostExplorerData)
async def get_aws_daily_costs(
    cost_client: CostClient = Depends(get_cost_client),
    start_date: date = Query(default=(date.today() - timedelta(days=30)).isoformat()),
    end_date: date = Query(default=date.today().isoformat())
):
    """Get daily AWS costs grouped by service for a specified time period"""
    # Ensure start_date is before or equal to end_date
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date cannot be after end_date.")

    # AWS Cost Explorer limits data to the last 12 months for GetCostAndUsage
    # and also a maximum of 1 year in a single query.
    # For simplicity, we'll let the AWS API handle exact limits for now, but 
    # in a real app, you might want to add more robust validation here.

    cost_data = await cost_client.get_aws_daily_costs(start_date.isoformat(), end_date.isoformat())
    if not cost_data:
        raise HTTPException(status_code=500, detail="Could not retrieve AWS daily costs. Check backend logs for details.")
    return AWSCostExplorerData(results_by_time=cost_data)

@router.get("/resource-optimization-suggestions", response_model=List[ResourceOptimizationSuggestion])
async def get_resource_optimization_suggestions(
    cost_client: CostClient = Depends(get_cost_client)
):
    """Get resource optimization suggestions"""
    suggestions = await cost_client.get_resource_optimization_suggestions()
    if not suggestions:
        raise HTTPException(status_code=500, detail="Could not retrieve resource optimization suggestions.")
    return suggestions

@router.get("/budget-status", response_model=List[BudgetStatus])
async def get_budget_status(
    cost_client: CostClient = Depends(get_cost_client)
):
    """Get current budget status"""
    budgets = await cost_client.get_budget_status()
    if not budgets:
        raise HTTPException(status_code=500, detail="Could not retrieve budget status.")
    return budgets
