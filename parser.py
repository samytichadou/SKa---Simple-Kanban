import os
import json

def _read_json(filepath):
    with open(filepath, "r") as read_file:
        dataset = json.load(read_file)
    return dataset
        
def _get_available_kabans(folder):
    # Kaban json file :
    # filename : ska_name.json
    # Kaban Name
    # Creation date
    available_kabans = []
    for file in os.listdir(folder):
        if file.startswith("ska_") and file.endswith(".json"):
            dataset = _read_json(os.path.join(folder, file))
            available_kabans.append(dataset)
    return available_kabans

def _get_kaban_columns(folder, k_name):
    # Kaban column folder
    # foldername : ska_name_columns
    # Column foldername : col_##_name
    
    columns = []
    
    # Get folder
    k_folder = os.path.join(folder, f"ska_{k_name}")
    if not os.path.isdir(k_folder):
        return columns

    # Get columns
    for root, dirs, files in os.walk(k_folder):
        for dir in dirs:
            if dir.startswith("col_"):
                tmp_name = dir.split("col_")[1]
                col_path = os.path.join(k_folder, dir)
                columns.append(
                    {
                    "name" : tmp_name[3:],
                    "index" : int(tmp_name[:2]),
                    "folderpath" : col_path,
                    "cards" : _get_columns_content(col_path),
                    }
                )
                    
    return columns

def _get_columns_content(column_folder):
    # Card json file :
    # filename : card_###_name.json
    # Card Name
    # Card Index
    # Card Description
    # Card Creation date
    cards = []
    for root, dirs, files in os.walk(column_folder):
        for file in files:
            if file.startswith("card_"):
                dataset = _read_json(os.path.join(column_folder, file))
                cards.append(dataset)
    return cards
        
    

#print(_get_available_kabans("/home/tonton/Desktop/test_ska/"))
print(_get_kaban_columns("/home/tonton/Desktop/test_ska/", "test"))
#print(_get_columns_content("/home/tonton/Desktop/test_ska/ska_test/col_00_plouf/"))
