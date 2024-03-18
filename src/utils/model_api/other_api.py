import dotenv
from llamaapi import LlamaAPI
import json
import os
import anthropic
import genai
import re  # For regular expressions

def get_llama_api_vars():
    """
    Load llama api token and return llama object
    """
    dotenv.load_dotenv()
    return LlamaAPI(os.getenv('LLAMA_API_TOKEN'))

def call_llama(int_prompt_first, model):
    """
    Convert a prompt to a llama api response
    """
    api_request_json = {
        "model": model,
        "messages": [
            int_prompt_first[0],
            int_prompt_first[1],
        ],
        'temperature': 0,
        'max_tokens': 10
    }
    llama = get_llama_api_vars()
    print(api_request_json)
    response = llama.run(api_request_json)
    print(json.dumps(response.json(), indent=2))
    output = response.json()['choices'][0]['message']['content']
    return output

def get_claude_api_vars():
    """
    Load Claude API token and return Anthropic client object
    """
    dotenv.load_dotenv()
    api_key = os.getenv('CLAUDE_API_KEY')
    return anthropic.Client(api_key=api_key)

def call_claude(int_prompt_first, model):
    """
    Convert a prompt to a Claude API response
    """
    client = get_claude_api_vars()
    formatted_prompt = (
        "Human: " + int_prompt_first[0]['content'] + '\n\n' +
        "Human: " + int_prompt_first[1]['content'] + '\n\n' +
        "Assistant:"
    )
    response = client.completions.create(
        model=model,
        prompt=formatted_prompt,
        max_tokens_to_sample=10,
        temperature=0,
    )
    output = response.completion
    return output
