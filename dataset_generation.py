import sys
import os
from pathlib import Path
import json 
import os

# Adding the 'src' and 'src/utils' directories to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
utils_dir = os.path.join(src_dir, 'utils')
sys.path.append(src_dir)
sys.path.append(utils_dir)

from utils import load_data, json_arr_to_file, run_api_call
from utils import prompt_dataset, load_examples_all, timer 
from utils import prompt_dataset_5pin, load_examples_all_5pin


# Load examples - choose 4 of 5 pin examples 
# helpful_examples, harmless_examples = load_examples_all() 
helpful_examples, harmless_examples = load_examples_all_5pin() 

hh = ['Helpful', 'Harmless' ]
neg_hh = ['Unhelpful', 'Harmful']
examples = [helpful_examples, harmless_examples]  
h_vars = list(zip(examples, hh, neg_hh  ) ) 


run_name = 'gpt-3.5-turbo'

# model = "gpt-4"
model="gpt-3.5-turbo"
# model="gpt-3.5-turbo-16k"

num_elements = 15


if model == "gpt-3.5-turbo":
    max_tokens = 3250
elif model == 'gpt-4':
    max_tokens = 7000

topics  = [
    "Medical",
    "Community",
    "Technology Use",
    "Travel",
    "Education and Learning",
    "Career and Job Search",
    "Environmental Issues",
    "Cultural Issues",
    "Recreational Activities",
    "Personal Relationships", 
    "Criminal activity"
]

@timer 
def run_dataset_gen():
    print(f'Making Directories for run name {run_name} \n')
    file_dir = os.path.join(script_dir, "data", "dataset", f'd_name--{run_name}')
    os.makedirs(file_dir, exist_ok=True)
    for f in hh:
        f=f.lower() 
        os.makedirs( os.path.join(file_dir, f) , exist_ok=True)
            
    for list_vars in h_vars: 
        ex, h, neg_h = list_vars
        print(f'Starting {h} \n')
        for topic in topics:
            print(f'Starting topic {topic} \n')
            ds_prompt = prompt_dataset_5pin( ex, h, neg_h , topic, num_elements) 
            print("Topic: ", topic, "Help/harm?" , h , "Prompt: ", ds_prompt, '\n') 

            content = run_api_call(ds_prompt, model, max_tokens)

            try:
                data = json.loads(content)
            except Exception as e:
                print("Exception: ", e)
                print(content)

            if isinstance(data, list):
                result_len = len(data)
                print(f"Result length: {result_len}")
            else:
                print("Result is not a list :(")
                print(data)

            filename_to_write = os.path.join( file_dir, h , f"{num_elements}--{topic}" ) 
            json_arr_to_file(data, f"{filename_to_write}.json", indent=2)

    print('Generation completed')

if __name__ == '__main__':
    run_dataset_gen() 