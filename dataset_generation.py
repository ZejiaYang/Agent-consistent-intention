import sys
import os
from pathlib import Path
import json 
import os
sys.path.append(os.path.join(Path.cwd().parent, 'src' , 'utils') ) 
from utils import load_data, json_arr_to_file, run_api_call
from utils import prompt_dataset

# add examples call fn
helpful_examples_un, harmless_examples = None,  None 

hh = ['Helpful', 'harmless' ]
neg_hh = ['Unhelpful', 'Harmful']
examples = [helpful_examples_un, harmless_examples]  
h_vars = list(zip(examples,  hh, neg_hh  ) ) 


run_name = 'gpt-4_test'
model = "gpt-4"
# model="gpt-3.5-turbo-16k"
#model="gpt-3.5-turbo"



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



num_elements = 10

file_dir = f"../data/intention-{run_name}"
os.makedirs(os.path.dirname(file_dir), exist_ok=True)
for f in hh:
    os.makedirs(f'../data/{file_dir}/{f}' , exist_ok=True)
        
for list_vars in h_vars: 
    ex, h, neg_h = list_vars
    for topic in topics:
        prompt_dataset = prompt_dataset( ex, h, neg_h , topic, num_elements) 
        print("Topic: ", topic, "Help/harm?" , hh , "Prompt: ", prompt_dataset)

        content = run_api_call(prompt_dataset, model)

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

