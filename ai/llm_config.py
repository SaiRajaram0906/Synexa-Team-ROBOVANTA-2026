from langchain_google_genai import ChatGoogleGenerativeAI
import os

def get_gemini_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7
    )
