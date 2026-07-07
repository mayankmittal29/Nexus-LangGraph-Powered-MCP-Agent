"""LLM instantiation. Provider is selected via the LLM_PROVIDER env var."""
from langchain_openai import ChatOpenAI

from . import config


def get_llm():
    if config.LLM_PROVIDER == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(model=config.GEMINI_MODEL)
    return ChatOpenAI()


llm = get_llm()
