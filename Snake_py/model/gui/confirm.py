import tkinter as tk
from tkinter import messagebox

def display(db):
    root = tk.Tk()
    root.withdraw()
    msgBox = messagebox.askquestion('Delete All', 'Are you sure you want to delete all?', icon='warning')
    if msgBox == 'yes':
        db.delete()
    else:
        messagebox.showinfo('Return', 'Nothing deleted. Returning.')

    root.destroy()