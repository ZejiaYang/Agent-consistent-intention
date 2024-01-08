import json 

def load_data(path):
    f= open(path)   
    data = json.load(f)
    return data

def json_arr_to_file(json_arr, filename_to_write, indent=None):
    with open(filename_to_write, "w") as f:
        json.dump(json_arr, f, indent=indent)
        f.write("\n")