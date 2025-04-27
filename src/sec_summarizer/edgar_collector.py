from edgar import Company


class EdgarCollector:
    """Class to collect 10-K filings from EDGAR."""

    def __init__(self, ticker):
        self.ticker = ticker
        self.filing = None
        self.business_description = None

    def get_latest_10k(self):
        """Given a ticker, get the latest 10-K filing."""
        try:
            self.filing = Company(self.ticker).get_filings(form="10-K").latest(1)
        except Exception as e:
            msg = f"Error fetching 10-K filing for {self.ticker}: {e}."
            raise Exception(msg) from e

    def get_business_description(self):
        """Fetch the business description from the latest 10-K filing."""
        if self.filing is None:
            self.get_latest_10k()
        try:
            filing_obj = self.filing.obj()
            self.business_description = filing_obj.business
        except AttributeError as e:
            msg = f"Error fetching business description for {self.ticker}: {e}."
            raise Exception(msg) from e
