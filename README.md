# Rhys_stream

[Project Documents]([url](https://drive.google.com/drive/folders/1pM45L7s4DCD0uCrmARLyVMqja6NUgDTa)https://drive.google.com/drive/folders/1pM45L7s4DCD0uCrmARLyVMqja6NUgDTa)


##  Current structure: 

####   Run Dataset_generation.py to generate dataset.
- The final dataset is  data/dataset_with_adapt/d_name--gpt-4-dataset-V2, this includes the adaptive prompts 
- the processed data is in found in structure data/processed/model_name/dataset name/{helpful/harmless}/{topic}

#### The method to create the dataset is 
-run dataset_generation with the model of choice  (gpt 4) 
-run add-adaptive_prompts to add the adaptive sentance using gpt-3.5-turbo 

#### The method for  adaptive experiemnts is: 
- Run  'run_experiments.py' with the list of models to test 

#### Processed data 
- saved in data/processed, tagged with model name and the dataset name
- api calls in src/ 

#### analysis
- is currently done in notebook/analysis.ipynb (in progress)
- plots and data are in reports/..



