import os
from datetime import datetime

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sec_summarizer.api.schemas import (
    CompanyCreate,
    CompanyResponse,
    FilingResponse,
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


@app.get("/companies/{ticker}", response_model=CompanyResponse)
def get_company(ticker: str, db: Session = Depends(get_db)):
    """Get a company record by its ticker symbol."""

    company = db.query(Company).filter_by(ticker=ticker).first()
    if not company:
        raise HTTPException(
            status_code=404,
            detail=f"Company {ticker} not found.",
        )
    return company


@app.get("/companies/", response_model=list[CompanyResponse])
def get_companies(db: Session = Depends(get_db)):
    """Get all company records in the database."""

    return db.query(Company).all()


@app.post("/filings/{ticker}", response_model=FilingResponse)
def create_filing(
    ticker: str,
    db: Session = Depends(get_db),
):
    """Create a new filing record in the database for a given company ticker."""

    # check if the company exists
    company = db.query(Company).filter_by(ticker=ticker).first()
    if not company:
        raise HTTPException(
            status_code=404,
            detail=f"Company {ticker} not found.",
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
            detail=f"Filing for {ticker} already exists.",
        )

    # fetch the filing from SEC EDGAR
    collector = EdgarCollector(ticker)
    collector.get_business_description()

    new_filing = Filing(
        company_id=company.id,
        filing_date=collector.filing.filing_date,
        business_description=collector.business_description,
    )
    db.add(new_filing)
    db.commit()
    db.refresh(new_filing)
    # truncate the business description to 1000 characters
    new_filing.business_description = (
        new_filing.business_description[:1000] + "..."
        if len(new_filing.business_description) > 1000
        else new_filing.business_description
    )
    return new_filing


@app.patch("/filings/{ticker}/summarize", response_model=FilingResponse)
def summarize_filing(
    ticker: str,
    model: str = "huggingface-facebook/bart-large-cnn",
    db: Session = Depends(get_db),
):
    """Summarize the business description of a filing for a given company ticker."""

    # check if the company exists
    company = db.query(Company).filter_by(ticker=ticker).first()
    if not company:
        raise HTTPException(
            status_code=404,
            detail=f"Company {ticker} not found.",
        )

    # check if the filing exists
    filing = (
        db.query(Filing)
        .filter_by(
            company_id=company.id,
        )
        .first()
    )
    if not filing:
        raise HTTPException(
            status_code=404,
            detail=f"Filing for {ticker} not found.",
        )

    # check there is a business description
    business_description = filing.business_description
    if not business_description:
        raise HTTPException(
            status_code=400,
            detail=f"Business description for {ticker} is empty.",
        )

    # summarize the business description
    summarizer = Summarizer(text=business_description, model=model)
    summarizer.summarize()
    if not summarizer.summary:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to summarize the business description for {ticker}.",
        )

    # update the filing with the summary
    filing.business_summary = summarizer.summary
    filing.model_used = model
    filing.created_at = datetime.now()
    db.commit()
    db.refresh(filing)

    # truncate the business description to 1000 characters
    filing.business_description = (
        filing.business_description[:1000] + "..."
        if len(filing.business_description) > 1000
        else filing.business_description
    )
    return filing


def main():
    init_db()

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("sec_summarizer.api.main:app", host="0.0.0.0", port=port, reload=True)


if __name__ == "__main__":
    main()
