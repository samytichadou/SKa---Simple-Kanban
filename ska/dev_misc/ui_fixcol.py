import PySimpleGUI as sg

def configure(event, canvas, frame_id):
    print("CONFIGURE")
    canvas.itemconfig(frame_id, width=canvas.winfo_width())

column_layout = [
    [sg.Frame(f"Frame {i}", [[sg.Text("Hello"), sg.Push(), sg.Text("World")]], expand_x=True)] for i in range(10)
]
layout = [
    [sg.Column(column_layout, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, key='Scrollable Column')]
]

window = sg.Window("Title", layout, resizable=True, margins=(0, 0), finalize=True)
frame_id = window['Scrollable Column'].Widget.frame_id
canvas = window['Scrollable Column'].Widget.canvas
canvas.bind("<Configure>", lambda event, canvas=canvas, frame_id=frame_id:configure(event, canvas, frame_id))

while True:

    event, values = window.read()

    if event in ('Close', sg.WIN_CLOSED):
        break

window.close()
