from tkinter import *
import tkinter.messagebox


def Zero_warning():
    tkinter.messagebox.showwarning('Warning', 'Viscosity, Density cannot be zero.')


def Save_complete():
    tkinter.messagebox.showinfo('Completed', 'Saving is completed.')


def Simulationtime_error():
    tkinter.messagebox.showwarning('Warning', 'Start time cannot be larger than End time.')


def Float_warning():
    tkinter.messagebox.showwarning('Warning', 'Iterations, Write interval should be INTEGER.')


def UnselectedFolder():
    tkinter.messagebox.showwarning('Warning', 'Set a folder of a simluation.\n Click Basic setting \u2192 Browse')