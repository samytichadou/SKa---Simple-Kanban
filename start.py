import os

from parser import load
from ui import ui_settings, ui_main

# Read config
current_dir= os.path.dirname(__file__)
config_file = os.path.join(current_dir, "config.json")
print(f"reading config file : {config_file}")
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
    ui_main.draw_main(available_kanbans, config_datas, config_file)
