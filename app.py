import streamlit as st
from chatbot import model, db

st.set_page_config(
    page_title="College Admission AI",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 College Admission Assistant")
st.write("Ask me anything about admissions!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask your question..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    docs = db.similarity_search(prompt, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    final_prompt = f"""
You are a helpful College Admission Assistant.

Use ONLY the context below.

Context:
{context}

Question:
{prompt}

Answer:
"""

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = model.generate_text(prompt=final_prompt)
            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )