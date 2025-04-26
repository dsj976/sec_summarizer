from sec_summarizer.summarizer.huggingface_summarizer import HuggingfaceSummarizer


class Summarizer:
    def __init__(self, model):
        self.model = model
        self.client = self._load_model(model)

    def _load_model(self, model):
        """
        Load the model based on the provided model name.
        """
        if model.startswith("huggingface-"):
            model_name = model.split("huggingface-")[-1]
            return HuggingfaceSummarizer(model_name)

        msg = f"Model not supported: {model}."
        raise ValueError(msg)

    def summarize(self, text):
        """
        Summarize the given text using the loaded model.
        """
        return self.client.summarize(text)
