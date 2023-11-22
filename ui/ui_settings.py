import PySimpleGUI as sg
import json

def _format_settings_from_gui(gui_values):
    new_dataset = {}
    for v in gui_values:
        if v.startswith("settings_"):
            name = v.split("settings_")[1]
            new_dataset[name] = gui_values[v]
    return new_dataset

def _write_json_file(datas, path) :
    with open(path, "w") as write_file :
        json.dump(datas, write_file, indent=4, sort_keys=False)

def _save_settings(gui_values, filepath):
    print("saving settings")
    dataset = _format_settings_from_gui(gui_values)
    _write_json_file(dataset, filepath)
    print("settings saved")
    return dataset

def draw_settings(settings, filepath):
    layout = []
    s_key_list = []
    # Generate layout
    save_disabled = False
    for s in settings:
        s_key = f"settings_{s}"

        # Initial state of save button if missing entry
        if not settings[s]:
            save_disabled = True

        # Create basic input
        new = [
                sg.Text(s),
                sg.In(settings[s], size=(25, 1), enable_events=True, key=s_key),
                ]

        # Get key of inputs for update
        s_key_list.append(s_key)

        # Get browse button if needed
        if "folder" in s:
            new.append(sg.FolderBrowse())
        layout.append(new)

    # Append buttons
    layout.append(
        [
            sg.Button("SAVE", disabled=save_disabled),
            sg.Button("CANCEL"),
        ]
        )

    sg.theme('Topanga')
    window = sg.Window("Settings", layout)

    while True:
        event, values = window.read()
        # Quit
        if event in ["Exit","CANCEL"] or event == sg.WIN_CLOSED:
            break
        # Allow save or not
        elif event in s_key_list:
            save_disabled = False
            for v in s_key_list:
                if not values[v]:
                    save_disabled = True
            window["SAVE"].update(disabled=save_disabled)
        # Save
        elif event == "SAVE":
            settings = _save_settings(values, filepath)
            break

    window.close()
    return settings

### TEST
# settings = {
#     "save_folder": "",
#     "save_interval": 300
# }
# draw_settings(settings, "")
