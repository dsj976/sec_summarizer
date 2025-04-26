import os

import uvicorn
from fastapi import FastAPI

from sec_summarizer.database.engine import init_db

app = FastAPI(
    title="SEC Summarizer API",
    description=(
        "An API for summarizing the business description of companies "
        "from SEC 10-K filings."
    ),
    version="0.1.0",
)


def main():
    init_db()

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("sec_summarizer.api.main:app", host="0.0.0.0", port=port, reload=True)


if __name__ == "__main__":
    main()
