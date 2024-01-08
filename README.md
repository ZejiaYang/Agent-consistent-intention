# Rhys_stream

[Project Documents]([url](https://drive.google.com/drive/folders/1pM45L7s4DCD0uCrmARLyVMqja6NUgDTa)https://drive.google.com/drive/folders/1pM45L7s4DCD0uCrmARLyVMqja6NUgDTa)


##  Current structure: 
####   Run Dataset_generation.py to generate dataset.
This is stored in /data/dataset/d_name/**  

Parameters to update: 
- run_name = 'gpt-4_test' : the name of the dataset to be generated, the d_name
- model = "gpt-4" : the OpenAI model to generate the dataset 
- num_elements = 3 : the number of scenarios to generate per topic 

####  Then run adapative_prompting.py to test adaptive prompts.
 Outputs are saved in /data/processed/model_name/d_name/**

Update the following parameters:
 - run_name = 'gpt-4_test' : change to the same as the name of the dataset to test (d_name) 
- test_models = [ "gpt-4"] : list of OpenAI models to test 

