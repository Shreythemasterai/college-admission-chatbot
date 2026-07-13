import streamlit as st
from chatbot import model, retriever

st.set_page_config(
    page_title="College Admission AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 College Admission AI Assistant")
st.write("Ask anything about Engineering Admissions.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask your question...")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    docs = retriever.invoke(prompt)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    final_prompt = f"""
You are an expert Engineering College Admission Assistant.

Answer ONLY from the context below.

Instructions:

- Give the complete answer.
- Do not summarize.
- Include every relevant detail.
- Use bullet points.
- Use headings.
- If the question is about a college include:
    • Eligibility
    • Cutoff
    • Fees
    • Courses
    • Internship
    • Average Package
    • Highest Package
    • Recruiters
- If comparing colleges, make a markdown table.
- If information is unavailable, clearly say so.

Context:
{context}

Question:
{prompt}

Detailed Answer:
"""

    with st.chat_message("assistant"):

        with st.spinner("Searching..."):

            answer = model.generate_text(
                prompt=final_prompt
            )

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )