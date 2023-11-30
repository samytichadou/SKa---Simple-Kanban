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
    ska_datas = content.split("ska{")[1].split("}")[0]
    card_datas["name"] = ska_datas.split("name:")[1].split(",")[0]
    card_datas["index"] = int(ska_datas.split("index:")[1].split(",")[0])
    card_datas["author"] = ska_datas.split("author:")[1].split(",")[0]
    card_datas["creation_date"] = ska_datas.split("creation_date:")[1].split(",")[0]
    card_datas["to_save"] = False
    card_datas["to_remove"] = False
    card_datas["to_add"] = False
    return card_datas

def _get_available_kanbans(folder):
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
                dataset['filepath'] = filepath
                dataset['show_content'] = False
                available_kabans.append(dataset)
    return available_kabans

def _get_specific_kanban_informations(kanban_dataset):
    # Get Kaban Details and Contents
    kanban_dataset["columns"] = _get_kanban_columns(
                            os.path.dirname(kanban_dataset["filepath"]),
                            )
    return kanban_dataset

def _get_kanban_columns(folder):
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
                    "frame_number": 0,
                    "to_save": False,
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
    return cards

# def _refresh_kb_datas(kb_datas):
#     kaban_dataset["columns"] = _get_kaban_columns(
#                             os.path.dirname(kaban_dataset["filepath"]),
#                             )
#     for kb in availables_kanban:
#         if kb["name"]==values["key_kanban"][0]:
#             kb_datas = load._get_specific_kaban_informations(kb)
#     return kb_datas
    

### TESTS ###
#available_kabans = _get_available_kabans("/home/tonton/blender_addons/addons/SKa-Simple-Kanban/example_structure/")
#print(_get_kaban_columns("/home/tonton/blender_addons/addons/SKa-Simple-Kanban/example_structure/", "test"))
#print(_get_columns_content("/home/tonton/blender_addons/addons/SKa-Simple-Kanban/example_structure/ska_test/col_00_plouf/"))
#print(_get_specific_kaban_informations(available_kabans[0]))
