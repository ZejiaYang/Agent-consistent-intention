import sys
import os
from pathlib import Path
import json 
import os
import glob 
import ast 
import re
import argparse


# Adding the 'src' and 'src/utils' directories to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
utils_dir = os.path.join(src_dir, 'utils')
sys.path.append(src_dir)
sys.path.append(utils_dir)

from utils import load_data, json_arr_to_file, run_api_call
from utils import  intention_prompt_first, intention_prompt_second , preprocess_options_and_labels, intention_prompt_second_llama
from utils import call_llama 



gpt_models = [
    'gpt-4-turbo-preview',
    'gpt-4',
    'gpt-3.5-turbo']

gpt_base_modesl = [
    'davinci-002',
    'babbage-002' 
]

llama_model_family = [
    "llama-7b-chat",
    "llama-7b-32k",
    "llama-13b-chat",
    "llama-70b-chat" ]
other_models = [
    "mixtral-8x7b-instruct",
    "mistral-7b-instruct",
    "mistral-7b-instruct-v0.1",  # Adjusted based on the note for v0.1
    "mistral-7b-v0.1",  # Adjusted based on the note for v0.1
    "NousResearch/Nous-Hermes-Llama2-13b",
    "falcon-7b-instruct",
    "falcon-40b-instruct",
    "alpaca-7b",
    "codellama-7b-instruct",
    "codellama-13b-instruct",
    "codellama-34b-instruct",
    "openassistant-llama2-70b",
    "vicuna-7b",
    "vicuna-13b",
    "vicuna-13b-16k"
]


def extract_numbers_in_range(text, lower=1, upper=5, base=False):
    # This pattern will match whole numbers in the text
    pattern = r'\b[1-5]\b'
    
    # Find all matches in the text
    matches = re.findall(pattern, text)
    
    # Convert matched strings to integers
    numbers = [int(match) for match in matches if lower <= int(match) <= upper]
    if not base and len(numbers) != 1:
        # raise ValueError('More than one answer received.')
        print('More than one answer found')
        return None 
    return numbers[0] 


def process_one_file(file , write_path , max_tokens, model  ):
    """
    Function to process one file in the dataset directory
    Inputs:
    file: str, path to the file to process
    write_path: str, path to the desired output file 
    """
    full_json = load_data(file)

    for item in full_json: 
        # Extracting data from JSON item
        op = item['options']
        lab = item['labels']
        scenario = item['scenario']
        adapt_outcome = ast.literal_eval(str(item['adapt_response'].replace("'s", 'es')))
        
        print('Adapt outcome list:\n', adapt_outcome)
        
        # Checking adapt outcome length
        if len(adapt_outcome) != len(op):
            raise Exception('Number of options and number of adapt outcomes do not match')
        if len(adapt_outcome) != 5: 
            raise Exception('Wrong number of adapt outcomes')
        
        # Preprocessing options and labels
        mapping, pr_string = preprocess_options_and_labels(op, lab, adapt_outcome)
        item['mapping_given_to_model'] = mapping 

        # Generating and running prompts
        first_prompt = intention_prompt_first(scenario, pr_string)
        
        if model in gpt_models:
            first_response = run_api_call(first_prompt, model, max_tokens)
        elif model in gpt_base_modesl:
            first_response = run_api_call(first_prompt, model, max_tokens, base=True)
        elif model in llama_model_family:
            first_response = call_llama(first_prompt, model)
        
        # Extracting numbers from the first response
        if model not in gpt_base_modesl:
            numeric_first_response = extract_numbers_in_range(first_response)
        else:
            numeric_first_response = extract_numbers_in_range(first_response, base=True)
        
        item['first response'] = numeric_first_response if numeric_first_response is not None else first_response
        print(item['first response'])
        if numeric_first_response is None:
            # Skip to the next item if first response is invalid
            item['second response'] = 'Invalid first response'
            continue 
        
        # Generating and running second prompts
        adapt_sentence = mapping[numeric_first_response]['adapt_outcome']
        
        if model in gpt_models + gpt_base_modesl:
            second_prompt = intention_prompt_second(scenario, pr_string, adapt_sentence)
        elif model in llama_model_family:
            second_prompt = intention_prompt_second_llama(scenario, pr_string, adapt_sentence)
        
        if model in gpt_models:
            second_response = run_api_call(second_prompt, model, max_tokens)
        elif model in gpt_base_modesl:
            second_response = run_api_call(second_prompt, model, max_tokens, base=True)
        elif model in llama_model_family:
            second_response = call_llama(second_prompt, model)
        
        if model not in gpt_base_modesl:
            numeric_second_response = extract_numbers_in_range(second_response)
        else:
            numeric_second_response = extract_numbers_in_range(second_response, base=True)
        
        item['second response'] = numeric_second_response if numeric_second_response is not None else second_response
        print(item['second response'])

    print(f'Starting to save file {file}')
    json_arr_to_file(full_json, write_path, indent=4)
    print('File saved. \n')


def run_apative_prompting(model, run_name, max_tokens=100):
    """
    Loop to run each file in the dataset directory through the adaptive prompting process
    Relies on dataset_generation.py having been run first to generate the dataset

    Inputs:
    model: str, name of the model to test the adaptive prompting call on 
    run_name: str, name of the dataset, usually includes the name of the model used to generate the dataset 
                Note this model can differ from the model running the adaptive prompt. 
    """
    # Make dir to store processed data
    file_dir = os.path.join(script_dir, "data", "processed", f'model--{model}', f'd_name--{run_name}')
    os.makedirs(file_dir, exist_ok=True)
    for f in  ['helpful', 'harmless']:
        os.makedirs( os.path.join(file_dir, f) , exist_ok=True)
                
    # Files to process
    topics_files = glob.glob(f'{script_dir}/data/dataset_with_adapt/d_name--{run_name}/*/*.json')
    if len(topics_files) == 0:
        raise Exception("No files found. Please run dataset_generation.py first")

    print(f'Starting to process {len(topics_files)} files \n')
    # Loop over topics files (jsons of topics), process each sub scenario and save new json for each topic file 
    for file in topics_files:
        # check if file exists
        print(file)
       
        file_name = file.split('/')[-1]
        hh  = file.split('/')[-2]
        write_path = os.path.join(file_dir, hh, file_name )
        print(write_path)
        #  check if file exists
        if os.path.exists(write_path):
            print(f'File {write_path} already exists, skipping')
            continue
        process_one_file(file, write_path, max_tokens , model )

    print('Run complete')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some inputs.')
    parser.add_argument('--model', type=str, required=True, help='model to test ')
    parser.add_argument('--run_name', type=str, required=True, help='name of the dataset to process')
    args = parser.parse_args()
    
    model = args.model
    run_name = args.run_name

    print(f'Starting model {model} and dataset {run_name}')
    if model == 'gpt-3.5-turbo':
        max_tokens = 200
    else:
        max_tokens = 300
    run_apative_prompting(model, run_name, max_tokens)
    print(f'Run for {model} complete')


        