from flask import Flask, request,make_response,render_template, jsonify
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import os 
from langchain.prompts import MessagesPlaceholder
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
import time
import threading
import requests
import json

import time
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from hugchat import hugchat
from streamlit_oauth import OAuth2Component
import base64
import random

os.environ['OPENAI_API_KEY']="sk-111111111111111111111111111111111111111111111111"
os.environ['OPENAI_API_BASE']="http://127.0.0.1:5000/v1"
import openai



embeddings = OpenAIEmbeddings()
instance = Chroma(persist_directory="/Users/j_fel/Desktop/ProfileLLM/db", embedding_function=embeddings)



tech_template = """"You are Juan Felix Pangestu, University Student who is studying at Hong Kong Baptist University. You are majoring in Business Computing Data Analytics which you are a second year currently. You are an Chinese-Indonesian Ethnic Minority in Hong Kong, where you studied at Rosaryhill Secondary School, an English medium DSE curriculum secondary school. Your Cantonese proficiency is low but your English proficiency is at a native level.




{context} 

Q: {question}
A: """
PROMPT = PromptTemplate(
    template=tech_template, input_variables=["context", "question"]
)



qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(model_name="x", temperature=0.5 ,max_tokens=2048),
                                                chain_type="stuff",
                                                retriever=instance.as_retriever(),
                                                chain_type_kwargs={"prompt": PROMPT})

def get_response(user_input):


    result = qa({"query": prompt})
    response = f"{result['result']}"

    return response


def getGreet():
    greeting = random.choice(
        [
            "Hi, I'm Felix, ask me away!",
            "What do you think about me?",
            "What can I tell you to make you give me a job?",
        ]
    )
    return greeting

#Frontend


st.set_page_config(page_title="JFP Bot")
st.title("Personal Bot - Juan Felix Pangestu")

    
if st.button("Reset",use_container_width=True):
    st.session_state.messages = [{"role": "assistant", "content": getGreet()}]
    st.rerun()
# Initialize chat history
    


if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": getGreet()}]

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

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = get_response(prompt)
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    

