# Run experiments 

import subprocess
import os 

################################ Update the following variables ################################

data_set_name = 'gpt-4-dataset-V2'

models = [
    'gpt-4-turbo-preview',
    'gpt-4',
    'gpt-3.5-turbo',
    'davinci-002']



################################ Run the experiments  ########################################

import subprocess
from concurrent.futures import ThreadPoolExecutor

def run_script(script_name, **kwargs):
    # Construct the command with script name and kwargs
    command = ['python', script_name]
    for key, value in kwargs.items():
        command.append(f'--{key}={value}')
    
    # Run the command and check if it succeeded
    completed_process = subprocess.run(command, check=True)  # Added check=True for automatic error handling

def main():
    # Use ThreadPoolExecutor to run scripts concurrently
    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = [executor.submit(run_script, 'adaptive_prompting.py', model=model, run_name=data_set_name)
                   for model in models]

        # Wait for all futures to complete
        for future in futures:
            future.result()  # This will re-raise any exception that occurred in the thread
    # run_script('adaptive_prompting.py', model = models[0],  run_name = data_set_name)

if __name__ == '__main__':
    main()
