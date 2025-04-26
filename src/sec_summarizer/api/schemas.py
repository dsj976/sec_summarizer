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
