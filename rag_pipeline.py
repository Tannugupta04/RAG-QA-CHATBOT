from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFacePipeline
from transformers import pipeline
from utils import preprocess_dataset

import os

def setup_vector_store(documents):
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = FAISS.from_texts(documents, embedding_model)
    vectordb.save_local("vectorstore")
    return vectordb

def load_vector_store():
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.load_local("vectorstore", embedding_model, allow_dangerous_deserialization=True)

# def setup_llm():
#     pipe = pipeline("text2text-generation", model="google/flan-t5-base", max_length=256)
#     return HuggingFacePipeline(pipeline=pipe)
# In rag_pipeline.py
def setup_llm():
    pipe = pipeline("text2text-generation", model="google/flan-t5-small", max_length=128)
    return HuggingFacePipeline(pipeline=pipe)

def get_answer(query, vectordb, llm):
    # docs = vectordb.similarity_search(query, k=5)
    docs = vectordb.similarity_search(query, k=3)  # Reduce from 5 to 3 or even 2

    context = "\n\n".join([doc.page_content for doc in docs])
    
    prompt = f"""You are a data expert analyzing loan approval data.

Context data:
{context}

Now, based on the above data, answer the following question clearly with insights:

Question: {query}
Answer:"""

    return llm(prompt)
