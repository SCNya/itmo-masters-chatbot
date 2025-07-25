from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
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

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.from_documents(texts, embeddings)

    llm = ChatOpenAI(
        model_name="Qwen/Qwen3-235B-A22B-Instruct-2507:novita",
        openai_api_key="",
        openai_api_base="https://router.huggingface.co/v1",
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
