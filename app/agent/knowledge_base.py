import sys
import os

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

project_root = "."

def init_knowledge():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

def create_knowledge_base(file_paths):
    """Loads documents from given paths and creates a FAISS vector store.""" 
    all_docs = []
    for path in file_paths:
        full_path = os.path.join(project_root, path)
        if os.path.exists(full_path):
            loader = TextLoader(full_path)
            docs = loader.load()
            for doc in docs:
                doc.metadata={"source": path} # Add source metadata
            all_docs.extend(docs)
        else:
            print(f"Warning: Artifact not found at {full_path}")

    if not all_docs:
        print("No documents found to create knowledge base.")
        return None

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(all_docs)
    
    print(f"Creating vector store from {len(splits)} document splits...")
    vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    return vectorstore.as_retriever()