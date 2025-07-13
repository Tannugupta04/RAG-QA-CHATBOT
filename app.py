import streamlit as st
from rag_pipeline import setup_llm, load_vector_store, get_answer
import os

# --- Sidebar ---
st.sidebar.title("Navigation")
st.sidebar.markdown("""
- Ask a Question  
- Click FAQs to Autofill  
- Press 'Get Answer'
""")
st.sidebar.markdown("---")
st.sidebar.info("This chatbot answers questions about loan approval using a real dataset. You can type a question or click one below.")

# --- Load Vector DB and LLM ---
if 'vectordb' not in st.session_state:
    if os.path.exists("vectorstore/index.faiss"):
        st.session_state.vectordb = load_vector_store()
    else:
        st.warning("Vectorstore not found! Please run build_index.py first.")

if 'llm' not in st.session_state:
    st.session_state.llm = setup_llm()

if "query_text" not in st.session_state:
    st.session_state.query_text = ""

# --- Title & Instructions ---
st.title("Loan Approval Q&A Chatbot")
st.markdown("This chatbot uses document retrieval and AI to answer questions about loan approval data. Ask anything related to credit history, applicant status, or loan statistics.")

# --- Input Box ---
query = st.text_input(
    "Ask your question here:",
    value=st.session_state.query_text,
    key="search_box"
)
st.session_state.query_text = query

# --- Get Answer ---
if st.button("Get Answer"):
    if query.strip():
        answer = get_answer(query, st.session_state.vectordb, st.session_state.llm)
        st.subheader("Answer:")
        st.write(answer)

# --- FAQ Section ---
st.markdown("---")
st.subheader("FAQs (Click to autofill question box)")
st.markdown("Click a question below to autofill it above. Then press 'Get Answer'.")

faq_questions = [
    "How many loans were approved in total?",
    "What is the loan approval rate?",
    "How many applications were rejected?",
    "How does credit history affect loan approval?",
    
    "Is loan approval higher for graduates than non-graduates?",
    "What is the approval rate for self-employed applicants?",
    "How many applicants with a loan amount over 200K got approved?",
    "Which property area has the highest number of loan approvals?",
    "What is the approval rate in urban vs rural areas?",
    "Do high-income applicants get more approvals?",
    "What’s the average loan amount for approved applicants?",
    "What is the typical loan amount for those with dependents?",
    "How many applicants with Credit_History = 1 got their loan approved?",
    "Did applicants with 3+ dependents get approved more often?",
    "Are male or female applicants more likely to be approved?",
    "Does having a coapplicant affect approval chances?",
    "Compare approval rates between applicants with and without education.",
    "What are the patterns of loan approval for low-income groups?",
    "Give me 3 common reasons why a loan might be rejected.",
    "Who is more likely to get a loan approved: a graduate or not?"
]

# FAQ buttons
for i, faq in enumerate(faq_questions):
    if st.button(faq, key=f"faq_{i}"):
        st.session_state.query_text = faq
        st.rerun()
