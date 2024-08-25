from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langchain_community.embeddings.ollama import OllamaEmbeddings

chroma_path_db = "chromaDB"

Prompt_template = """
Answer the question based only on the following context:
{context}

Answer the question based on the above context: {question}
"""

def get_embeddings():
    #embeddings = BedrockEmbeddings(
     #   credentials_profile_name = "default",region_name = "us-west-2"
    #)
    embeddings = OllamaEmbeddings(model = "llama3")
    return embeddings

def query_rag(query_text):
    database = Chroma(persist_directory=chroma_path_db, embedding_function=get_embeddings())

    results = database.similarity_search_with_score(query_text,k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt = ChatPromptTemplate.from_template(Prompt_template)
    prompt = prompt.format(context=context_text, question=query_text)

    model = OllamaLLM(model='llama3')
    result = model.invoke(prompt)
    return result, context_text
