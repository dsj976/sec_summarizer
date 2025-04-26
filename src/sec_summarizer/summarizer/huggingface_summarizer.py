from transformers import pipeline


class HuggingfaceSummarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        try:
            self.summarizer = pipeline("summarization", model=model_name)
        except Exception as e:
            msg = f"Error loading HuggingFace model '{model_name}': {e}"
            raise Exception(msg) from e

    @staticmethod
    def _chunk_text(text: str, chunk_size: int) -> list:
        """
        Split the text into chunks containing full sentences,
        with a maximum size of chunk_size.

        Args:
            text (str): The text to split.
            chunk_size (int): The maximum size of each chunk.

        Returns:
            list: A list of text chunks.
        """
        sentences = text.split(". ")
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            clean_sentence = sentence[:-1] if sentence.endswith(".") else sentence
            if len(current_chunk) + len(clean_sentence) + 1 <= chunk_size:
                current_chunk += clean_sentence + ". "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = clean_sentence + ". "

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def summarize(
        self,
        text: str,
        max_length: int = 150,
        min_length: int = 30,
        do_sample: bool = False,
        chunk_size: int = 1024,
    ) -> str:
        """
        Summarize the given text using the Hugging Face model.

        Args:
            text (str): The text to summarize.
            max_length (int): The maximum length of the summary.
            min_length (int): The minimum length of the summary.
            do_sample (bool): Whether you want a deterministic output (False)
                or a stochastic one (True).
            chunk_size (int): The size of the chunks to split the text into.

        Returns:
            str: The summarized text.
        """
