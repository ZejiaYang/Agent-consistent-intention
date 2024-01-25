import json
import os
import glob 

files_with_less_than_20_entries = [] 


folders = glob.glob('/Users/gracecolverd/MARS/Rhys_stream/data/dataset/d_name--gpt-4-dataset-V2/*')
# Replace 'your_folder_path' with the path to your folder containing JSON files
for folder_path in folders:
    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):  # Check if the file is a JSON file
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r') as file:
                # Load JSON data from file
               with open(file_path, 'r') as file:
                # Load JSON data from file
                data = json.load(file)

                # Determine number of entries (items in array or key-value pairs in object)
                num_entries = None
                if isinstance(data, list):
                    num_entries = len(data)  # Number of items in array
                elif isinstance(data, dict):
                    num_entries = len(data.keys())  # Number of key-value pairs in object

                # Check if the file has less than 20 entries
                if num_entries is not None and num_entries < 20:
                    files_with_less_than_20_entries.append(file_path)
               
print(files_with_less_than_20_entries)