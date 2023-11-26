import PySimpleGUI as sg

from . import ui_settings, ui_browser, load

def configure(event, canvas, frame_id):
    canvas.itemconfig(frame_id, width=canvas.winfo_width())

def layout_colcontent(col_datas):
    col_layout = []
    for card in col_datas["cards"]:
        line_number = card["content"].count('\n') + 1

        col_layout.append(
            [
            sg.Frame(
                layout = [
                    [
                        sg.MLine(
                            card["content"],
                            size=(25, line_number),
                            expand_x=True,
                            )
                    ],
                    [
                        sg.Button(
                            "<-",
                            expand_x=True,
                            key=f"moveL_{card['name']}",
                            ),
                        sg.Button(
                            "DWN",
                            expand_x=True,
                            key=f"moveDWN_{card['name']}",
                            ),
                        sg.Button(
                            "UP",
                            expand_x=True,
                            key=f"moveUP_{card['name']}",
                            ),
                        sg.Button(
                            "->",
                            expand_x=True,
                            key=f"moveR_{card['name']}",
                            ),
                    ],
                ],
                title=card["name"],
                # title_color='red',
                relief=sg.RELIEF_SUNKEN,
                tooltip=f"{card['creation_date']}\n{card['author']}",
                expand_x=True,
                )
            ]
        )

        # layout.append(card_layout)
    return col_layout

def layout_selected_kanban(kb_datas):
    layout = []
    scrollable_column_keys = []

    # Get columns
    for c in kb_datas["columns"]:
        key = f"col{c['index']}_{c['name']}"
        column = [
            [
                sg.Text(
                    c["name"],
                    )
            ],
            [sg.HorizontalSeparator()],
            [sg.Column(
                layout_colcontent(c),
                expand_x=True,
                expand_y=True,
                scrollable=True,
                vertical_scroll_only=True,
                key=key,
                )
            ],
            ]
        if c["index"]!=0:
            layout.append(sg.VerticalSeparator())
        layout.append(
            sg.Column(
                column,
                expand_x=True,
                expand_y=True,
                ),
            )
        scrollable_column_keys.append(key)
    print(scrollable_column_keys)
    return layout, scrollable_column_keys

def draw_main(
    kb_datas,
    availables_kanban,
    config_datas,
    config_file,
    ):

    # Init variables
    current = kb_datas["name"]
    browser = False

    # Build base layout
    button_size = (10, 1)
    layout = [
        [
            sg.Text(
                f"Opened : {current}",
                expand_x=True,
                ),
            sg.Button(
                "BROWSER",
                expand_x=True,
                size=button_size,
                ),
            sg.Button(
                "SETTINGS",
                expand_x=True,
                size=button_size,
                ),
            sg.Button(
                "QUIT",
                expand_x=True,
                size=button_size,
                ),
        ],
        [sg.HorizontalSeparator()],
    ]

    # Get kb layout
    kb_layout, scrollable_column_list = layout_selected_kanban(kb_datas)
    layout.append(kb_layout)
    
    window = sg.Window(
        "Ska Main",
        layout,
        resizable = True,
        size = (900,600),
        finalize = True,
        )
    # Scrollable column fix
    for c in scrollable_column_list:
        frame_id = window[c].Widget.frame_id
        canvas = window[c].Widget.canvas
        canvas.bind("<Configure>", lambda event, canvas=canvas, frame_id=frame_id:configure(event, canvas, frame_id))

    while True:
        # Use Timeout to autosave (in millisecond)
        event, values = window.read(timeout=int(config_datas["save_interval"])*1000)
        
        # Quit
        if event in ["Exit","QUIT"] or event == sg.WIN_CLOSED:
            break

        # Open settings
        elif event == "SETTINGS":
            
            # Open settings window
            config_datas = ui_settings.draw_settings(
                config_datas,
                config_file,
                )
            
            # Refresh windows with new settings

        # Open browser
        elif event == "BROWSER":
            browser = True
            break
        
        # Auto save
        else:
            print("auto save")
            # Save current if needed
            if current:
                print(f"saving {current}")
        
    window.close()

    # Open browser if needed
    if browser:
        ui_browser.draw_browser(
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
