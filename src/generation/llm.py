from langchain_groq import ChatGroq

from dotenv import load_dotenv

import streamlit as st
import os


# ---------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------

load_dotenv()


# ---------------------------------------------------
# GET API KEY
# ---------------------------------------------------

try:

    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

except:

    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY"
    )


# ---------------------------------------------------
# GET LLM
# ---------------------------------------------------

def get_llm():

    llm = ChatGroq(

        groq_api_key=GROQ_API_KEY,

        model_name="llama-3.1-8b-instant",

        temperature=0
    )

    return llm