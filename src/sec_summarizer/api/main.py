import os

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sec_summarizer.api.schemas import CompanyCreate, CompanyResponse
from sec_summarizer.database.engine import get_db, init_db
from sec_summarizer.database.models import Company

app = FastAPI(
    title="SEC Summarizer API",
    description=(
        "An API for summarizing the business description of companies "
        "from SEC 10-K filings."
    ),
    version="0.1.0",
)


@app.post("/companies/", response_model=CompanyResponse)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    """Create a new company record in the database."""

    # check if the company already exists
    existing_company = db.query(Company).filter_by(ticker=company.ticker).first()
    if existing_company:
        raise HTTPException(
            status_code=400,
            detail="Company with this ticker already exists.",
        )

    new_company = Company(ticker=company.ticker, name=company.name)
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


def main():
    init_db()

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("sec_summarizer.api.main:app", host="0.0.0.0", port=port, reload=True)


if __name__ == "__main__":
    main()
