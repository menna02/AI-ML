import os 
from groq import Groq # type: ignore


os.environ['GROQ_API_KEY']= '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'

client = Groq()
chat_history = []

def generate_response(content):
    chat_history.append({'role':'user', 'content':content})
    messages = [{'role':'system', 'content':'You are a helpful assistant'}, *chat_history]

    response = client.chat.completions.create(
        model= 'llama-3.1-8b-instant',
        messages= messages
    )

    assistant_response = response.choices[0].message.content

    chat_history.append({'role':'assistant', 'content':assistant_response})
    print(f'Chatbot: {assistant_response}')

if __name__=='__main__':
    while True:
        user_input = input('You: ')
        if user_input.lower()=='exit':
            print('Chatbot: Bye!')
            break
        generate_response(user_input)