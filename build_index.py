from rag_pipeline import setup_vector_store
from utils import preprocess_dataset

if __name__ == "__main__":
    documents = preprocess_dataset("data/Training Dataset.csv")
    setup_vector_store(documents)
    print("Vector DB created.")
