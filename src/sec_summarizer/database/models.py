from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    ticker = Column(String(10), nullable=False, unique=True)
    filings = relationship("Filing", back_populates="company")

    def __repr__(self):
        return f"<Company(name='{self.name}', ticker='{self.ticker}')>"


class Filing(Base):
    __tablename__ = "filings"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    filing_type = Column(String(50), nullable=False, default="10-K")
    filing_date = Column(DateTime, nullable=False)
    business_description = Column(Text, nullable=True)
    business_summary = Column(Text, nullable=True)
    model_used = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="filings")

    def __repr__(self):
        return (
            f"<Filing(company='{self.company.ticker}', "
            f"type='{self.filing_type}', date='{self.filing_date}')>"
        )
