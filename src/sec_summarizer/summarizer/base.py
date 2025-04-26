from sec_summarizer.summarizer.huggingface_summarizer import HuggingfaceSummarizer


class Summarizer:
    def __init__(self, text: str, model: str):
        self.text = text
        self.model = model
        self.client = self._load_model(model)

    def _load_model(self, model: str):
        """
        Load the model based on the provided model name.
        """
        if model.startswith("huggingface-"):
            model_name = model.split("huggingface-")[-1]
            return HuggingfaceSummarizer(model_name)

        msg = f"Model not supported: {model}."
        raise ValueError(msg)

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

    def summarize(self, chunk_size=1024):
        """
        Summarize the given text using the loaded model.
        """
        if len(self.text) > chunk_size:
            self.chunks = self._chunk_text(self.text, chunk_size=chunk_size)
        else:
            self.chunks = [self.text]
        self.summary = self.client.summarize(self.chunks)
