"""Streamlit session-state helpers: thread bookkeeping and history loading."""
import uuid

import streamlit as st

from backend import chatbot, retrieve_all_threads


def generate_thread_id():
    return uuid.uuid4()


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []


def load_conversation(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get("messages", [])


def init_session_state():
    if "message_history" not in st.session_state:
        st.session_state["message_history"] = []

    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = generate_thread_id()

    if "chat_threads" not in st.session_state:
        st.session_state["chat_threads"] = retrieve_all_threads()

    add_thread(st.session_state["thread_id"])
