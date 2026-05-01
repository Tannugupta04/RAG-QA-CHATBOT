# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.llms import HuggingFacePipeline

# from transformers import pipeline
# from utils import preprocess_dataset

# import os
# from transformers import pipeline

# def setup_vector_store(documents):
#     embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#     vectordb = FAISS.from_texts(documents, embedding_model)
#     vectordb.save_local("vectorstore")
#     return vectordb

# def load_vector_store():
#     embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#     return FAISS.load_local("vectorstore", embedding_model, allow_dangerous_deserialization=True)

# # def setup_llm():
# #     pipe = pipeline("text2text-generation", model="google/flan-t5-base", max_length=256)
# #     return HuggingFacePipeline(pipeline=pipe)
# # In rag_pipeline.py
# # def setup_llm():
# #     pipe = pipeline("text2text-generation", model="google/flan-t5-small", max_length=128)
# #     return HuggingFacePipeline(pipeline=pipe)
# def setup_llm():
#     pipe = pipeline(
#         task="text2text-generation",
#         model="google/flan-t5-small",
#         tokenizer="google/flan-t5-small",
#         max_new_tokens=128
#     )
#     return pipe

# def get_answer(query, vectordb, llm):
#     docs = vectordb.similarity_search(query, k=3)

#     context = "\n\n".join([doc.page_content for doc in docs])

#     prompt = f"""
# You are a loan approval data assistant.

# Use only the given context.

# If the question is about CIBIL score, answer using Credit_History:
# Credit_History = 1 means good credit history.
# Credit_History = 0 means poor/no credit history.

# Question: {query}

# Context:
# {context}

# Give only one short final answer. Do not show records. Do not show JSON.

# Answer:
# """

#     response = llm(prompt)

#     if isinstance(response, list):
#         answer = response[0]["generated_text"]
#     else:
#         answer = str(response)

#     return answer.strip()
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
<<<<<<< HEAD
=======
from langchain_community.llms import HuggingFacePipeline

>>>>>>> 273e7facd395a04a475fd6e57006a362bb34ec1a
from transformers import pipeline
import pandas as pd


def setup_vector_store(documents):
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = FAISS.from_texts(documents, embedding_model)
    vectordb.save_local("vectorstore")
    return vectordb


def load_vector_store():
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.load_local(
        "vectorstore",
        embedding_model,
        allow_dangerous_deserialization=True
    )


def setup_llm():
    pipe = pipeline(
        task="text2text-generation",
        model="google/flan-t5-small",
        tokenizer="google/flan-t5-small",
        max_new_tokens=80
    )
    return pipe


def get_answer(query, vectordb, llm, df=None):
    q = query.lower()

    # Exact answers using Pandas
    if df is not None and "Loan_Status" in df.columns:
        df = df.copy()

        if "LoanAmount" in df.columns:
            df["LoanAmount"] = pd.to_numeric(df["LoanAmount"], errors="coerce")

        if "ApplicantIncome" in df.columns:
            df["ApplicantIncome"] = pd.to_numeric(df["ApplicantIncome"], errors="coerce")

        total = len(df)
        approved = (df["Loan_Status"] == "Y").sum()
        rejected = (df["Loan_Status"] == "N").sum()

        if "how many loans were approved" in q or "total approved" in q:
            return f"Total approved loans are {approved}."

        if "how many applications were rejected" in q or "total rejected" in q:
            return f"Total rejected loan applications are {rejected}."

        if "approval rate" in q and "urban" not in q and "rural" not in q:
            rate = (approved / total) * 100
            return f"The overall loan approval rate is {rate:.2f}%."

        if "cibil" in q:
            return (
                "This dataset does not contain an exact CIBIL score column. "
                "It uses Credit_History instead, where 1 means good credit history "
                "and 0 means poor or no credit history."
            )

        if "credit history" in q and "affect" in q:
            if "Credit_History" in df.columns:
                grouped = df.groupby("Credit_History")["Loan_Status"].value_counts().unstack().fillna(0)
                return (
                    "Credit history strongly affects loan approval. "
                    "Applicants with Credit_History = 1 have much higher approval chances, "
                    "while applicants with Credit_History = 0 are mostly rejected."
                )

        if "credit_history = 1" in q or "credit history = 1" in q:
            if "Credit_History" in df.columns:
                count = df[
                    (df["Credit_History"] == 1) &
                    (df["Loan_Status"] == "Y")
                ].shape[0]
                return f"{count} applicants with Credit_History = 1 got their loan approved."

        if "average loan amount" in q and "approved" in q:
            if "LoanAmount" in df.columns:
                avg = df[df["Loan_Status"] == "Y"]["LoanAmount"].mean()
                return f"The average loan amount for approved applicants is {avg:.2f}."

        if "loan amount over 200" in q or "loan amount over 200k" in q:
            if "LoanAmount" in df.columns:
                count = df[
                    (df["LoanAmount"] > 200) &
                    (df["Loan_Status"] == "Y")
                ].shape[0]
                return f"{count} applicants with loan amount over 200K got approved."

        if "property area" in q and "highest" in q:
            if "Property_Area" in df.columns:
                area_counts = df[df["Loan_Status"] == "Y"]["Property_Area"].value_counts()
                top_area = area_counts.idxmax()
                top_count = area_counts.max()
                return f"{top_area} property area has the highest number of loan approvals with {top_count} approvals."

        if "self-employed" in q or "self employed" in q:
            if "Self_Employed" in df.columns:
                temp = df[df["Self_Employed"] == "Yes"]
                if len(temp) > 0:
                    rate = (temp["Loan_Status"] == "Y").sum() / len(temp) * 100
                    return f"The approval rate for self-employed applicants is {rate:.2f}%."

        if "graduate" in q and "non-graduate" in q:
            if "Education" in df.columns:
                grad = df[df["Education"] == "Graduate"]
                nongrad = df[df["Education"] == "Not Graduate"]

                grad_rate = (grad["Loan_Status"] == "Y").sum() / len(grad) * 100
                nongrad_rate = (nongrad["Loan_Status"] == "Y").sum() / len(nongrad) * 100

                return (
                    f"Graduates have an approval rate of {grad_rate:.2f}%, "
                    f"while non-graduates have an approval rate of {nongrad_rate:.2f}%."
                )

        if "male" in q and "female" in q:
            if "Gender" in df.columns:
                male = df[df["Gender"] == "Male"]
                female = df[df["Gender"] == "Female"]

                male_rate = (male["Loan_Status"] == "Y").sum() / len(male) * 100
                female_rate = (female["Loan_Status"] == "Y").sum() / len(female) * 100

                return (
                    f"Male applicants have an approval rate of {male_rate:.2f}%, "
                    f"while female applicants have an approval rate of {female_rate:.2f}%."
                )

    # RAG fallback
    docs = vectordb.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a loan approval data assistant.

Use only the context below.
Give one short direct answer.
Do not show records.
Do not show JSON.
Do not give unnecessary bullet points.

Context:
{context}

Question:
{query}

Answer:
"""

    response = llm(prompt)

    if isinstance(response, list) and len(response) > 0:
        answer = response[0].get("generated_text", "")
    else:
        answer = str(response)

    return answer.strip()