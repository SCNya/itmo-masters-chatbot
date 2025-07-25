from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter


def create_qa_chain(text: str):
    """
    Создает цепочку QA из текста.
    """
    with open("temp_data.txt", "w") as f:
        f.write(text)

    loader = TextLoader("temp_data.txt")
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(
        openai_api_key="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",
        openai_api_base="https://openrouter.ai/api/v1",
    )
    vectorstore = FAISS.from_documents(texts, embeddings)

    llm = ChatOpenAI(
        model_name="qwen/qwen3-235b-a22b-07-25:free",
        openai_api_key="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",
        openai_api_base="https://openrouter.ai/api/v1",
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
    )

    return qa_chain


def get_answer(qa_chain, question: str) -> str:
    """
    Получает ответ на вопрос из цепочки QA.
    """
    answer = qa_chain.run(question)
    return answer
