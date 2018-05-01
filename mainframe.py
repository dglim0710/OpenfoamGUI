from tkinter import *
from tkinter import filedialog
from collections import OrderedDict
import globalvar
import os
import PreFile
import MessageBox


class task_frame(LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render()

    def render(self):
        self.create_task()

    def create_task(self):
        tree_menu_list = ['Basic setting', 'Properties', 'Nozzle spec', 'Solution control', 'Boundary condition', 'Solution scheme', 'Sovler control', 'Meshing', 'Result']
        fontsize = 30

        if globalvar.n == 0:
            self.config(text=tree_menu_list[globalvar.n], font=fontsize)
            Label(self, text='Case folder : ', width=15).grid(row=0, column=0)
            Label(self, text=globalvar.Case_folder_path).grid(row=0, column=1, columnspan=2)
            bt1 = Button(self, text='Browse', command=lambda: Case_browse_button())
            bt1.grid(row=0, column=3)
            # Label(self, text='Openfoam folder : ', width=15).grid(row=1, column=0)
            # Label(self, text=globalvar.Of_folder_path).grid(row=1, column=1, columnspan=2)
            # bt1 = Button(self, text='Browse', command=lambda: Of_browse_button())
            # bt1.grid(row=1, column=3)
        elif globalvar.n == 1:
            self.config(text=tree_menu_list[globalvar.n], font=fontsize)
            Label_dict = ['Liquid density', 'Liquid viscosity', 'Gas density', 'Gas viscosity', 'Surface tension coefficient', 'Gravity (x, y, z)']
            Unit_list = ['[kg/m\xb3]', '[kg/m\u22C5s]', '[kg/m\xb3]', '[kg/m\u22C5s]', '[kg/m\xb2]', '[m/s\xb2]']
            default_value = [0., 0., 0., 0., 0., 0., 0., -9.81]
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
                    Label_values[j].set(default_value[j])
                    Value_dict[Label_array[j]].grid(row=i, column=2, columnspan=1, rowspan=1)
                    j = j+1
                elif vector_dis[i] == 1.:
                    for j in range(j, j+3):
                        if int_dis[j] == 0.:
                            Label_values[j] = DoubleVar()
                        elif int_dis[j] == 1.:
                            Label_values[j] = IntVar()
                        Value_dict[Label_array[j]] = Entry(self, textvariable=Label_values[j], width=10)
                        Label_values[j].set(default_value[j])
                        Value_dict[Label_array[j]].grid(row=i, column=k, columnspan=1, rowspan=1)
                        k = k+1
                    j = j+1
            Button(self, text='Save', width=5, command=lambda: save(Label_values, Value_dict, Label_array, globalvar.n)).grid(row=len(Label_dict)+3, column=6, pady=5, sticky=E)
            Label(self, text='Saving folder : ', width=15).grid(row=len(Label_dict)+10, column=0, pady=5)
            Label(self, text=globalvar.Case_folder_path).grid(row=len(Label_dict)+10, column=2, rowspan=1, columnspan=3)
        elif globalvar.n == 2:
            self.config(text=tree_menu_list[globalvar.n], font=fontsize)
            Label_dict = ['Type', 'Location  (x, y, z)', 'Omega  (x, y, z)', 'Nozzle direction  (x, y, z)', 'Nozzle velocity', 'Radius', 'Width', 'Height', 'Length', 'Angle', 'Fixed thickness', 'Jet velocity']
            vector_dis = [0., 1., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
            Unit_list = ['', '[m]', '[RPM]', '', '[m/s]', '[m]', '[m]', '[m]', '[m]', '[\u00b0]', '[m]', '[m/s]']
            Value_dict = OrderedDict([('Type', 0.), ('LocationX', 0.), ('LocationY', 0.), ('LocationZ', 0.), ('OmegaX', 0.), ('OmegaY', 0.), ('OmegaZ', 0.), ('Motion_directionX', 0.), ('Motion_directionY', 0.), ('Motion_directionZ', 0.), ('Nozzle_velocity', 0.),  ('Radius', 0.), ('Width', 0.), ('Height', 0.), ('Length', 0.), ('Angle', 0.), ('Fixed_thickness', 0.), ('Jet_velocity', 0.)])
            int_dis = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
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
            Button(self, text='Save', width=5, command=lambda: save(Label_values, Value_dict, Label_array, globalvar.n)).grid(row=len(Label_dict)+3, column=6, pady=5, sticky=E)
            Label(self, text='Saving folder : ', width=15).grid(row=len(Label_dict)+5, column=0, pady=5)
            Label(self, text=globalvar.Case_folder_path).grid(row=len(Label_dict)+5, column=1, columnspan=6)
        elif globalvar.n == 3:
            self.config(text=tree_menu_list[globalvar.n], font=fontsize)
            Label_dict = ['Start time', 'End time', 'Time step', 'Write interval']
            Unit_list = ['[s]', '[s]', '[s]', '', '']
            vector_dis = [0., 0., 0., 0., 0.]
            int_dis = [0., 0., 0., 1., 1.]
            default_value = [0., 0., 1e-6, 100]
            Value_dict = OrderedDict([('Start_time', 0.), ('End_time', 0.), ('Time_step', 0.), ('Write_interval', 0.)])
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
                    Label_values[j].set(default_value[j])
                    Value_dict[Label_array[j]].grid(row=i, column=2, columnspan=1, rowspan=1)
                    j = j+1
                elif vector_dis[i] == 1.:
                    for j in range(j, j+3):
                        if int_dis[j] == 0.:
                            Label_values[j] = DoubleVar()
                        elif int_dis[j] == 1.:
                            Label_values[j] = IntVar()
                        Value_dict[Label_array[j]] = Entry(self, textvariable=Label_values[j], width=10)
                        Label_values[j].set(default_value[j])
                        Value_dict[Label_array[j]].grid(row=i, column=k, columnspan=1, rowspan=1)
                        k = k+1
                    j = j+1
            Button(self, text='Save', width=5, command=lambda: save(Label_values, Value_dict, Label_array, globalvar.n)).grid(row=len(Label_dict)+3, column=3, pady=2, sticky=E)
            Button(self, text='Run', width=5, command=lambda: Runsolver(globalvar.Case_folder_path, globalvar.Of_folder_path)).grid(row=len(Label_array)+4, column=3, sticky=E)
            Label(self, text='Saving folder : ', width=15).grid(row=len(Label_dict)+5, column=0, pady=5)
            Label(self, text=globalvar.Case_folder_path).grid(row=len(Label_dict)+5, column=1, columnspan=3)
        elif globalvar.n == 4:
            self.config(text=tree_menu_list[globalvar.n], font=fontsize)
        elif globalvar.n == 5:
            self.config(text=tree_menu_list[globalvar.n], font=fontsize)
        elif globalvar.n == 6:
            self.config(text=tree_menu_list[globalvar.n], font=fontsize)
            Label_dict = ['\u03A8', 'U', 'h', 'U', 'h',  'Iterations']
            Value_dict = OrderedDict([('psi_abs', 0.), ('psi_rel', 0.), ('u_abs', 0.), ('u_rel', 0.), ('h_abs', 0.), ('h_rel', 0.), ('u_relax', 0.), ('h_relax', 0.), ('Iterations', 0.)])
            vector_dis = [1., 1., 1., 0., 0., 0.]
            Unit_list = ['', '', '', '', '', '']
            int_dis = [0., 0., 0., 0., 0., 0., 0., 0., 1.]
            default_value = [1e-9, 1e-4, 1e-9, 1e-4, 1e-9, 1e-4, 0.2, 0.2, 15]
            Label(self, text='Residual', width=10).grid(row=0, column=0)
            Label(self, text='Absolute', width=10).grid(row=0, column=2)
            Label(self, text='Relative', width=10).grid(row=0, column=3)
            Label_array = list(Value_dict.keys())
            Label_values = list(Value_dict.values())
            j = 0
            for i in range(0, 3):
                k = 2
                Label(self, text=Label_dict[i], width=20).grid(row=i+1, column=0, columnspan=1, pady=5)
                Label(self, text=Unit_list[i], width=10).grid(row=i+1, column=1, columnspan=1)
                if vector_dis[i] == 0.:
                    if int_dis[j] == 0.:
                        Label_values[j] = DoubleVar()
                    elif int_dis[j] == 1.:
                        Label_values[j] = IntVar()
                    Value_dict[Label_array[j]] = Entry(self, textvariable=Label_values[j], width=10)
                    Label_values[j].set(default_value[j])
                    Value_dict[Label_array[j]].grid(row=i+1, column=2, columnspan=1, rowspan=1)
                    j = j+1
                elif vector_dis[i] == 1.:
                    for j in range(j, j+2):
                        if int_dis[j] == 0.:
                            Label_values[j] = DoubleVar()
                        elif int_dis[j] == 1.:
                            Label_values[j] = IntVar()
                        Value_dict[Label_array[j]] = Entry(self, textvariable=Label_values[j], width=10)
                        Label_values[j].set(default_value[j])
                        Value_dict[Label_array[j]].grid(row=i+1, column=k, columnspan=1, rowspan=1)
                        k = k+1
                    j = j+1
            Label(self, text='').grid(row=4, column=0)
            Label(self, text='Relaxation factor', width=20).grid(row=5, column=0, columnspan=1)
            for i in range(3, 6):
                k = 2
                Label(self, text=Label_dict[i], width=20).grid(row=i+3, column=0, columnspan=1, pady=5)
                Label(self, text=Unit_list[i], width=10).grid(row=i+3, column=1, columnspan=1)
                if vector_dis[i] == 0.:
                    if int_dis[j] == 0.:
                        Label_values[j] = DoubleVar()
                    elif int_dis[j] == 1.:
                        Label_values[j] = IntVar()
                    Value_dict[Label_array[j]] = Entry(self, textvariable=Label_values[j], width=10)
                    Label_values[j].set(default_value[j])
                    Value_dict[Label_array[j]].grid(row=i+3, column=2, columnspan=1, rowspan=1)
                    j = j+1
                elif vector_dis[i] == 1.:
                    for j in range(j, j+2):
                        if int_dis[j] == 0.:
                            Label_values[j] = DoubleVar()
                        elif int_dis[j] == 1.:
                            Label_values[j] = IntVar()
                        Value_dict[Label_array[j]] = Entry(self, textvariable=Label_values[j], width=10)
                        Label_values[j].set(default_value[j])
                        Value_dict[Label_array[j]].grid(row=i+3, column=k, columnspan=1, rowspan=1)
                        k = k+1
                    j = j+1
            Button(self, text='Save', width=5, command=lambda: save(Label_values, Value_dict, Label_array, globalvar.n)).grid(row=len(Label_dict)+5, column=3, pady=5, sticky=E)
            Label(self, text='Saving folder : ', width=15).grid(row=len(Label_dict)+6, column=0, pady=5)
            Label(self, text=globalvar.Case_folder_path).grid(row=len(Label_dict)+6, column=1, columnspan=3)
        elif globalvar.n == 7:
            self.config(text=tree_menu_list[globalvar.n], font=fontsize)
            Label_dict = ['Mesh type', 'Maximum mesh size']
            vector_dis = [0., 0.]
            Unit_list = ['', '[m]']
            Value_dict = OrderedDict([('Mesh_Type', 0.), ('Mesh_size', 0.)])
            int_dis = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,]
            Label_array = list(Value_dict.keys())
            Label_values = list(Value_dict.values())
            OptionList = ['Triangular', 'Hexagonal']
            Label_values[0] = StringVar()
            Label_values[0].set(OptionList[1])
            Label(self, text=Label_dict[0]).grid(row=0, column=0, pady=5)
            OptionMenu(self, Label_values[0], *OptionList).grid(row=0, column=2)
            j = 1
            for i in range(1, len(Label_dict)):
                k = 2
                Label(self, text=Label_dict[i]).grid(row=i, column=0, columnspan=1, pady=5)
                Label(self, text=Unit_list[i]).grid(row=i, column=1)
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
            Button(self, text='Save', width=12, command=lambda: save(Label_values, Value_dict, Label_array, globalvar.n)).grid(row=len(Label_dict)+3, column=6, pady=2)
            Button(self, text='Meshing', width=12,command=lambda: meshing(Label_values[0].get())).grid(row=len(Label_dict)+4, column=6, pady=2)
            Button(self, text='Generate mesh', width=12,command=lambda: geneartemesh(globalvar.Case_folder_path, globalvar.Of_folder_path, Label_values[0].get())).grid(row=len(Label_dict)+5, column=6, pady=2)
            Label(self, text='Saving folder : ', width=15).grid(row=len(Label_dict)+6, column=0, pady=2)
            Label(self, text=globalvar.Case_folder_path).grid(row=len(Label_dict)+6, column=1, columnspan=3)
        elif globalvar.n == 8:
            self.config(text=tree_menu_list[globalvar.n], font=fontsize)
            Label(self, text='Case folder : ', width=10).grid(row=0, column=0)
            Label(self, text=globalvar.Case_folder_path).grid(row=0, column=1, columnspan=2)
            bt1 = Button(self, text='Browse', command=lambda: Case_browse_button(), width=5)
            bt1.grid(row=0, column=3)
            bt1 = Button(self, text='Result', command=lambda: paraFoam(globalvar.Case_folder_path, globalvar.Of_folder_path), width=5)
            bt1.grid(row=1, column=3)


class tree_frame(LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(text='Tree menu', bg='white', bd=4, font=1)
        self.render()

    def render(self):
        self.create_tree()

    def create_tree(self):
        label1 = Label(self, text='- Pre-process')
        label1.grid(row=0, column=0, padx=2, pady=2)
        label1.config(bg='white', activebackground='gray')

        bt0 = Button(self, text='Basic setting', command=lambda: replace_task_frame(0), width=15)
        bt0.grid(row=1, column=0, padx=2, pady=2)
        bt0.config(bg='white', activebackground='gray', bd=0)
        bt0 = Button(self, text='Meshing', command=lambda: replace_task_frame(7), width=15)
        bt0.grid(row=2, column=0, padx=2, pady=2)
        bt0.config(bg='white', activebackground='gray', bd=0)

        empty0 = Label(self, text='')
        empty0.grid(row=3, column=0, padx=2, pady=2)
        empty0.config(bg='white', activebackground='gray')
        label2 = Label(self, text='- Settings')
        label2.grid(row=4, column=0, padx=2, pady=2)
        label2.config(bg='white', activebackground='gray')
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
        label3 = Label(self, text='- Advanced settings')
        label3.grid(row=9, column=0, padx=2, pady=2)
        label3.config(bg='white', activebackground='gray')
        # bt4 = Button(self, text='Boundary condition', command=lambda: replace_task_frame(4), width=15)
        # bt4.grid(row=10, column=0, padx=2, pady=2)
        # bt4.config(bg='white', activebackground='gray', bd=0)
        # bt5 = Button(self, text='Solution scheme', command=lambda: replace_task_frame(5), width=15)
        # bt5.grid(row=11, column=0, padx=2, pady=2)
        # bt5.config(bg='white', activebackground='gray', bd=0)
        bt6 = Button(self, text='Solver control', command=lambda: replace_task_frame(6), width=15)
        bt6.grid(row=12, column=0, padx=2, pady=2)
        bt6.config(bg='white', activebackground='gray', bd=0)

        empty2 = Label(self, text='')
        empty2.grid(row=13, column=0, padx=2, pady=2)
        empty2.config(bg='white', activebackground='gray')
        label4 = Label(self, text='- Post-process')
        label4.grid(row=14, column=0, padx=2, pady=2)
        label4.config(bg='white', activebackground='gray')
        bt7 = Button(self, text='Result', width=15, command=lambda: replace_task_frame(8))
        bt7.grid(row=15, column=0, padx=2, pady=2)
        bt7.config(bg='white', activebackground='gray', bd=0)

        empty3 = Label(self, text='')
        empty3.grid(row=16, column=0, padx=2, pady=20)
        empty3.config(bg='white', activebackground='gray')
        img = PhotoImage(file='logo.gif')
        wall = Label(self, image=img)
        wall.image = img
        wall.grid(row=20, column=0, sticky=S)


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


class upper_menu(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_menu()
        self.help_menu()

    def file_menu(self):
        filemenu = Menu(self, tearoff=0)
        filemenu.add_command(label='Open Case folder', command=lambda: Case_browse_button())
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=quit)
        self.add_cascade(label='File', menu=filemenu)

    def help_menu(self):
        helpmenu = Menu(self, tearoff=0)
        helpmenu.add_command(label='Help')
        helpmenu.add_command(label='About')
        self.add_cascade(label='Help', menu=helpmenu)


class Application(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Developer Simulator_V_0.1')
        self.geometry()
        self.config(menu=upper_menu())
        self.render()

    def render(self):
        global b
        tree_frame(self).pack(side=LEFT, fill=BOTH, expand=Y)
        b = task_frame(self)
        b.pack(side=RIGHT, fill=BOTH, expand=Y)


def replace_task_frame(menu_number):
    global b
    globalvar.n = menu_number
    b.destroy()
    b = task_frame(app)
    b.pack(side=RIGHT, fill=BOTH, expand=Y)


#------------------------------------------------Button function--------------------------------------------------------


def paraFoam(Casepath, OFpath):
    Casepath = 'cd '+Casepath+' && '
    OFpath = 'call '+OFpath+'/foamWindowsEnvironment.bat'+' && '
    Runpara = 'paraFoam'
    Total = Casepath+OFpath+Runpara
    os.system(Total)


def Runsolver(Casepath, OFpath):
    Casepath = 'cd '+Casepath+' && '
    OFpath = 'call ./Openfoam/foamWindowsEnvironment.bat && '
    RunOP = 'samsungFoamFVTPM7'
    Total = Casepath+OFpath+RunOP
    os.system(Total)


def meshing(mesh_type):
    if mesh_type == 'Triangular':
        mesh_name = 'Mesh_Tri.py'
    elif mesh_type == 'Hexagonal':
        mesh_name = 'Mesh_Hexa.py'
    Salomepath = 'cd ./SALOME/WORK &&'
    RUNSalome = 'run_salome.bat '
    total = Salomepath+RUNSalome+mesh_name
    os.system(total)


def geneartemesh(Casepath, OFpath, mesh_type):
    if mesh_type == 'Triangular':
        mesh_name = 'Mesh_Tri.unv'
    elif mesh_type == 'Hexagonal':
        mesh_name = 'Mesh_Hexa.unv'
    Casepath = 'cd '+Casepath+' && '
    OFpath = 'call ./Openfoam/foamWindowsEnvironment.bat && '
    generateMesh = 'ideasUnvToFoam '
    changeDictionary = ' && changeDictionary'
    Total = Casepath+OFpath+generateMesh+mesh_name+changeDictionary
    os.system(Total)


def Case_browse_button():
    globalvar.Case_folder_path = filedialog.askdirectory()


def Of_browse_button():
    globalvar.Of_folder_path = filedialog.askdirectory()


def save(label_values, label_dict, label_array, menu_number):
    input_list = list(label_array)
    for i in range(0, len(label_values)):
        # if int_check[i] == 1. and type(label_values[i].get()) is not int:
            # MessageBox.Float_warning()
        label_dict[input_list[i]] = label_values[i].get()

    if menu_number == 1:
        if label_dict['Gas_Viscosity'] == 0. or label_dict['Gas_Density'] == 0. or label_dict['Liquid_Viscosity'] == 0. or label_dict['Liquid_Density'] == 0. or label_dict['Surface_tension'] == 0.:
            MessageBox.Zero_warning()
        elif globalvar.Case_folder_path == '! Set the path of a simulation folder !\n ! Click Basic setting \u2192 Browse !':
            MessageBox.UnselectedFolder()
        else:
            MessageBox.Save_complete()
            with open(globalvar.Case_folder_path+'/constant/transportProperties', "w") as text_file:
                text_file.write(PreFile.transportProperties_save(label_dict))
            with open(globalvar.Case_folder_path+'/constant/g', "w") as text_file:
                text_file.write(PreFile.g_save(label_dict))
    elif menu_number == 2:
        if globalvar.Case_folder_path == '! Set the path of a simulation folder !\n ! Click Basic setting \u2192 Browse !':
            MessageBox.UnselectedFolder()
        else:
            MessageBox.Save_complete()
            with open(globalvar.Case_folder_path+'/constant/physicalParameters', "w") as text_file:
                text_file.write(PreFile.physicalParameters_save(label_dict))
    elif menu_number == 3:
        if label_dict['Start_time'] > label_dict['End_time']:
            MessageBox.Simulationtime_error()
        elif globalvar.Case_folder_path == '! Set the path of a simulation folder !\n ! Click Basic setting \u2192 Browse !':
            MessageBox.UnselectedFolder()
        elif label_dict['Time_step'] == 0. or label_dict['Write_interval'] == 0:
            MessageBox.Timestep_error()
        else:
            MessageBox.Save_complete()
            with open(globalvar.Case_folder_path+'/system/controlDict', "w") as text_file:
                text_file.write(PreFile.controlDict_save(label_dict))
    elif menu_number == 6:
        if globalvar.Case_folder_path == '! Set the path of a simulation folder !\n ! Click Basic setting \u2192 Browse !':
            MessageBox.UnselectedFolder()
        else:
            MessageBox.Save_complete()
            with open(globalvar.Case_folder_path+'/system/fvSolution', "w") as text_file:
                text_file.write(PreFile.fvSolution_save(label_dict))
    elif menu_number == 7:
        MessageBox.Save_complete()
        with open('./SALOME/WORK/Mesh_Tri.py', "w") as text_file:
            text_file.write(PreFile.mesh_save(label_dict))


#----------------------------------------------------------------------------------------------------------------------


app = Application()
app.mainloop()

