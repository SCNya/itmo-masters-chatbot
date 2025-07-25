from unittest.mock import patch

from master_program_chatbot.qa import create_qa_chain, get_answer


def test_create_qa_chain():
    with patch("master_program_chatbot.qa.HuggingFaceEmbeddings"), patch(
        "master_program_chatbot.qa.FAISS"
    ), patch("master_program_chatbot.qa.ChatOpenAI"), patch(
        "master_program_chatbot.qa.RetrievalQA"
    ):
        text = "This is a test text."
        qa_chain = create_qa_chain(text)
        assert qa_chain is not None


def test_get_answer():
    mock_qa_chain = patch(
        "master_program_chatbot.qa.RetrievalQA",
    )
    mock_qa_chain.run = lambda question: "This is a test answer."
    answer = get_answer(mock_qa_chain, "What is the answer?")
    assert answer == "This is a test answer."
