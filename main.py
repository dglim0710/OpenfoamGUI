from tkinter import *

n = 0


class task_frame(LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render()

    def render(self):
        self.create_task()

    def create_task(self):
        tree_menu_list = ['First page','Properties','Nozzle spec','Solution control']

        if n == 0:
            self.config(text=tree_menu_list[n], width=300, height=600)
            Label(self, text='Select tree menu').pack()
        elif n == 1:
            self.config(text=tree_menu_list[n])
            Label_array = ['Liquid Density','Liquid Viscosity','Gas Density','Gas Viscosity','Gravity']
            for i in range(0,len(Label_array)):
                Label(self, text=Label_array[i]).grid(row=i, column=0,  padx=5, pady=5)
                Entry(self).grid(row=i, column=1)
            Button(self, text='Save', width=5).grid(row=len(Label_array)+3, column=3, pady=30)
        elif n == 2:
            self.config(text=tree_menu_list[n])
            Label_array = ['Type','Location','Nozzle velocity','Motion direction','Radius','Width','Height','Length','Angle','Fixed thickness','Jet velocity','Angular velocity','Thickness tol1','Thickness tol2']
            OptionList = ['Circular', 'Rectangular']
            self.dropVar=StringVar()
            Label(self, text=Label_array[0]).grid(row=0, column=0, padx=5, pady=5)
            OptionMenu(self, self.dropVar, *OptionList).grid(row=0, column=1, padx=5, pady=5)
            for i in range(1,len(Label_array)):
                Label(self, text=Label_array[i]).grid(row=i, column=0, padx=5, pady=5)
                Entry(self).grid(row=i, column=1)
            Button(self, text='Save', width=5).grid(row=len(Label_array)+3, column=3, pady=30)
        elif n == 3:
            self.config(text=tree_menu_list[n])
            Label_array = ['Start time','End time','Time step','Write interval','Iterations']
            for i in range(0,len(Label_array)):
                Label(self, text=Label_array[i]).grid(row=i, column=0, padx=5, pady=5)
                Entry(self).grid(row=i, column=1)
            Button(self, text='Save', width=5).grid(row=len(Label_array)+3, column=3)
            Button(self, text='Run', width=5).grid(row=len(Label_array)+4, column=3)


class tree_frame(LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render()

    def render(self):
        self.create_tree()

    def create_tree(self):
        self.config(text='Tree menu', width='600', height='600', background='white', bd=4)
        label1 = Label(self, text='- SETTINGS')
        label1.grid(row=0, column=0, padx=2, pady=2)
        label1.config(bg='white', activebackground='gray')
        bt1 = Button(self, text='Properties', command=lambda: replace_task_frame(1), width=15)
        bt1.grid(row=1, column=0, padx=2, pady=2)
        bt1.config(bg='white', activebackground='gray', bd=0)
        bt2 = Button(self, text='Nozzle spec', command=lambda: replace_task_frame(2), width=15)
        bt2.grid(row=2, column=0, padx=2, pady=2)
        bt2.config(bg='white', activebackground='gray', bd=0)
        bt3 = Button(self, text='Solution control', command=lambda: replace_task_frame(3), width=15)
        bt3.grid(row=3, column=0, padx=2, pady=2)
        bt3.config(bg='white', activebackground='gray', bd=0)
        bt4 = Button(self, text='Result', width=15)
        bt4.grid(row=4, column=0, padx=2, pady=2)
        bt4.config(bg='white', activebackground='gray', bd=0)


class logo_frame(LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render()

    def render(self):
        self.create_logo()

    def create_logo(self):
        self.config(width=300, height=300, background='white')
        Button(self, text='1').pack()


class Application(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Dev Simulator')
        self.geometry('900x600')
        self.render()

    def render(self):
        global b
        b = task_frame(self)
        tree_frame(self).pack(side=LEFT, fill=BOTH, expand=Y)
        logo_frame(self).pack(side=BOTTOM)
        b.pack(side=RIGHT, fill=BOTH, expand=Y)


def replace_task_frame(menu_number):
    global n
    global b
    n = menu_number
    b.destroy()
    b = task_frame(app)
    b.pack(side=RIGHT, fill=BOTH, expand=Y)

app = Application()
app.mainloop()

