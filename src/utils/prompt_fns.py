import random 
import json
import numpy as np
import pandas as pd



def preprocess_options_and_labels(options, labels):
    """ Fn to randomise the options given to the LLM, whilst storing the mappings from number to label  
    """
    # Zip options and labels
    zipped = list(zip(options, labels))

    # Randomize the order
    random.shuffle(zipped)

    # Enumerate the options (starting from 1) and create the mapping
    mapping = {}
    numbered_options = []
    for number, (option, label) in enumerate(zipped, start=1):
        mapping[number] = label
        numbered_options.append(f"{number}. {option}")

    return mapping, numbered_options


def intention_prompt_first(scenario,  options):
    """ First prompt for LLM, containing the scenrio ,followed by the four options 
    """
    if len(options ) != 4:
        raise Exception("There must be four options")
    
    op1, op2, op3, op4 = options
    system_prompt_content = f"""{scenario} 
    
    {op1}
    {op2}
    {op3}
    {op4}

    Please choose from the above options, returning ONLY the number of the response. 
      """ 
    pre_prompt = [
        {"role": "system", "content": system_prompt_content},
    ]
    
    return pre_prompt 


def intention_prompt_second(scenario,  options, adapt_outcome ):
    """ second adaptive prompt, same as first but also give the 'adapt_outcome' to the model 
    """
    op1, op2, op3, op4 = options
    system_prompt_content = f"""{scenario} 
    
    {op1}
    {op2}
    {op3}
    {op4}

    {adapt_outcome}

    Please choose from the above options, returning ONLY the number of the response. 
      """ 
    pre_prompt = [
        {"role": "system", "content": system_prompt_content},
    ]
    
    return pre_prompt 