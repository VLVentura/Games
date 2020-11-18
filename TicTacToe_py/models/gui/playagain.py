import tkinter as tk
from tkinter import messagebox

def display_question(winner, mode=None):
    root = tk.Tk()

    if mode == 'tie':
        msg = 'It was a draw!\nDo you want to play again?\n'
    else:
        msg = 'Winner of the match was {}!\nDo you want to play again?'.format(winner)
    
    root.withdraw()

    msgBox = messagebox.askquestion('Play Again', message=msg, icon='question')
    if msgBox == 'no':
        ans = False
    else:
        messagebox.showinfo('Play Again', message='Restarting board!')
        ans = True

    root.destroy()
    return ans