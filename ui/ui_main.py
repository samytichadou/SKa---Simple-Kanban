import PySimpleGUI as sg
import time

from . import ui_settings

def layout_available_kanbans(availables_kanban):
    kanban_list = []
    for kan in availables_kanban:
        kanban_list.append(kan["name"])
    available_layout=[
            [
                sg.Combo(kanban_list, key='key_kanban', enable_events=True),
                sg.Button("SETTINGS", key='key_settings'),
            ],
        ]
    return available_layout


def draw_main(
    availables_kanban,
    config_datas,
    config_file,
    ):
    
    timer_start = None
    current = ""
    
    # Build layout
    layout = layout_available_kanbans(availables_kanban)
    
    sg.theme('Topanga')
    window = sg.Window("Ska Main", layout)

    while True:
        # Use Timeout to autosave (in millisecond)
        event, values = window.read(timeout=int(config_datas["save_interval"])*1000)
        
        # Quit
        if event in ["Exit","CANCEL"] or event == sg.WIN_CLOSED:
            break
        
        # Open different kanban
        elif event == "key_kanban":
            
            # Save current if needed
            if current:
                print(f"saving {current}")
            
            # Store previous
            current = values["key_kanban"]
            
            # Update kanban
            print(f"opening {current}")
        
        # Open settings
        elif event == "key_settings":
            
            # Open settings window
            config_datas = ui_settings.draw_settings(config_datas, config_file)
            
            # Refresh windows with new settings
        
        # Auto save
        else:
            print("timer auto save")
            # Save current if needed
            if current:
                print(f"saving {current}")
        
    window.close()

### TEST
# settings = {
#     "save_folder": "",
#     "save_interval": 300
# }
# draw_settings(settings, "")
