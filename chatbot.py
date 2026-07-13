from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai import Credentials

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from config import *

credentials = Credentials(
    url=IBM_URL,
    api_key=IBM_API_KEY
)

model = Model(
    model_id=MODEL_ID,
    credentials=credentials,
    project_id=IBM_PROJECT_ID
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "vector_db",
    embeddings,
    allow_dangerous_deserialization=True
)

if __name__ == "__main__":
    print("College Admission Chatbot")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            break

        docs = db.similarity_search(question, k=6)
        context = "\n".join([doc.page_content for doc in docs])

        prompt = f"""
You are a College Admission Assistant.

Use ONLY the information below.

Context:
{context}

Question:
{question}

Answer:
"""

        response = model.generate_text(prompt=prompt)

        print("\nBot:", response)
        print()