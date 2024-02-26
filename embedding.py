import sys
from pathlib import Path
import os, glob
import voyageai
from dotenv import load_dotenv
import numpy as np
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
utils_dir = os.path.join(src_dir, 'utils')
sys.path.append(src_dir)
sys.path.append(utils_dir)

from utils import load_data, json_arr_to_file
from utils import preprocess_options_and_labels

load_dotenv()  # This loads the variables from .env
VOYAGE_API_KEY = os.getenv('VOYAGE_API_KEY')
client = voyageai.Client(api_key=VOYAGE_API_KEY)
"voyage-large-2"
run_name = "gpt-4-dataset-V2"
model_name = "voyage-large-2"
embeddings_dict = {}

def process_json(json_data):
    # Load JSON data
    data = json_data
    
    # Extract 'topic', 'scenario', and 'options'
    topic = data['topic']
    scenario = data['scenario']
    first_period_index = scenario.find('.')

    if first_period_index != -1:
        scenario = scenario[:first_period_index + 1]

    options = [option.replace("Suggest that the user", "") for option in data['options']]
    concatenated_text = topic + "." + scenario + ".".join(options)
    return concatenated_text

def run_embed_call(client,prompt):
    return client.embed(prompt, model=model_name, input_type="document").embeddings[0]

def embed_one_file(client, file):
    full_json = load_data(file)

    for item in full_json: 
        
        prompt = process_json(item)
        embedding = run_embed_call(client, prompt)
        label = item['topic']
        print(len(embedding))
        if item['topic'] in embeddings_dict:
            embeddings_dict[label].append(embedding)
        else:
            embeddings_dict[label] = [embedding]

    print(f'Finish file {file}')


def run_embedding_prompting(client, model_name):

    file_dir = os.path.join(script_dir, "data", "embeding", f'd_name--{model_name}')
    os.makedirs(file_dir, exist_ok=True)
    for f in  ['helpful']:
        os.makedirs( os.path.join(file_dir, f) , exist_ok=True)
                
    topics_files = glob.glob(f'{script_dir}/data/dataset_with_adapt/d_name--{run_name}/*/*.json')
    if len(topics_files) == 0:
        raise Exception("No files found. Please run dataset_generation.py first")

    print(f'Starting to process {len(topics_files)} files \n')
    for file in topics_files:
        print(file)
        embed_one_file(client, file)

    np.save(f'embeddings_{model_name}.npy', embeddings_dict)
    print('Run complete')

if __name__ == '__main__':
    run_embedding_prompting(client, model_name)





