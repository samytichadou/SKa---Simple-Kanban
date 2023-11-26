import os
import json

def _read_json(filepath):
    with open(filepath, "r") as read_file:
        dataset = json.load(read_file)
    return dataset

def _read_ska_markdown(filepath):
    card_datas = {}
    with open(filepath) as f:
        lines = f.readlines()
        
    content = ''.join(lines)
    card_datas["content"] = content
    card_datas["name"] = content.split("ska_name : ")[1].split("  ")[0]
    card_datas["index"] = int(content.split("ska_index : ")[1].split("  ")[0])
    card_datas["author"] = content.split("ska_author : ")[1].split("  ")[0]
    card_datas["creation_date"] = content.split("ska_creation_date : ")[1].split("  ")[0]
    return card_datas

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
                            )
    return kaban_dataset

def _get_kaban_columns(folder):
    # Kaban column folder
    # foldername : ska_name_columns
    # Column foldername : col_##_name

    columns = []

    # Get columns
    for root, dirs, files in os.walk(folder):
        for dir in dirs:
            if dir.startswith("col_"):
                print(f"found column in {dir}")
                tmp_name = dir.split("col_")[1]
                col_path = os.path.join(folder, dir)
                columns.append(
                    {
                    "name" : tmp_name[3:],
                    "index" : int(tmp_name[:2]),
                    "folderpath" : col_path,
                    "cards" : _get_columns_content(col_path),
                            }
                )
                    
    if not columns:
        print(f"no column found in {folder}")

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
                dataset = _read_ska_markdown(os.path.join(column_folder, file))
                cards.append(dataset)
    cards = sorted(
        cards,
        key = lambda c: c["index"],
        )
    return cards

    

### TESTS ###
#available_kabans = _get_available_kabans("/home/tonton/blender_addons/addons/SKa-Simple-Kanban/example_structure/")
#print(_get_kaban_columns("/home/tonton/blender_addons/addons/SKa-Simple-Kanban/example_structure/", "test"))
#print(_get_columns_content("/home/tonton/blender_addons/addons/SKa-Simple-Kanban/example_structure/ska_test/col_00_plouf/"))
#print(_get_specific_kaban_informations(available_kabans[0]))
