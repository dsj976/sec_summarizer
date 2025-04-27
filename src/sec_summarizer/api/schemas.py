from datetime import datetime

from pydantic import BaseModel, Field


class CompanyCreate(BaseModel):
    name: str = Field(..., description="Name of the company", example="Google")
    ticker: str = Field(..., description="Company stock ticker", example="GOOGL")


class CompanyResponse(BaseModel):
    id: int
    name: str
    ticker: str

    class Config:
        orm_mode = True


class FilingResponse(BaseModel):
    id: int
    company_id: int
    filing_type: str
    filing_date: datetime
    business_description: str
    business_summary: str | None = None
    model_used: str | None = None
    created_at: datetime | None = None

    class Config:
        orm_mode = True
