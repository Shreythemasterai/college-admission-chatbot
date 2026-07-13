from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai import Credentials

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from config import *

# IBM Credentials
credentials = Credentials(
    url=IBM_URL,
    api_key=IBM_API_KEY
)

# Model Parameters
parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 1024,
    "min_new_tokens": 200,
    "temperature": 0.1,
    "repetition_penalty": 1.05
}

# IBM Model
model = Model(
    model_id=MODEL_ID,
    credentials=credentials,
    project_id=IBM_PROJECT_ID,
    params=parameters
)

# Embedding Model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS Database
db = FAISS.load_local(
    "vector_db",
    embeddings,
    allow_dangerous_deserialization=True
)

# Retriever
retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 20,
        "fetch_k": 40
    }
)

# Terminal Chatbot
if __name__ == "__main__":

    print("=" * 60)
    print("🎓 College Admission AI Assistant")
    print("=" * 60)

    while True:

        question = input("\nYou: ")

        if question.lower() == "exit":
            break

        docs = retriever.invoke(question)

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        final_prompt = f"""
You are an expert College Admission AI Assistant.

Answer ONLY using the information below.

Rules:
- Give detailed answers.
- Use headings.
- Use bullet points.
- Never skip information.
- If comparing colleges, create a markdown table.
- Mention:
  * Eligibility
  * Cutoff
  * Fee Structure
  * Courses
  * Internship
  * Average Package
  * Highest Package
  * Recruiters

Context:
{context}

Question:
{question}

Detailed Answer:
"""

        answer = model.generate_text(
            prompt=final_prompt
        )

        print("\nBot:\n")
        print(answer)