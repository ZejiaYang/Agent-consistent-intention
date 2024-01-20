import sys
import os
from pathlib import Path
import json 
import os
import glob 


# Adding the 'src' and 'src/utils' directories to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
utils_dir = os.path.join(src_dir, 'utils')
sys.path.append(src_dir)
sys.path.append(utils_dir)

from utils import load_data, json_arr_to_file, run_api_call
from utils import  intention_prompt_first, intention_prompt_second , preprocess_options_and_labels



# run_name = 'gpt-4_test'
run_name = 'gpt-4-dataset-V1'
test_models = [ "gpt-4"]
# test_models = ['gpt-4', 'gpt-3.5-turbo-16k', 'gpt-3.5-turbo']



def process_one_file(file , write_path ):
    """
    Function to process one file in the dataset directory
    Inputs:
    file: str, path to the file to process
    write_path: str, path to the desired output file 
    """
    full_json = load_data(file)
    for item in full_json: 
        op = item['options']
        lab  = item['labels']
        scenario = item['scenario']
        adapt_outcome = item['adapt_outcome']
        
        # permutate options and save mapping 
        mapping, pr_string = preprocess_options_and_labels(op, lab)
        item['mapping_given_to_model'] = mapping 
        
        # load prompts
        first_prompt = intention_prompt_first(scenario, pr_string)
        second_prompt = intention_prompt_second(scenario, pr_string, adapt_outcome)
        # print('First prompt')
        # print('System prompt:', first_prompt[0]['content'])  
        # print('User prompt:', first_prompt[1]['content']) 
        # print('Second prompt')
        # print('System prompt:', second_prompt[0]['content'])  
        # print('User prompt:', second_prompt[1]['content']) 

        # run prompt to gpt and store
        first_model_response = run_api_call(first_prompt, model) 
        item['first response'] = first_model_response
        second_response = run_api_call(second_prompt, model) 
        item['second response'] = second_response

    print(f'Starting to save file {file}')
    json_arr_to_file(full_json, write_path, indent=4)
    print('File saved. \n')

def run_apative_prompting(model, run_name):
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
    topics_files = glob.glob(f'{script_dir}/data/dataset/d_name--{run_name}/*/*.json')
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
        if os.path.exists(write_path):
            print('File already exists, skipping')
            continue
        process_one_file(file, write_path )

    print('Run complete')


if __name__ == "__main__":
    for model in test_models:
        print(f'Starting model {model}')
        run_apative_prompting(model, run_name)