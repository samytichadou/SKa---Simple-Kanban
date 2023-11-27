import PySimpleGUI as psg
#set the theme for the screen/window
psg.theme("LightPurple")
#define layout
layout=[[psg.Text("Name",size=(15, 1), font='Lucida',justification='right'),psg.Input()],
        [psg.Text("Date of Birth",size=(15, 1), font=("Verdana",11),text_color='Black',background_color='Yellow', justification='right'),psg.Input()],
        [psg.Text("Class",size=(15, 1), font=("Verdana",11),text_color='Red',justification='right'),psg.Input('M.Sc', background_color='Yellow')],
        [psg.Text("Address",size=(15, 1), font=("Arial",11),text_color='Green',justification='right'),psg.Multiline()],
        [psg.Button("SAVE", font=("Times New Roman",12)),psg.Button("CANCEL", font=("Times New Roman",12))]]
#Define Window
win =psg.Window("Data Entry",layout)
#Read  values entered by user
e,v=win.read()
#close first window
win.close()

#define layout for second windows to display data entered by user in first window
layout1=[[psg.Text("The data you entered is  :", size=(20,1), font='Lucida', text_color='Magenta')],
        [psg.Text("Name :"+v[0], size=(20,1), font='Lucida', text_color='Blue')],
        [psg.Text("DOB :"+v[1], size=(20,1), font='Lucida', text_color='Lime')],
        [psg.Text("Class  :"+v[2], size=(len(v[2])+10,1), font='Lucida', text_color='Yellow')],
        [psg.Text("Address  :"+v[3], size=(int(len(v[3])/4),4), font='Lucida', text_color='Brown', justification='center')]]
#Define Window and display the layout to print output
win1=psg.Window("Output Screen",layout1)

e,v=win1.read()
#close second window
win1.close()
