import os
from langchain_community.document_loaders import PDFPlumberLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP

def load_and_split_documents(data_path=None):
    if data_path is None:
        data_path = DATA_PATH
    docs = []
    for file in os.listdir(data_path):
        path = os.path.join(data_path, file)
        if file.endswith(".txt"):
            docs.extend(TextLoader(path).load())
        elif file.endswith(".pdf"):
            docs.extend(PDFPlumberLoader(path).load())
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_documents(docs)