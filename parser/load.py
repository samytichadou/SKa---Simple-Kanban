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
    #
    # Also get filepath

    available_kabans = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.startswith("ska_") and file.endswith(".json"):
                filepath = os.path.join(root, file)
                dataset = _read_json(filepath)
                dataset["filepath"]= filepath
                available_kabans.append(dataset)
    return available_kabans

def _get_specific_kaban_informations(kaban_dataset):
    # Get Kaban Details and Contents
    kaban_dataset["columns"] = _get_kaban_columns(
                            os.path.dirname(kaban_dataset["filepath"]),
                            kaban_dataset["name"],
                            )
    return kaban_dataset

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

    

### TESTS ###
#available_kabans = _get_available_kabans("/home/tonton/blender_addons/addons/SKa-Simple-Kanban/example_structure/")
#print(_get_kaban_columns("/home/tonton/blender_addons/addons/SKa-Simple-Kanban/example_structure/", "test"))
#print(_get_columns_content("/home/tonton/blender_addons/addons/SKa-Simple-Kanban/example_structure/ska_test/col_00_plouf/"))
#print(_get_specific_kaban_informations(available_kabans[0]))
