Link ToApp(https://rag-app-chatbot-apt6padceu6vygjttd4pyy.streamlit.app/)

# Loan Approval Q&A Chatbot (RAG-based)

This project is a **Retrieval-Augmented Generation (RAG)** based chatbot that answers user queries about loan approvals. It uses a structured dataset (`Training Dataset.csv` from Kaggle) to build a document store, retrieve relevant chunks using semantic search (FAISS), and generate intelligent answers using a language model (LLM).

---

##  Features

-  **RAG-based Q&A**: Retrieves and answers questions from structured CSV data using vector similarity + LLMs
-  **Ask Any Question**: Type a question or select from FAQ dropdown
- **Built-in FAQs**: Autofill questions to guide users
-  **Finance-focused**: Built using a loan approval prediction dataset
- **Streamlit UI**: Clean, modern interface for interaction

---

## Project Structure

RAG_Loan_chatbot/
│
├── app.py # Main Streamlit app (UI + logic)

├── rag_pipeline.py # RAG functions (LLM setup, retrieval, answer generation)

├── utils.py # Preprocessing functions for the dataset

├── build_index.py # Script to build the FAISS vector index from CSV

├── requirements.txt # All required Python libraries

├── vectorstore/ # Folder to store the FAISS index files

│ └── index.faiss # The FAISS vector index (created after building)

├── data/

│ └── Training Dataset.csv # Loan dataset from Kaggle

└── README.md # You're reading it!




---

## 📥 Dataset

Download the dataset from Kaggle:

**Kaggle URL:**  
[Loan Approval Dataset](https://www.kaggle.com/datasets/sonalisingh1411/loan-approval-prediction)



## 📂 Dataset Overview

This project uses the **Loan Approval Prediction** dataset from Kaggle to enable retrieval-augmented Q&A about home loan approvals.

### 📌 Source:
- **Kaggle URL**: [Loan Approval Prediction Dataset](https://www.kaggle.com/datasets/sonalisingh1411/loan-approval-prediction)
- **File Used**: `Training Dataset.csv`

---

###  Dataset Description

The dataset contains **loan application records** submitted by various individuals. Each row represents a unique applicant and includes demographic, financial, and credit-related information, along with the **loan approval decision**.

---

###  Key Features

| Column Name         | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `Loan_ID`           | Unique identifier for the loan application                                  |
| `Gender`            | Gender of the applicant (`Male`/`Female`)                                  |
| `Married`           | Marital status of the applicant (`Yes`/`No`)                               |
| `Dependents`        | Number of dependents                                                        |
| `Education`         | Education level (`Graduate`/`Not Graduate`)                                 |
| `Self_Employed`     | Employment status (`Yes`/`No`)                                              |
| `ApplicantIncome`   | Income of the applicant                                                     |
| `CoapplicantIncome` | Income of the co-applicant (if any)                                         |
| `LoanAmount`        | Loan amount requested (in thousands)                                        |
| `Loan_Amount_Term`  | Term of loan in months                                                      |
| `Credit_History`    | Credit history (1 = good, 0 = bad/no record)                                |
| `Property_Area`     | Area of property (`Urban`, `Semiurban`, `Rural`)                            |
| `Loan_Status`       | Loan approval status (`Y` = Approved, `N` = Rejected)                       |

---

###  Usage in Chatbot

The chatbot is powered by a **RAG (Retrieval-Augmented Generation)** pipeline that:

-  Converts the dataset into natural language "documents"
-  Stores them in a **vector database** using FAISS
   Retrieves relevant records based on user queries
-  Uses an LLM to generate human-like answers grounded in the dataset

This allows users to ask questions like:
- *"How many loans were approved in total?"*
- *"Do graduates get approved more than non-graduates?"*
- *"What is the approval rate in urban areas?"*

---

###  Note

This dataset is meant for educational and demonstration purposes only.


---

###  `app.py`

This is the **main Streamlit application** file. It handles the **user interface** and links user input to the RAG backend logic.

**Key Features:**
- Text input for asking questions
- FAQ dropdown with auto-fill functionality
- Button to trigger the RAG pipeline
- Loads the LLM and Vector DB once at app startup

---

###  `rag_pipeline.py`

This file contains the **core RAG logic** for:
- **LLM Setup**: Defines which large language model to use (e.g., OpenAI, Claude, Mistral)
- **Vector Store Loading**: Loads the FAISS index and embedding model
- **Answer Generation**: Retrieves relevant chunks and generates a context-aware response using the LLM

**Main Functions:**
- `setup_llm()`: Initialize the language model
- `load_vector_store()`: Load FAISS index with embeddings
- `get_answer(query, vectordb, llm)`: Executes the full RAG process (retrieval + generation)

---

###  `utils.py`

This file contains **helper functions** for processing the dataset into a format suitable for vector embedding and retrieval.

**Main Function:**
- `preprocess_dataset(file_path)`: 
  - Reads the CSV
  - Converts each row into a descriptive, human-readable "document"
  - Returns a list of such document strings to be embedded

---

###  `build_index.py`

A **setup script** that should be run once to create the vector store.

**What it does:**
- Loads the dataset using `utils.py`
- Converts rows to documents
- Generates embeddings (e.g., using OpenAI or Hugging Face)
- Stores them in a FAISS vector database under `vectorstore/index.faiss`

**Run it like this:**
```bash
python build_index.py



### `vectorstore/index.faiss`

After running `build_index.py`, this folder will be automatically created and will contain the following files:

- **`index.faiss`**  
  This is the **FAISS vector index file** that stores the high-dimensional embeddings of your preprocessed loan documents. It's used for **fast similarity search** when a user asks a question.

- **`index.pkl`** *(if generated)*  
  This optional file contains metadata (e.g., document IDs, text references) used to **reconstruct the original documents** during retrieval.

⚠ **Do not edit these files manually.**  
They are automatically generated and loaded by `rag_pipeline.py` when answering questions via the chatbot.


## 🖼 Screenshots

###  Home Page with Chat Interface
![Home Page](
<img width="2536" height="1626" alt="Screenshot 2025-07-13 194510" src="https://github.com/user-attachments/assets/2b7df819-9980-467b-9f36-7e10b0861110" />)


---

###  FAQ Section (Click to Autofill)
![FAQ Section](<img width="1248" height="1456" alt="Screenshot 2025-07-13 194521" src="https://github.com/user-attachments/assets/8274c091-1305-4460-95ae-b1f3207e5edd" />
)

---

###  Answer Display after Query
![Answer Result](<img width="1620" height="992" alt="answwer png" src="https://github.com/user-attachments/assets/20d48d65-d6be-4b3f-bf0e-3fec27534967" />
)



