import os

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sec_summarizer.api.schemas import (
    CompanyCreate,
    CompanyResponse,
    FilingCreate,
    FilingSummary,
)
from sec_summarizer.database.engine import get_db, init_db
from sec_summarizer.database.models import Company, Filing
from sec_summarizer.edgar_collector import EdgarCollector
from sec_summarizer.summarizer.base import Summarizer

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


@app.post("/filings/", response_model=FilingSummary)
def create_filing(
    filing: FilingCreate,
    db: Session = Depends(get_db),
):
    """Create a new filing record in the database."""

    # check if the company exists
    company = db.query(Company).filter_by(ticker=filing.company_ticker).first()
    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found.",
        )

    # check if the filing already exists
    existing_filing = (
        db.query(Filing)
        .filter_by(
            company_id=company.id,
        )
        .first()
    )
    if existing_filing:
        raise HTTPException(
            status_code=400,
            detail="Filing for this company already exists.",
        )

    # fetch the filing from SEC EDGAR
    collector = EdgarCollector(filing.company_ticker)
    collector.get_business_description()
    summarizer = Summarizer(
        text=collector.business_description,
        model=filing.model,
    )
    summarizer.summarize()
    new_filing = Filing(
        company_id=company.id,
        filing_date=collector.filing.filing_date,
        business_description=collector.business_description,
        business_summary=summarizer.summary,
        model_used=filing.model,
    )
    db.add(new_filing)
    db.commit()
    db.refresh(new_filing)
    return new_filing


def main():
    init_db()

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("sec_summarizer.api.main:app", host="0.0.0.0", port=port, reload=True)


if __name__ == "__main__":
    main()
