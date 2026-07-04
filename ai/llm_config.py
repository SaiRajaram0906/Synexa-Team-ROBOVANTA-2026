import os
from langchain_google_genai import ChatGoogleGenerativeAI
from tenacity import retry, wait_exponential, stop_after_attempt

# Shared Configuration for all Agents
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 4096
LLM_TIMEOUT = 60

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def get_gemini_llm():
    api_key = os.environ.get("GOOGLE_API_KEY", "dummy_key_for_testing")
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro-latest",
        temperature=LLM_TEMPERATURE,
        max_output_tokens=LLM_MAX_TOKENS,
        timeout=LLM_TIMEOUT,
        google_api_key=api_key
    )
