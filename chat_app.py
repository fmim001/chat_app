import streamlit as st
import numpy as np
import random

import datarobot as dr
from datarobot.models.genai.vector_database import VectorDatabase
from datarobot.models.genai.vector_database import ChunkingParameters
from datarobot.enums import PromptType
from datarobot.enums import VectorDatabaseEmbeddingModel
from datarobot.enums import VectorDatabaseChunkingMethod
from datarobot.models.genai.playground import Playground
from datarobot.models.genai.llm import LLMDefinition
from datarobot.models.genai.llm_blueprint import LLMBlueprint
from datarobot.models.genai.llm_blueprint import VectorDatabaseSettings
from datarobot.models.genai.chat import Chat
from datarobot.models.genai.chat_prompt import ChatPrompt
from datarobot.models.genai.vector_database import CustomModelVectorDatabaseValidation
from datarobot.models.genai.comparison_chat import ComparisonChat
from datarobot.models.genai.comparison_prompt import ComparisonPrompt
from datarobot.models.genai.custom_model_llm_validation import CustomModelLLMValidation


endpoint="https://app.datarobot.com/api/v2"
token="NjZkNjZmZGFhMjMxYzc4ZGMxMGIxOGRlOkRuT082UlFpem1FL3p3Rm1ybUt4Q0xrTUVSUTNVQWpCd3k2RlpHUCthb2M9"
dr.Client(endpoint=endpoint, token=token)

def get_llm_response(chat_id,input_text):
    chat = Chat.get(chat_id)
    prompt1 = ChatPrompt.create(
        chat=chat,
        text=input_text,
        wait_for_completion=True,
    )
    return prompt1.result_text

st.title("ChatGPT-like clone")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["chat_id"] = "66fe0da2f45d3cc89e411613"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = get_llm_response(
            chat_id=st.session_state["chat_id"],
            input_text=prompt
        )
        st.write(stream)
    st.session_state.messages.append({"role": "assistant", "content": stream})