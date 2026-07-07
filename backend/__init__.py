"""Backend package: LangGraph chatbot with tool-calling and MCP integration.

Public surface mirrors the original single-file backend so the frontend can
simply do `from backend import chatbot, retrieve_all_threads, submit_async_task`.
"""
from .async_runtime import run_async, submit_async_task
from .checkpointer import retrieve_all_threads
from .graph import chatbot

__all__ = ["chatbot", "retrieve_all_threads", "submit_async_task", "run_async"]
