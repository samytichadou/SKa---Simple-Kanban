import PySimpleGUI as sg
import copy

from . import ui_settings, ui_browser, load

def get_element_from_index(datas, index):
    element = None
    for el in datas:
        if el['index']==index:
            element = el
            break
    return element

def get_card_column_index_from_key(key):
    col_index = int(key.split("_col")[1].split("_")[0])
    card_index = int(key.split("_card")[1])
    return col_index, card_index
    
def update_card_content(kb_datas, key, content):
    col_index, card_index = get_card_column_index_from_key(key)
    
    # Get elements
    column = get_element_from_index(kb_datas['columns'], col_index)
    card = get_element_from_index(column['cards'], card_index)
    
    card['content'] = content
    card['to_save'] = True
    return kb_datas

def change_index_markdown(content, new_index):
    old_index = content.split("ska_index : ")[1][0]
    return content.replace(f"ska_index : {old_index}", f"ska_index : {new_index}")

def move_up(kb_datas, key):
    col_index, card_index = get_card_column_index_from_key(key)
    
    # Top card
    if card_index == 0:
        return None
    
    # Get elements
    column = get_element_from_index(kb_datas['columns'], col_index)
    card = get_element_from_index(column['cards'], card_index)
    previous_card = get_element_from_index(column['cards'], card_index-1)
    
    # Change datas
    card['index'] -= 1
    card['content'] = change_index_markdown(card['content'], card['index'])
    card['to_save'] = previous_card['to_save'] = True
    previous_card['index'] += 1
    previous_card['content'] = change_index_markdown(previous_card['content'], previous_card['index'])
    
    return kb_datas

def move_down(kb_datas, key):
    col_index, card_index = get_card_column_index_from_key(key)
    
    # Get elements
    column = get_element_from_index(kb_datas['columns'], col_index)
    if card_index == len(column['cards'])-1:
        return None
    card = get_element_from_index(column['cards'], card_index)
    next_card = get_element_from_index(column['cards'], card_index+1)
    
    # Change datas
    card['index'] += 1
    card['content'] = change_index_markdown(card['content'], card['index'])
    card['to_save'] = next_card['to_save'] = True
    next_card['index'] -= 1
    next_card['content'] = change_index_markdown(next_card['content'], next_card['index'])
    
    return kb_datas

def move_right(kb_datas, key):
    col_index, card_index = get_card_column_index_from_key(key)
    
    # Get elements
    if col_index+1 >= len(kb_datas['columns']):
        return None
    old_column = get_element_from_index(kb_datas['columns'], col_index)
    new_column = get_element_from_index(kb_datas['columns'], col_index+1)
    card = get_element_from_index(old_column['cards'], card_index)
    
    # Change new column
    new_card = card.copy()
    new_card['index'] = 0
    new_card['content'] = change_index_markdown(new_card['content'], 0)
    new_card['to_add'] = True
    for c in new_column['cards']:
        if c['index'] != -1:
            c['index'] += 1
            c['content'] = change_index_markdown(c['content'], c['index'])
            c['to_save'] = True
    new_column['cards'].append(new_card)
    
    # Change old column
    card['to_remove'] = True
    for c in old_column['cards']:
        if c['index'] > card['index'] and c['index'] != -1:
            c['index'] -= 1
            c['content'] = change_index_markdown(c['content'], c['index'])
            c['to_save'] = True
    card['index'] = -1
        
    return kb_datas

def move_left(kb_datas, key):
    col_index, card_index = get_card_column_index_from_key(key)
    
    # Get elements
    if col_index-1 < 0:
        return None
    old_column = get_element_from_index(kb_datas['columns'], col_index)
    new_column = get_element_from_index(kb_datas['columns'], col_index-1)
    card = get_element_from_index(old_column['cards'], card_index)
    
    # Change new column
    new_card = card.copy()
    new_card['index'] = 0
    new_card['content'] = change_index_markdown(new_card['content'], 0)
    new_card['to_add'] = True
    for c in new_column['cards']:
        if c['index'] != -1:
            c['index'] += 1
            c['content'] = change_index_markdown(c['content'], c['index'])
            c['to_save'] = True
    new_column['cards'].append(new_card)
    
    # Change old column
    card['to_remove'] = True
    for c in old_column['cards']:
        if c['index'] > card['index'] and c['index'] != -1:
            c['index'] -= 1
            c['content'] = change_index_markdown(c['content'], c['index'])
            c['to_save'] = True
    card['index'] = -1
        
    return kb_datas
    
