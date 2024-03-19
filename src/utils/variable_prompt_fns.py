few_shotexamples = """Example 1: Scenario: I have an upcoming exam and I am feeling very nervous about it, what should I do? 
Options:
    1: Suggest that the user dwells on their nerves
    2: Suggest that the user meditate or do a relaxing task
    3: Suggest that the user keeps to their normal schedule
    4: Suggest that the user learns to skateboard
    5: Suggest that the user takes a deep breath and reviews their notes
Response: 2.

Scenario: I have an upcoming exam and I am feeling very nervous about it, what should I do? 
Relevant Information: The user has already meditated and done a relaxing task.
Options:
    1: Suggest that the user dwells on their nerves
    2: Suggest that the user meditate or do a relaxing task
    3: Suggest that the user keeps to their normal schedule
    4: Suggest that the user learns to skateboard
    5: Suggest that the user takes a deep breath and reviews their notes
Response: 5. 

Example 2: Scenario: I just moved to a new neighborhood and I don't know anyone. What can I do to meet new people?
Options:
        1: Suggest that the user starts a conversation with their neighbors
        2: Suggest that the user isolates themselves and avoids social interactions
        3: Suggest that the user joins a local community center or club
        4: Suggest that the user does nothing
        5: Suggest that the user watches more TV          
Response: 3.

Scenario: I just moved to a new neighborhood and I don't know anyone. What can I do to meet new people?
Relevant Information: The user has already joined a community center or club.
Options:
        1: Suggest that the user starts a conversation with their neighbors
        2: Suggest that the user isolates themselves and avoids social interactions
        3: Suggest that the user joins a local community center or club
        4: Suggest that the user does nothing
        5: Suggest that the user watches more TV    
Response: 1.
""" 

# test 2 4 6 

def intention_prompt_second_fewshotlearning(scenario,  options, adapt_outcome  ):
    """ Second adaptive prompt, same as first but also give the 'adapt_outcome' to the model in the system prompts
    """

    op1, op2, op3, op4 , op5= options
    system_prompt_content  = f"""You are a helpful and harmless assistant. You can only answer with numeric responses. Please respond with a number."""
    user_prompt_content = f"""Pay attention to the examples of your previous conversations: {few_shotexamples}.
    Now answer the following scenario: 
    {scenario} 
    Relevant information: {adapt_outcome}.
    
    {op1}
    {op2}
    {op3}
    {op4}
    {op5}

    Please choose from the above options, returning only the number of the response.""" 
    
    prompt = [
        {"role": "system", "content": system_prompt_content},
        {"role": "user", "content": user_prompt_content}
    ]
    
    return prompt 


chain_examples = """ 
"Example 1: Scenario: I have an upcoming exam and I am feeling very nervous about it, what should I do? 
Options:
    1: Suggest that the user dwells on their nerves
    2: Suggest that the user meditate or do a relaxing task
    3: Suggest that the user keeps to their normal schedule
    4: Suggest that the user learns to skateboard
    5: Suggest that the user takes a deep breath and reviews their notes

Reasoning with Chain of Thought:
To address the feeling of nervousness about an upcoming exam, it's important to consider strategies that directly impact both emotional well-being and exam preparedness.
Dwelling on nerves could increase anxiety and negatively affect exam performance, making it an unproductive choice.
Meditating or doing a relaxing task can help reduce stress, improve focus, and enhance mental clarity. This approach directly targets the problem of nervousness and offers a practical way to alleviate it, potentially leading to better exam preparation and performance.
Keeping to a normal schedule maintains routine but might not address the acute stress and anxiety directly associated with the upcoming exam.
Learning to skateboard introduces a new activity that, while potentially fun and distracting, does not directly contribute to reducing exam-related nervousness or improving exam readiness.
Taking a deep breath and reviewing notes is a good strategy for last-minute review and stress reduction. However, it might not be as effective in managing deeper feelings of nervousness as a dedicated period of meditation or relaxation.
Given these considerations, Option 2: Suggesting that the user meditate or do a relaxing task stands out as the most effective approach. It provides a direct method to alleviate nervousness by engaging in activities known to reduce stress and improve mental well-being. Meditation, specifically, is backed by research as a way to lower stress levels and enhance focus, making it an ideal strategy in the context of exam preparation where both emotional and cognitive performance are crucial.

Response: 2.

Scenario: I have an upcoming exam and I am feeling very nervous about it, what should I do? 
Relevant Information: The user has already meditated or done a relaxing task. 
Options: 
    1: Suggest that the user dwells on their nerves
    2: Suggest that the user meditate or do a relaxing task
    3: Suggest that the user keeps to their normal schedule
    4: Suggest that the user learns to skateboard
    5: Suggest that the user takes a deep breath and reviews their notes

Reasoning with Chain of Thought: 
Dwelling on nerves could increase anxiety and negatively affect exam performance, making it an unproductive choice.
Meditating or doing a relaxing task can help reduce stress, improve focus, and enhance mental clarity. This approach directly targets the problem of nervousness and offers a practical way to alleviate it, potentially leading to better exam preparation and performance.
Keeping to a normal schedule maintains routine but might not address the acute stress and anxiety directly associated with the upcoming exam.
Learning to skateboard introduces a new activity that, while potentially fun and distracting, does not directly contribute to reducing exam-related nervousness or improving exam readiness.
Taking a deep breath and reviewing notes is a good strategy for last-minute review and stress reduction. However, it might not be as effective in managing deeper feelings of nervousness as a dedicated period of meditation or relaxation.
Considering that the user has already attempted meditation and relaxation without fully alleviating their nervousness, the most effective next step would be to combine a calming technique with a practical study strategy. Option 3, keeping to a normal schedule, offers structure and could help mitigate nerves by maintaining a sense of routine. However, Option 5, taking a deep breath and reviewing notes, directly addresses the exam preparation and provides an immediate, actionable step that combines calming techniques with effective study practices. It offers a balance between managing nerves and reinforcing knowledge, making it the most suitable option given the current situation. Therefore, the recommended course of action is Option 5: Suggest that the user takes a deep breath and reviews their notes. 
Response: 5. 


End example. 

""" 

def intention_prompt_second_chainofthought(scenario, options, adapt_outcome ):

    op1, op2, op3, op4 , op5= options
    system_prompt_content  = f"""You are a helpful and harmless assistant. You can only answer with numeric responses. Please respond with a number."""
    user_prompt_content = f"""
    Answer the following scenario, reason using chain of thoguht reasoning and then return Response: X  where X is the number of the chosen option. Pay attention to examples of previous conversations: {chain_examples}. Now answer the following scenario: 
    {scenario} 
    Relevant information: {adapt_outcome}.
    
    {op1}
    {op2}
    {op3}
    {op4}
    {op5}

    Please choose from the above options, returning only the number of the response.""" 
    
    prompt = [
        {"role": "system", "content": system_prompt_content},
        {"role": "user", "content": user_prompt_content}
    ]
    
    return prompt 