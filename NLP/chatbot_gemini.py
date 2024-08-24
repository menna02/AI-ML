import os
import json
from langchain_core.messages  import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ['GOOGLE_API_KEY']='AIzaSyDvy0EEs7fCM1c_4D3h6CTlARt5LYGRw3o'

def generate_response(content, model_name='gemini-pro'):
    model = ChatGoogleGenerativeAI(model= model_name)
    message = HumanMessage(content= content)
    response = model.stream([message])

    for chunk in response:
        print(f'Chatbot:{chunk.content}')

if __name__ == '__main__':
    while True:
        user_input = input('You: ')
        if user_input.lower()=='exit':
            print('Chatbot: Bye!')
            break
        else:
            generate_response(user_input)