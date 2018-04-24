from tkinter import *
import tkinter.messagebox


def Zero_warning():
    tkinter.messagebox.showwarning('Warning', 'Viscosity, Density cannot be zero.')


def Save_complete():
    tkinter.messagebox.showinfo('Completed', 'Saving is completed.')


def Simulationtime_error():
    tkinter.messagebox.showwarning('Warning', 'Start time cannot be larger than End time.')