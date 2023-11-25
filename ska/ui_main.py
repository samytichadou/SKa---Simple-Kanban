import PySimpleGUI as sg

from . import ui_settings, ui_browser, load

def layout_colcontent(col_datas):
    col_layout = []
    for card in col_datas["cards"]:

        col_layout.append(
            [
            sg.Frame(
                layout = [
                    [sg.Text(card["description"])],
                    [
                        sg.Button(
                            "<-",
                            expand_x=True,
                            key=f"moveL_{card['name']}",
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
                tooltip=card["creation_date"],
                expand_x=True,
                )
            ]
        )

    layout = [
        sg.Column(
            col_layout,
            expand_x=True,
            expand_y=True,
            scrollable=True,
            vertical_scroll_only=True,
        )
        ]

        # layout.append(card_layout)
    return layout

def layout_selected_kanban(kb_datas):
    layout = []

    # Get columns
    n=0
    for c in kb_datas["columns"]:
        col_content = layout_colcontent(c)
        column = [
            [
                sg.Text(
                    c["name"],
                    )
            ],
            #[sg.HorizontalSeparator()],
            col_content,
            ]
        if n!=0:
            layout.append(sg.VerticalSeparator())
        layout.append(
            sg.Column(
                column,
                expand_x=True,
                expand_y=True,
                # scrollable=True,
                # vertical_scroll_only=True,
                ),
            )
        n+=1

    return layout

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
    kb_layout = layout_selected_kanban(kb_datas)
    layout.append(kb_layout)
    
    window = sg.Window(
        "Ska Main",
        layout,
        resizable = True,
        size = (900,600),
        )

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
