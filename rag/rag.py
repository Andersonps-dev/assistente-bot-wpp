import psycopg2
from decouple import config
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DATABASE_URL = config('DATABASE_URL')

def load_documents_from_db():
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    cursor.execute("SELECT content FROM business_data")
    rows = cursor.fetchall()
    documents = [row[0] for row in rows]
    connection.close()
    return documents

if __name__ == '__main__':
    docs = load_documents_from_db()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = text_splitter.split_documents(
        documents=docs,
    )

    persist_directory = '/app/chroma_data'

    embedding = HuggingFaceEmbeddings()
    vector_store = Chroma(
        embedding_function=embedding,
        persist_directory=persist_directory,
    )
    vector_store.add_documents(
        documents=chunks,
    )