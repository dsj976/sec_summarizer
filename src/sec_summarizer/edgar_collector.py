from edgar import Company


class EdgarCollector:
    def get_latest_10k(self, ticker):
        """Given a ticker, get the latest 10-K filing."""

        try:
            return Company(ticker).get_filings(form="10-K").latest(1)
        except Exception as e:
            msg = f"Error fetching 10-K filing for {ticker}: {e}."
            raise Exception(msg) from e
