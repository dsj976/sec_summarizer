from transformers import pipeline


class HuggingfaceSummarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        try:
            self.summarizer = pipeline("summarization", model=model_name)
        except Exception as e:
            msg = f"Error loading HuggingFace model '{model_name}': {e}"
            raise Exception(msg) from e

    def summarize(
        self,
        chunks: list[str],
        max_length: int = 150,
        min_length: int = 30,
        do_sample: bool = False,
    ) -> str:
        """
        Summarize the given text using the Hugging Face model.
        If multiple chunks are provided, they will be summarized
        hierarchically: first, each chunk will be summarized individually,
        and then the resulting summaries will be summarized again.

        Args:
            chunks (list[str]): The text to summarize, split into chunks.
            max_length (int): The maximum length of the summary.
            min_length (int): The minimum length of the summary.
            do_sample (bool): Whether you want a deterministic output (False)
                or a stochastic one (True).

        Returns:
            str: The summarized text.
        """

        summaries = []
        for chunk in chunks:
            try:
                summary = self.summarizer(
                    chunk,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=do_sample,
                )
                summaries.append(summary[0]["summary_text"])
            except Exception as e:
                msg = f"Error summarizing chunk: {e}"
                raise Exception(msg) from e

        if not summaries:
            msg = "No summaries generated. Please check the input chunks."
            raise Exception(msg)

        if len(summaries) > 1:
            final_summary = " ".join(summaries)
            return self.summarizer(
                final_summary,
                max_length=max_length,
                min_length=min_length,
                do_sample=do_sample,
            )[0]["summary_text"]

        return summaries[0]
