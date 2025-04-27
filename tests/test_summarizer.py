import pytest

from sec_summarizer.summarizer.base import Summarizer
from sec_summarizer.summarizer.huggingface_summarizer import HuggingfaceSummarizer


def test_chunk_text():
    """
    Test the _chunk_text method of the HuggingfaceSummarizer class.
    """
    sentences = [
        "This is the first sentence.",
        "This is the second sentence.",
        "This is the third sentence.",
        "This is the fourth sentence.",
    ]
    sentence_length = [len(sentence) for sentence in sentences]
    text = " ".join(sentences)
    chunk_size = max(
        (
            sentence_length[0] + sentence_length[1] + 1,
            sentence_length[2] + sentence_length[3] + 1,
        )
    )
    chunks = Summarizer._chunk_text(text, chunk_size)
    assert len(chunks) == 2
    assert chunks[0] == sentences[0] + " " + sentences[1]
    assert chunks[1] == sentences[2] + " " + sentences[3]


@pytest.mark.skipif(
    not HuggingfaceSummarizer.is_model_cached("t5-small"),
    reason="HuggingFace model is not cached locally.",
)
def test_huggingface_summarizer():
    """
    Test the Summarizer class.
    """
    sample_text = [
        "This is a test sentence. "
        "This is another test sentence. "
        "This is yet another test sentence."
    ]
    model_name = "t5-small"
    summarizer = HuggingfaceSummarizer(model_name)
    summary = summarizer.summarize(
        sample_text,
        max_length=30,
        min_length=10,
        do_sample=False,
    )
    assert isinstance(summary, str)
    assert len(summary) > 0
