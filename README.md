# sec_summarizer

[![Actions Status][actions-badge]][actions-link]
[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

An Application Programming Interface (API) to summarize a company description from its latest 10-K filing.
The solution is based on the [SEC EDGAR database](https://www.sec.gov/edgar/searchedgar/companysearch.html), and currently only supports the [Hugging Face Transformers library](https://huggingface.co/docs/transformers/index) to summarize the business description.

## Installation

Install from source inside a virtual environment:

```bash
git clone https://github.com/dsj976/sec_summarizer
cd sec_summarizer
python -m venv .venv
source .venv/bin/activate
python -m pip install .
```

## Usage

Refer to the notebook `api_demo.ipynb` for a demonstration of how to use the API. Importantly, you need to specify your EDGAR identity with an email address in order to access the SEC EDGAR database. You can do this by setting the `EDGAR_IDENTITY` environment variable:

```bash
export EDGAR_IDENTITY="anonymous@user.com"
```

In order to serve the API from a Docker container, you should create a `.env` file in the root directory of the project specifying your EDGAR identity. The file should look like this:

```bash
EDGAR_IDENTITY="anonymous@user.com"
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on how to contribute.

## License

Distributed under the terms of the [MIT license](LICENSE).


<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/dsj976/sec_summarizer/workflows/CI/badge.svg
[actions-link]:             https://github.com/dsj976/sec_summarizer/actions
[pypi-link]:                https://pypi.org/project/sec_summarizer/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/sec_summarizer
[pypi-version]:             https://img.shields.io/pypi/v/sec_summarizer
<!-- prettier-ignore-end -->
