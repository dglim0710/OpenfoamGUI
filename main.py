from tkinter import *
from tkinter import filedialog
from collections import OrderedDict
import os
import PreFile
import MessageBox

n = 0
Case_folder_path = 'You need to set the path of a simulation folder\n Click Basic setting \u2192 Browse'
Of_folder_path = 'Set the path of the Openfoam folder'


class task_frame(LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render()

    def render(self):
        self.create_task()

    def create_task(self):
        tree_menu_list = ['Basic setting', 'Properties', 'Nozzle spec', 'Solution control']
        fontsize = 30

        if n == 0:
            global Case_folder_path
            self.config(text=tree_menu_list[n], font=fontsize)
            Label(self, text=Case_folder_path, width=40).grid(row=0, column=0)
            bt1 = Button(self, text='Browse', command=lambda: Case_browse_button())
            bt1.grid(row=0, column=1)
            Label(self, text=Of_folder_path, width=40).grid(row=1, column=0)
            bt1 = Button(self, text='Browse', command=lambda: Of_browse_button())
            bt1.grid(row=1, column=1)
        elif n == 1:
            self.config(text=tree_menu_list[n], font=fontsize)
            Label_dict = ['Liquid density', 'Liquid viscosity', 'Gas density', 'Gas viscosity', 'Surface tension coefficient', 'Gravity']
            Unit_list = ['[kg/m\xb3]', '[kg/m\u22C5s]', '[kg/m\xb3]', '[kg/m\u22C5s]', '[kg/m\xb2]', '[m/s\xb2]']
            vector_dis = [0., 0., 0., 0., 0., 1.]
            int_dis = [0., 0., 0., 0., 0., 0., 0., 0.]
            Value_dict = OrderedDict([('Liquid_Density', 0.), ('Liquid_Viscosity', 0.), ('Gas_Density', 0.), ('Gas_Viscosity', 0.), ('Surface_tension', 0),('GravityX', 0.), ('GravityY', 0.), ('GravityZ', 0.)])
            Label_array = list(Value_dict.keys())
            Label_values = list(Value_dict.values())
            j = 0
            for i in range(0, len(Label_dict)):
                k = 2
                Label(self, text=Label_dict[i], width=20).grid(row=i, column=0, columnspan=1, pady=5)
                Label(self, text=Unit_list[i], width=10).grid(row=i, column=1)
                if vector_dis[i] == 0.:
                    if int_dis[j] == 0.:
                        Label_values[j] = DoubleVar()
                    elif int_dis[j] == 1.:
                        Label_values[j] = IntVar()
                    Value_dict[Label_array[j]] = Entry(self, textvariable=Label_values[j], width=10)
                    Value_dict[Label_array[j]].grid(row=i, column=2, columnspan=1, rowspan=1)
                    j = j+1
                elif vector_dis[i] == 1.:
                    for j in range(j, j+3):
                        if int_dis[j] == 0.:
                            Label_values[j] = DoubleVar()
                        elif int_dis[j] == 1.:
                            Label_values[j] = IntVar()
                        Value_dict[Label_array[j]] = Entry(self, textvariable=Label_values[j], width=10)
                        Value_dict[Label_array[j]].grid(row=i, column=k, columnspan=1, rowspan=1)
                        k = k+1
                    j = j+1
            Button(self, text='Save', width=5, command=lambda: save(Label_values, Value_dict, Label_array, n)).grid(row=len(Label_dict)+3, column=6, pady=5, sticky=E)
            Label(self, text='Saving folder : ', width=15).grid(row=len(Label_dict)+10, column=0, pady=5)
            Label(self, text=Case_folder_path, width=len(Case_folder_path)).grid(row=len(Label_dict)+10, column=1, rowspan=1, columnspan=6)
        elif n == 2:
            self.config(text=tree_menu_list[n], font=fontsize)
            Label_dict = ['Type', 'Location', 'Omega', 'Nozzle direction', 'Nozzle velocity', 'Radius', 'Width', 'Height', 'Length', 'Angle', 'Fixed thickness', 'Jet velocity', 'Thickness tol1', 'Thickness tol2']
            vector_dis = [0., 1., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
            Unit_list = ['', '[m]', '[RPM]', '', '[m/s]', '[m]', '[m]', '[m]', '[m]', '[\u00b0]', '[m]', '[m/s]', '', '']
            Value_dict = OrderedDict([('Type', 0.), ('LocationX', 0.), ('LocationY', 0.), ('LocationZ', 0.), ('OmegaX', 0.), ('OmegaY', 0.), ('OmegaZ', 0.), ('Motion_directionX', 0.), ('Motion_directionY', 0.), ('Motion_directionZ', 0.), ('Nozzle_velocity', 0.),  ('Radius', 0.), ('Width', 0.), ('Height', 0.), ('Length', 0.), ('Angle', 0.), ('Fixed_thickness', 0.), ('Jet_velocity', 0.), ('Thickness_tol1', 0.), ('Thickness_tol2', 0.)])
            int_dis = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,]
            Label_array = list(Value_dict.keys())
            Label_values = list(Value_dict.values())
            OptionList = ['circular', 'rectangular']
            Label_values[0] = StringVar()
            Label_values[0].set(OptionList[1])
            Label(self, text=Label_dict[0]).grid(row=0, column=0, pady=5)
            OptionMenu(self, Label_values[0], *OptionList).grid(row=0, column=1, columnspan=2)
            j = 1
            for i in range(1, len(Label_dict)):
                k = 2
                Label(self, text=Label_dict[i], width=20).grid(row=i, column=0, columnspan=1, pady=5)
                Label(self, text=Unit_list[i], width=10).grid(row=i, column=1)
                if vector_dis[i] == 0.:
                    if int_dis[j] == 0.:
                        Label_values[j] = DoubleVar()
                    elif int_dis[j] == 1.:
                        Label_values[j] = IntVar()
                    Value_dict[Label_array[j]] = Entry(self, textvariable=Label_values[j], width=10)
                    Value_dict[Label_array[j]].grid(row=i, column=2, columnspan=1, rowspan=1)
                    j = j+1
                elif vector_dis[i] == 1.:
                    for j in range(j, j+3):
                        if int_dis[j] == 0.:
                            Label_values[j] = DoubleVar()
                        elif int_dis[j] == 1.:
                            Label_values[j] = IntVar()
                        Value_dict[Label_array[j]] = Entry(self, textvariable=Label_values[j], width=10)
                        Value_dict[Label_array[j]].grid(row=i, column=k, columnspan=1, rowspan=1)
                        k = k+1
                    j=j+1
            Button(self, text='Save', width=5, command=lambda: save(Label_values, Value_dict, Label_array, n)).grid(row=len(Label_dict)+3, column=6, pady=5, sticky=E)
            Label(self, text='Saving folder : ', width=15).grid(row=len(Label_dict)+5, column=0, pady=5)
            Label(self, text=Case_folder_path, width=len(Case_folder_path)).grid(row=len(Label_dict)+5, column=1, columnspan=6)
        elif n == 3:
            self.config(text=tree_menu_list[n], font=fontsize)
            Label_dict = ['Start time', 'End time', 'Time step', 'Write interval', 'Iterations']
            Unit_list = ['[s]', '[s]', '[s]', '', '']
            vector_dis = [0., 0., 0., 0., 0.]
            int_dis = [0., 0., 0., 1., 1.]
            Value_dict = OrderedDict([('Start_time', 0.), ('End_time', 0.), ('Time_step', 0.), ('Write_interval', 0.), ('Iterations', 0.)])
            Label_array = list(Value_dict.keys())
            Label_values = list(Value_dict.values())
            j = 0
            for i in range(0, len(Label_dict)):
                k = 2
                Label(self, text=Label_dict[i], width=20).grid(row=i, column=0, columnspan=1, pady=5)
                Label(self, text=Unit_list[i], width=10).grid(row=i, column=1, columnspan=1)
                if vector_dis[i] == 0.:
                    if int_dis[j] == 0.:
                        Label_values[j] = DoubleVar()
                    elif int_dis[j] == 1.:
                        Label_values[j] = IntVar()
                    Value_dict[Label_array[j]] = Entry(self, textvariable=Label_values[j], width=10)
                    Value_dict[Label_array[j]].grid(row=i, column=2, columnspan=1, rowspan=1)
                    j = j+1
                elif vector_dis[i] == 1.:
                    for j in range(j, j+3):
                        if int_dis[j] == 0.:
                            Label_values[j] = DoubleVar()
                        elif int_dis[j] == 1.:
                            Label_values[j] = IntVar()
                        Value_dict[Label_array[j]] = Entry(self, textvariable=Label_values[j], width=10)
                        Value_dict[Label_array[j]].grid(row=i, column=k, columnspan=1, rowspan=1)
                        k = k+1
                    j = j+1
            Button(self, text='Save', width=5, command=lambda: save(Label_values, Value_dict, Label_array, n)).grid(row=len(Label_dict)+3, column=5, pady=5, sticky=E)
            Button(self, text='Run', width=5, command=Runsolver(Case_folder_path, Of_folder_path)).grid(row=len(Label_array)+4, column=5, sticky=E)
            Label(self, text='Saving folder : ', width=15).grid(row=len(Label_dict)+5, column=0, pady=5)
            Label(self, text=Case_folder_path, width=len(Case_folder_path)).grid(row=len(Label_dict)+5, column=1, columnspan=5)


class tree_frame(LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fontsize = 1
        self.config(text='Tree menu', bg='white', bd=4, font=fontsize)
        self.render()

    def render(self):
        self.create_tree()

    def create_tree(self):
        global Case_folder_path
        global Of_folder_path
        label1 = Label(self, text='- Pre-process')
        label1.grid(row=0, column=0, padx=2, pady=2)
        label1.config(bg='white', activebackground='gray')
        bt0 = Button(self, text='Meshing', command=lambda: replace_task_frame(7), width=15)
        bt0.grid(row=1, column=0, padx=2, pady=2)
        bt0.config(bg='white', activebackground='gray', bd=0)

        empty0 = Label(self, text='')
        empty0.grid(row=2, column=0, padx=2, pady=2)
        empty0.config(bg='white', activebackground='gray')
        label1 = Label(self, text='- Settings')
        label1.grid(row=3, column=0, padx=2, pady=2)
        label1.config(bg='white', activebackground='gray')
        bt0 = Button(self, text='Basic setting', command=lambda: replace_task_frame(0), width=15)
        bt0.grid(row=4, column=0, padx=2, pady=2)
        bt0.config(bg='white', activebackground='gray', bd=0)
        bt1 = Button(self, text='Properties', command=lambda: replace_task_frame(1), width=15)
        bt1.grid(row=5, column=0, padx=2, pady=2)
        bt1.config(bg='white', activebackground='gray', bd=0)
        bt2 = Button(self, text='Nozzle spec', command=lambda: replace_task_frame(2), width=15)
        bt2.grid(row=6, column=0, padx=2, pady=2)
        bt2.config(bg='white', activebackground='gray', bd=0)
        bt3 = Button(self, text='Solution control', command=lambda: replace_task_frame(3), width=15)
        bt3.grid(row=7, column=0, padx=2, pady=2)
        bt3.config(bg='white', activebackground='gray', bd=0)

        empty1 = Label(self, text='')
        empty1.grid(row=8, column=0, padx=2, pady=2)
        empty1.config(bg='white', activebackground='gray')
        label2 = Label(self, text='- Advanced settings')
        label2.grid(row=9, column=0, padx=2, pady=2)
        label2.config(bg='white', activebackground='gray')
        bt4 = Button(self, text='Boundary condition', command=lambda: replace_task_frame(4), width=15)
        bt4.grid(row=10, column=0, padx=2, pady=2)
        bt4.config(bg='white', activebackground='gray', bd=0)
        bt5 = Button(self, text='Solution scheme', command=lambda: replace_task_frame(5), width=15)
        bt5.grid(row=11, column=0, padx=2, pady=2)
        bt5.config(bg='white', activebackground='gray', bd=0)
        bt6 = Button(self, text='Solver control', command=lambda: replace_task_frame(6), width=15)
        bt6.grid(row=12, column=0, padx=2, pady=2)
        bt6.config(bg='white', activebackground='gray', bd=0)

        empty2 = Label(self, text='')
        empty2.grid(row=13, column=0, padx=2, pady=2)
        empty2.config(bg='white', activebackground='gray')
        label3 = Label(self, text='- Post-process')
        label3.grid(row=14, column=0, padx=2, pady=2)
        label3.config(bg='white', activebackground='gray')
        bt7 = Button(self, text='Result', width=15, command=paraFoam(Case_folder_path, Of_folder_path))
        bt7.grid(row=15, column=0, padx=2, pady=2)
        bt7.config(bg='white', activebackground='gray', bd=0)

        empty3 = Label(self, text='')
        empty3.grid(row=16, column=0, padx=2, pady=20)
        empty3.config(bg='white', activebackground='gray')
        img = PhotoImage(file='logo.gif')
        wall = Label(self, image=img)
        wall.image = img
        wall.grid(row=20, column=0)


class logo_frame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render()
        self.config(bg='white')

    def render(self):
        self.create_logo()

    def create_logo(self):
        img = PhotoImage(file='./logo.gif')
        wall = Label(self, image=img)
        wall.image = img
        wall.pack()


class Application(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Dev Simulator')
        self.geometry()
        self.render()

    def render(self):
        global b
        tree_frame(self, width='100').pack(side=LEFT, fill=BOTH, expand=Y)
        b = task_frame(self)
        b.pack(side=RIGHT, fill=BOTH, expand=Y)


def replace_task_frame(menu_number):
    global n
    global b
    n = menu_number
    b.destroy()
    b = task_frame(app)
    b.pack(side=RIGHT, fill=BOTH, expand=Y)


def paraFoam(Casepath, OFpath):
    Casepath = 'cd'+Casepath+'&&'
    OFpath = 'call'+OFpath+'&&'
    Runpara = 'paraFoam'
    Total = Casepath+OFpath+Runpara
    os.system(Total)


def Runsolver(Casepath, OFpath):
    Casepath = 'cd'+Casepath+'&&'
    OFpath = 'call'+OFpath+'&&'
    RunOP = 'samsungFoamFVTPM7'
    Total = Casepath+OFpath+RunOP
    os.system(Total)


def Case_browse_button():
    global Case_folder_path
    Case_folder_path = filedialog.askdirectory()


def Of_browse_button():
    global Of_folder_path
    Of_folder_path = filedialog.askdirectory()


def save(label_values, label_dict, label_array, menu_number):
    input_list = list(label_array)
    for i in range(0, len(label_values)):
        label_dict[input_list[i]] = label_values[i].get()
    if menu_number == 1:
        if label_dict['Gas_Viscosity'] == 0. or label_dict['Gas_Density'] == 0. or label_dict['Liquid_Viscosity'] == 0. or label_dict['Liquid_Density'] == 0. or label_dict['Surface_tension'] == 0.:
            MessageBox.Zero_warning()
        else:
            MessageBox.Save_complete()
            with open(folder_path+'/constant/transportProperties', "w") as text_file:
                text_file.write(PreFile.transportProperties_save(label_dict))
            with open(folder_path+'/constant/g', "w") as text_file:
                text_file.write(PreFile.g_save(label_dict))
    elif menu_number == 2:
        MessageBox.Save_complete()
        with open(folder_path+'/constant/physicalParameters', "w") as text_file:
            text_file.write(PreFile.physicalParameters_save(label_dict))
    elif menu_number == 3:
        if label_dict['Start_time'] > label_dict['End_time']:
            MessageBox.Simulationtime_error()
        else:
            MessageBox.Save_complete()
            with open(folder_path+'/system/controlDict', "w") as text_file:
                text_file.write(PreFile.controlDict_save(label_dict))
            with open(folder_path+'/system/fvSolution', "w") as text_file:
                text_file.write(PreFile.fvSolution_save(label_dict))


app = Application()
app.mainloop()

