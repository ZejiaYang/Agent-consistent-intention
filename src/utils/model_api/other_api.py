import dotenv 
from llamaapi import LlamaAPI
import json
import os

def get_llama_api_vars():
    """ 
    Load llama api token and return llama object
    """
    dotenv.load_dotenv()
    return LlamaAPI(os.getenv('LLAMA_API_TOKEN') )


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
                        'temperature': 0 ,
                        'max_tokens':10
                        }
    llama = get_llama_api_vars()
    print(api_request_json)
    response = llama.run(api_request_json)
    print(json.dumps(response.json(), indent=2))
    output= response.json()['choices'][0]['message']['content']
    return output 


