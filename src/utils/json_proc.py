import json 

def load_data(path):
    f= open(path)   
    data = json.load(f)
    return data

def json_arr_to_file(json_arr, filename_to_write, indent=None):
    with open(filename_to_write, "w") as f:
        json.dump(json_arr, f, indent=indent)
        f.write("\n")


import time

def timer(func):
    """A decorator that prints the execution time of the function it decorates."""
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Start the timer
        result = func(*args, **kwargs)  # Call the function
        end_time = time.time()  # End the timer
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper


