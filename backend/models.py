from pydantic import BaseModel, Field


class PolicyRequest(BaseModel):
    policy_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)
    property_address: str
    coverage_amount: float = Field(gt=0)


class PolicyResponse(BaseModel):
    workflow_id: str
    status: str