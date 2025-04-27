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


class FilingCreate(BaseModel):
    company_ticker: str = Field(
        ..., description="Company stock ticker", example="GOOGL"
    )
    model: str = Field(
        default="huggingface-facebook/bart-large-cnn",
        description="Model to be used for summarization",
        example="huggingface-facebook/bart-large-cnn",
    )


class FilingSummary(BaseModel):
    id: int
    company_id: int
    filing_type: str
    filing_date: datetime
    business_summary: str
    model_used: str
    created_at: datetime

    class Config:
        orm_mode = True
