# Example: reuse your existing OpenAI setup
import time
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from hugchat import hugchat
import os
os.environ['OPENAI_API_KEY']="sk-111111111111111111111111111111111111111111111111"
os.environ['OPENAI_API_BASE']="http://127.0.0.1:5000/v1"
import openai

prompt = """You are Juan Felix Pangestu, University Student who is studying at Hong Kong Baptist University. You are majoring in Business Computing Data Analytics which you are a second year currently. You are an Chinese-Indonesian Ethnic Minority in Hong Kong, where you studied at Rosaryhill Secondary School, an English medium DSE curriculum secondary school. Your Cantonese proficiency is low but your English proficiency is at a native level.

You have done the International Innovation Graduate Project Hackathon by HSBC where you placed in a finalist position and placed a Semi-finalist position at the Hong Kong Undergraduate Financial Planner of the Year Award hosted by Society of Registered Financial Planners.

For interests, you are currently on the HKBU Rugby Team which you actively participate. Additionally you have an interest in English Debate which you did a lot in your secondary school.

Your skills include:
Languages: Java, Python, SQL, C, R, HTML, CSS, Javascript
Technologies: Adobe Photoshop, Blender, Microsoft 365, Odoo, Tableau
General: Product Management, Business Development, Marketing, Client Services

You have a certification from Google for Google Data Analytics and from KPMG for KPMG AU Data Analytics"""

history = [
    {"role": "system", "content": prompt},
    
]

st.set_page_config(page_title="Admazes")


hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)


input_container = st.container()
colored_header(label='', description='', color_name='red-30')
response_container = st.container()

def get_input():
    input_text = st.text_input("You: ", "", key="input")
    return input_text
## Applying the user input box
with input_container:
    user_input = get_input()



def get_response(user_input):

    history.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
    model="x",
    messages=history,
    temperature=0.5,
    max_tokens=2048
    
    )
    history.append(response)
    text = response['choices'][0]['message']['content']
    return text

if 'bot_response' not in st.session_state:
    st.session_state['bot_response'] = ["I'm Admazes Bot, tell me how I can help you"]
## user_input stores User's questions
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ['Hi!']

with response_container:
    if user_input:
        result = get_response(user_input)
        response = result

        st.session_state.user_input.append(user_input)
        st.session_state.bot_response.append(response)
        
    if st.session_state['bot_response']:
        for i in range(len(st.session_state['bot_response'])):
            message(st.session_state['user_input'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state['bot_response'][i], key=str(i))