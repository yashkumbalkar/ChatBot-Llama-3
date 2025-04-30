import os
import json
import streamlit as st
from groq import Groq


# streamlit page configuration
st.set_page_config(
    page_title="LLAMA 3.1. Chat",
    page_icon="💬",
    layout="centered"
)


GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# save the api key to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# initialize the chat history as streamlit session state of not present already
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# streamlit page title
st.title("🦙 LLAMA 3.1. ChatBot")

# Instruction below the title
st.markdown("_Type `'exit'` or `'quit'` to end the chat._")

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Check if chat has ended
if st.session_state.get("chat_ended"):
    st.info("Chat ended. Please refresh the page to start over.")
    st.stop()


# input field for user's message:
user_prompt = st.chat_input("Ask Anything...")

if user_prompt:

    if user_prompt.lower().strip() in {"exit", "quit"}:
      st.session_state.chat_ended = True
      st.info("Chat ended. Please refresh the page to start over.")
      st.stop()

    with st.chat_message("user"):
      st.markdown(user_prompt)

    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # sends user's message to the LLM and get a response
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # display the LLM's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

