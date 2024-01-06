from openai import OpenAI
import json
# use .env file to store api keys 
from dotenv import load_dotenv
import os


def load_api_vars(): 
    # load_dotenv()  # This loads the variables from .env
    # #OPENAI_API_KEY=  os.getenv('OENAI_API_KEY')
    # #ORGANIZATION_ID =  os.getenv('ORGANIZATION_ID')
    OPENAI_API_KEY= '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'
    ORGANIZATION_ID = 'org-S4oTbd7zk3qfXLn5OvQbpTD3'
    client = OpenAI(api_key='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', organization='org-S4oTbd7zk3qfXLn5OvQbpTD3')
    return client 

def convert_statement(client, messages, max_tokens, model):
    print(f"Calling API with {model}")
    x = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=max_tokens,
        top_p=0,
        frequency_penalty=0.5,
        presence_penalty=0.5,
    )
    return x

def get_response_text(response):
    return response.choices[0].message.content


def run_api_call(prompt, model):
    max_tokens = 7000
    client = load_api_vars()
    response = convert_statement(client, prompt, max_tokens, model=model)
    content = get_response_text(response)
    return content 