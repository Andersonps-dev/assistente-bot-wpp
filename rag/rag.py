import os
import time
from decouple import config
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

os.environ['HUGGINGFACE_API_KEY'] = config('HUGGINGFACE_API_KEY')

class PDFHandler(FileSystemEventHandler):
    def __init__(self, vector_store, file_path):
        self.vector_store = vector_store
        self.file_path = file_path

    def on_modified(self, event):
        if event.src_path == self.file_path:
            print(f"Arquivo {self.file_path} modificado. Atualizando o banco de vetores...")
            self.update_vector_store()

    def update_vector_store(self):
        # Carrega o novo PDF
        loader = PyPDFLoader(self.file_path)
        docs = loader.load()

        # Divide em chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        chunks = text_splitter.split_documents(documents=docs)

        # Limpa o banco de vetores existente
        self.vector_store.delete_collection()
        # Recria a coleção e adiciona os novos documentos
        self.vector_store = Chroma(
            embedding_function=HuggingFaceEmbeddings(),
            persist_directory=persist_directory,
        )
        self.vector_store.add_documents(documents=chunks)
        print("Banco de vetores atualizado com sucesso!")

def initialize_vector_store(file_path, persist_directory):
    # Carrega o PDF inicial
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = text_splitter.split_documents(documents=docs)

    # Inicializa o Chroma
    embedding = HuggingFaceEmbeddings()
    vector_store = Chroma(
        embedding_function=embedding,
        persist_directory=persist_directory,
    )
    vector_store.add_documents(documents=chunks)
    return vector_store

if __name__ == '__main__':
    file_path = '/app/rag/data/dados.pdf'
    persist_directory = '/app/chroma_data'

    vector_store = initialize_vector_store(file_path, persist_directory)
    print("Banco de vetores inicializado com sucesso!")
    
    event_handler = PDFHandler(vector_store, file_path)
    observer = Observer()
    observer.schedule(event_handler, path='/app/rag/data/', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()