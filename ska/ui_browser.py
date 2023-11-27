import PySimpleGUI as sg
import time

from . import ui_settings, ui_main, load

def layout_available_kanbans(availables_kanban):
    kanban_list = []
    for kan in availables_kanban:
        kanban_list.append(kan["name"])
    available_layout=[
            [
                sg.Listbox(
                    kanban_list,
                    key='key_kanban',
                    enable_events=True,
                    #select_mode='extended',
                    expand_x=True,
                    expand_y=True,
                    size=(20, 3),
                    ),
                sg.Button("SETTINGS"),
            ],
            [
                sg.Button("OPEN"),
                sg.Button("QUIT"),
            ]
        ]
    return available_layout

def draw_browser(
    availables_kanban,
    config_datas,
    config_file,
    ):

    #sg.set_options(font=font)

    # Init variables
    open_disabled = True
    kb_datas = None

    # Build layout
    layout = layout_available_kanbans(availables_kanban)

    window = sg.Window(
        "SKa Browser",
        layout,
        resizable=True,
        )

    while True:
        event, values = window.read()

        # Quit
        if event in ["Exit","QUIT"] or event == sg.WIN_CLOSED:
            break

        # Open different kanban
        elif event == "key_kanban":

            # Change Open button state
            if open_disabled:
                open_disabled = False
                window["OPEN"].update(disabled=open_disabled)

        # Open settings
        elif event == "SETTINGS":

            # Open settings window
            config_datas = ui_settings.draw_settings(
                config_datas,
                config_file,
                )

        # Open kanban
        elif event == "OPEN":

            # Get kanban datas
            for kb in availables_kanban:
                if kb["name"]==values["key_kanban"][0]:
                    kb_datas = kb
                    break

            # Quit if datas
            if kb_datas:
                # Quit
                break
            else:
                print(f"unable to open {values['key_kanban'][0]}")

    window.close()

    # Open kanban if datas
    if kb_datas:
        print(f"Opening {values['key_kanban']}")
        ui_main.draw_main(
            kb_datas,
            availables_kanban,
            config_datas,
            config_file,
            )

### TEST
# settings = {
#     "save_folder": "",
#     "save_interval": 300
# }
# draw_settings(settings, "")