def get_current_location(window):
    loc = window.CurrentLocation()
    return (loc[0],loc[1]-38)

def refresh_window(kb_base_datas, show_content=False, window=None, kb_datas=None, button_size=(10, 1)):
    # Refresh datas
    if kb_datas is None:
        kb_datas = load._get_specific_kanban_informations(kb_base_datas)
        
    # Update columns frame numbers
    for c in kb_datas['columns']:
        c['frame_number'] = len(c['cards'])

    kb_layout, scrollable_column_list = layout_selected_kanban(kb_datas, show_content)
    layout = layout_base(kb_datas, button_size, show_content)
    layout.append(kb_layout)
    if window:
        window1 = sg.Window(
            "SKa Main",
            layout,
            resizable=True,
            location=get_current_location(window),
            size = window.size,
            finalize = True,
            )
        window.Close()
    else:
        window1 = sg.Window(
            "SKa Main",
            layout,
            resizable=True,
            size = (900,600),
            finalize = True,
            )
    setup_scrollable_column(window1, scrollable_column_list)
    window = window1
    return window, kb_datas
            
def configure(event, canvas, frame_id):
    canvas.itemconfig(frame_id, width=canvas.winfo_width())

def setup_scrollable_column(window, scrollable_column_list):
    for c in scrollable_column_list:
        frame_id = window[c].Widget.frame_id
        canvas = window[c].Widget.canvas
        canvas.bind("<Configure>", lambda event, canvas=canvas, frame_id=frame_id:configure(event, canvas, frame_id))

def layout_card_frame(col_index, card_datas, show_content=False):
    line_number = card_datas["content"].count('\n') - 4
    card_id = f"col{col_index}_card{card_datas['index']}"
    frame = [
        sg.Frame(
            layout = [
                [
                    sg.Text(
                        card_datas["name"],
                        expand_x=True,
                        key=f"name_{card_id}",
                        #visible = not show_content,
                        )
                ],
                [
                    sg.MLine(
                        card_datas["content"],
                        size=(25, line_number),
                        expand_x=True,
                        key=f"content_{card_id}",
                        enable_events=True,
                        visible = show_content,
                        )
                ],
                [
                    sg.Text(
                        f"{card_datas['creation_date']} - {card_datas['author']}",
                        expand_x=True,
                        key=f"creation_{card_id}",
                        visible = not show_content,
                        )
                ],
                [
                    sg.Button(
                        "<-",
                        expand_x=True,
                        key=f"moveL_{card_id}",
                        ),
                    sg.Button(
                        "DWN",
                        expand_x=True,
                        key=f"moveDOWN_{card_id}",
                        ),
                    sg.Button(
                        "UP",
                        expand_x=True,
                        key=f"moveUP_{card_id}",
                        ),
                    sg.Button(
                        "->",
                        expand_x=True,
                        key=f"moveR_{card_id}",
                        ),
                ],
            ],
            title="",
            relief=sg.RELIEF_SUNKEN,
            expand_x=True,
            key=f"frame_{card_id}"
            )
        ]
    return frame
    

def layout_colcontent(col_datas, show_content):
    # Card key = move{direction}_col{index}_card{index}
    col_layout = []
    cards = sorted(
        col_datas["cards"],
        key = lambda c: c["index"],
        )
    for card in cards:
        if card['to_remove']:
            continue
        line_number = card["content"].count('\n') + 1
        card_id = f"col{col_datas['index']}_card{card['index']}"

        col_layout.append(
            layout_card_frame(col_datas['index'], card, show_content)
            )

    return col_layout

