import PySimpleGUI as sg

col_1 = [[sg.Multiline('Hello', size=(20, 5), key=('ML', '1'), metadata=True)]]
col_2 = [[sg.pin(sg.Multiline('World', size=(20, 5), key=('ML', '2'), metadata=True))]]

layout = [
    [sg.Button('ML1'), sg.Button('ML2')],
    [sg.Column(col_1)],
    [sg.Column(col_2)],
]
window = sg.Window('Title', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event in ('ML1', 'ML2'):
        element = window[('ML', event[-1])]
        visible = element.metadata = not element.metadata
        element.update(visible=visible)

window.close()
