import os
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st

os.environ['GOOGLE_API_KEY']='AIzaSyDvy0EEs7fCM1c_4D3h6CTlARt5LYGRw3o'

def generate_response(content):
    model = ChatGoogleGenerativeAI(model='gemini-pro')
    message = HumanMessage(content=content)
    response = model.stream([message])

    response_text = ''
    for chunk in response:
        response_text+=chunk.content

    return response_text

st.title('Chatbot Using Gemini API')
st.write('This is an assistive chatbot using Google Gemini Model')

if 'chat_history'  not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input('You: ')
if st.button('Send'):
    response = generate_response(user_input)

    st.session_state.chat_history.append(['You: ', user_input])
    st.session_state.chat_history.append(['Bot: ', response])
    user_input=''

if st.session_state.chat_history:
    for sender, msg in st.session_state.chat_history:
        st.write(f"{sender}: {msg}")



