import re


class DescriptionExtractor:
    def extract_from_filing(self, filing_text: str):
        """Extract the business description from the 10-K filing."""

        normalized_text = re.sub(r"\s+", " ", filing_text)  # normalize whitespace

        # Define regex patterns for start and end of the business description.
        # In the 10-K filing, the business description usually starts with
        # "Item 1. Business" and ends with "Item 1A. Risk Factors"
        start_pattern = r"item\s+1[\.:]?\s+business"
        end_pattern = r"item\s+1a[\.:]?\s+risk\s+factors"

        # search for patterns, ignoring case
        start_match = re.search(start_pattern, normalized_text, re.IGNORECASE)
        end_match = re.search(end_pattern, normalized_text, re.IGNORECASE)

        if start_match and end_match:
            start_index = start_match.end()
            end_index = end_match.start()
            return normalized_text[start_index:end_index].strip()

        msg = "Business description not found in the filing text."
        raise ValueError(msg)
