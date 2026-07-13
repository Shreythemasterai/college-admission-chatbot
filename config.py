import os
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st

    IBM_API_KEY = st.secrets["IBM_API_KEY"]
    IBM_PROJECT_ID = st.secrets["IBM_PROJECT_ID"]
    IBM_URL = st.secrets["IBM_URL"]
    MODEL_ID = st.secrets["IBM_MODEL_ID"]

except Exception:
    IBM_API_KEY = os.getenv("IBM_API_KEY")
    IBM_PROJECT_ID = os.getenv("IBM_PROJECT_ID")
    IBM_URL = os.getenv("IBM_URL")
    MODEL_ID = os.getenv("IBM_MODEL_ID")