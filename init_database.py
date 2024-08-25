import argparse, os, shutil
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_chroma import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings

chroma_path_db = "chromaDB"
data_path = "data"



def get_embeddings():
    #embeddings = BedrockEmbeddings(
     #   credentials_profile_name = "default",region_name = "us-west-2"
    #)
    embeddings = OllamaEmbeddings(model = "llama3")
    return embeddings

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1500,
        chunk_overlap = 500,
        length_function = len,
        is_separator_regex= False,
    )
    return text_splitter.split_documents(documents)

def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id != last_page_id:
            current_chunk_index = 0
        else:
            current_chunk_index +=1

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id
    
    return chunks

def load_documents():
    document_loader = PyPDFDirectoryLoader(data_path)
    return document_loader.load()

def add_chroma_vectors(chunks: list[Document]):
    database = Chroma(
        persist_directory = chroma_path_db,embedding_function = get_embeddings()
    )

    chunks_with_ids = calculate_chunk_ids(chunks)

    existing_file = database.get(include=[])
    existing_ids = set(existing_file['ids'])
    print(f"Existing IDs: {len(existing_ids)}")

    new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]

    if len(new_chunks):
        new_chunks_ids = [chunk.metadata["id"] for chunk in new_chunks]
        database.add_documents(new_chunks, ids= new_chunks_ids)
        print(f"Adding {len(new_chunks)} new chunks")
    else:
        print("No new documents to add")
    
def clear_database():
    if os.path.exists(chroma_path_db):
        shutil.rmtree(chroma_path_db)

def init():
    documents = load_documents()
    chunks = split_documents(documents)
    add_chroma_vectors(chunks)