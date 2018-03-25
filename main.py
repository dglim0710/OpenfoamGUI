from tkinter import *

root = Tk()
root.title('Dev simulator')
a = Frame(root)


def replace_task_frame(menu_number):
    a.destroy()
    global a
    a = Frame(root)
    if menu_number == 1:
        set_task1_frame(a)
    elif menu_number == 2:
        set_task2_frame(a)
    elif menu_number == 3:
        set_task3_frame(a)
    a.pack(side=LEFT)


def set_task1_frame(menu):
    Label_array = ['Liquid Density','Liquid Viscosity','Gas Density','Gas Viscosity','Gravity']
    for i in range(0,len(Label_array)):
        Label(menu, text=Label_array[i]).grid(row=i, column=0)
        Entry(menu).grid(row=i, column=1)


def set_task2_frame(menu):
    Label_array = ['Type','Location','Nozzle velocity','Motion direction','Radius','Width','Height','Length','Angle','Fixed thickness','Jet velocity','Angular velocity','Thickness tol1','Thickness tol2']
    for i in range(0,len(Label_array)):
        Label(menu, text=Label_array[i]).grid(row=i, column=0)
        Entry(menu).grid(row=i, column=1)


def set_task3_frame(menu):
    Label_array = ['Start time','End time','Time step','Write interval','Iterations']
    for i in range(0,len(Label_array)):
        Label(menu, text=Label_array[i]).grid(row=i, column=0)
        Entry(menu).grid(row=i, column=1)


Tree_frame = Frame(root)
Tree_label = Label(Tree_frame, text='- SETTINGS').grid(row=0, column=0, sticky=W)
Properties_button = Button(Tree_frame, text='Properties', command=lambda: replace_task_frame(1)).grid(row=1, column=0, sticky=W)
Nozzle_button = Button(Tree_frame, text='Nozzle spec', command=lambda: replace_task_frame(2)).grid(row=2, column=0, sticky=W)
Solution_button = Button(Tree_frame, text='Solution control', command=lambda: replace_task_frame(3)).grid(row=3, column=0, sticky=W)

Tree_frame.pack(side=LEFT)

root.mainloop()