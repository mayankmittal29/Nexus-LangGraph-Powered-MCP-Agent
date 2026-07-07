"""Streamlit app assembly: session init, sidebar, history, and chat input."""
import streamlit as st

from .chat import handle_user_input, render_history
from .session import init_session_state
from .sidebar import render_sidebar


def main():
    init_session_state()
    render_sidebar()
    render_history()

    user_input = st.chat_input("Type here")
    if user_input:
        handle_user_input(user_input)
