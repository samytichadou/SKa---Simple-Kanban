import os
from parser import load
from ui import ui_settings

# Read config
print("reading config file")
current_dir= os.path.dirname(__file__)
config_file = os.path.join(current_dir, "config.json")
config_datas = load._read_json(config_file)

# Open settings if missing
for setting in config_datas:
    if not config_datas[setting]:
        print(f"missing {setting}, opening settings")
        config_datas = ui_settings.draw_settings(config_datas, config_file)
        break

# Getting available Kanbans
if config_datas["save_folder"]:
    print("loading save folder")
    available_kanbans = load._get_available_kabans(config_datas["save_folder"])

    print(available_kanbans)
