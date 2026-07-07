"""Sidebar UI: new-chat button and conversation history list."""
import streamlit as st
from langchain_core.messages import HumanMessage

from .session import load_conversation, reset_chat


def render_sidebar():
    st.sidebar.title("LangGraph MCP Chatbot")

    if st.sidebar.button("New Chat"):
        reset_chat()

    st.sidebar.header("My Conversations")
    for thread_id in st.session_state["chat_threads"][::-1]:
        if st.sidebar.button(str(thread_id)):
            st.session_state["thread_id"] = thread_id
            messages = load_conversation(thread_id)

            temp_messages = []
            for msg in messages:
                role = "user" if isinstance(msg, HumanMessage) else "assistant"
                temp_messages.append({"role": role, "content": msg.content})
            st.session_state["message_history"] = temp_messages
