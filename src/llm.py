from langchain_groq import ChatGroq

from dotenv import load_dotenv

import os


# ---------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------

load_dotenv()


# ---------------------------------------------------
# GET LLM
# ---------------------------------------------------

def get_llm():

    llm = ChatGroq(

        groq_api_key=os.getenv(
            "GROQ_API_KEY"
        ),

        model_name="llama-3.1-8b-instant",

        temperature=0
    )

    return llm