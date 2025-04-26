from sec_summarizer.summarizer.huggingface_summarizer import HuggingfaceSummarizer


def test_chunk_text():
    """
    Test the _chunk_text method of the HuggingfaceSummarizer class.
    """
    summarizer = HuggingfaceSummarizer()
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
    chunks = summarizer._chunk_text(text, chunk_size)
    assert len(chunks) == 2
    assert chunks[0] == sentences[0] + " " + sentences[1]
    assert chunks[1] == sentences[2] + " " + sentences[3]