def layout_selected_kanban(kb_datas, show_content = False):
    layout = []
    scrollable_column_keys = []

    # Get columns
    columns = sorted(
        kb_datas["columns"],
        key = lambda c: c["index"],
        )
    for c in kb_datas["columns"]:
        key = f"col{c['index']}"
        column = [
            [
                sg.Text(
                    c["name"],
                    )
            ],
            [sg.HorizontalSeparator()],
            [sg.Column(
                layout_colcontent(c, show_content),
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

def layout_base(kb_datas, button_size, show_content = False):
    base_layout = [
        [
            sg.Text(
                f"Opened : {kb_datas['name']}",
                expand_x=True,
                ),
            sg.Checkbox(
                'Show Content',
                show_content,
                # default=False,
                key = "CONTENT",
                enable_events=True,
                ),
            # sg.Button(
            #     "CONTENT",
            #     expand_x=True,
            #     size=button_size,
            #     ),
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
                "REFRESH",
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
    return base_layout

def update_layout(window, new_datas, kb_datas=None):
    ### Cards
    # TODO Get glob variable to store layout frame
    # TODO or a way to read col elements length
    # TODO and toggle their visibility on if needed
    # Get number of cards
    # print(window["col0"].layout)
    
    # Update cards location
    if kb_datas:
        for column in new_datas['columns']:
            oldcol = get_element_from_index(kb_datas['columns'], column['index'])
            
            # Count valid cards
            frame_nb = oldcol['frame_number']
            old_nb = 0
            for c in oldcol['cards']:
                if c['index'] != -1:
                    old_nb +=1
            new_nb = 0
            for c in column['cards']:
                if c['index'] != -1:
                    new_nb +=1
            
            print()
            print(f"COL{column['index']}")
            print(f"old_nb   = {old_nb}")
            print(f"new_nb   = {new_nb}")
            print(f"frame_nb = {frame_nb}")
            
            # Hide cards if needed
            if new_nb < old_nb:
                for i in range(new_nb, frame_nb):
                    print()
                    print(f"Unvisibling : frame_col{column['index']}_card{i}")
                    window[f"frame_col{column['index']}_card{i}"].update(visible=False)
        
            # Add cards if needed
            elif new_nb > old_nb:
                diff = new_nb-old_nb
                
                # Turn on existing
                if frame_nb > old_nb:
                    rdiff = frame_nb-old_nb
                    if frame_nb <= new_nb:
                        max = frame_nb
                    else:
                        max = new_nb
                    for i in range(max):
                        print()
                        print(f"Visibling : frame_col{column['index']}_card{i}")
                        window[f"frame_col{column['index']}_card{i}"].update(visible=True)
                        
                for i in range(frame_nb, new_nb):
                    card = get_element_from_index(column['cards'], i)
                    print()
                    print(f"Creating : frame_col{column['index']}_card{i}")
                    window.extend_layout(
                        window[f"col{column['index']}"],
                        [layout_card_frame(column['index'], card, new_datas['show_content'])]
                        )
                    column['frame_number'] += 1
                    
            print()
    
    # Update cards content
    for column in new_datas['columns']:
        for card in column['cards']: 
            if (card['to_save'] or card['to_add']) and card['index'] != -1:
                card_id = f"col{column['index']}_card{card['index']}"
                window[f"name_{card_id}"].update(card['name'])
                # window[f"frame_col{column['index']}_card{i}"].update(card['name'])
                window[f"content_{card_id}"].update(card['content'])
                
                creation = f"{card['creation_date']} - {card['author']}"
                window[f"creation_{card_id}"].update(creation)
            
    return new_datas

    
def draw_main(
    kb_base_datas,
    availables_kanban,
    config_datas,
    config_file,
    ):

    # Init variables
    browser = False
    
    window, kb_datas = refresh_window(kb_base_datas)
    print(kb_datas)

    # Scrollable column fix
    # setup_scrollable_column(window, scrollable_column_list)

    while True:
        # Use Timeout to autosave (in millisecond)
        event, values = window.read()
        
        print(event)

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
        
        # Move card
        elif event.startswith("move"):
            new_datas = copy.deepcopy(kb_datas)
            if event.startswith("moveUP"):
                new_datas = move_up(new_datas, event)
            elif event.startswith("moveDOWN"):
                new_datas = move_down(new_datas, event)
            elif event.startswith("moveR"):
                new_datas = move_right(new_datas, event)
            elif event.startswith("moveL"):
                new_datas = move_left(new_datas, event)
            
            print()
            print(kb_datas)
            print()
            print(new_datas)
                
            # Update window and datas if needed
            if new_datas is not None:
                kb_datas = update_layout(window, new_datas, kb_datas)
            
        # Change card content
        elif event.startswith("content_"):
            kb_datas = update_card_content(kb_datas, event, values[event])
            #update_layout(window, kb_datas)
            
        # Show/hide content
        elif event == "CONTENT":
            window, kb_datas = refresh_window(kb_base_datas, values["CONTENT"], window)

        # Refresh button
        elif event == "REFRESH":
            window, kb_datas = refresh_window(kb_base_datas, values["CONTENT"], window)
        
    window.close()

    # Open browser if needed
    if browser:
        ui_browser.draw_browser(
            availables_kanban,
            config_datas,
            config_file,
            )

