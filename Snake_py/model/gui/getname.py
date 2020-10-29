from tkinter import *

class Box:
    def __init__(self, score):
        self.name = None
        
        self.root = Tk()

        self.label = Label(self.root, text='You die! Your score was {}'.format(score), width=50, height=2)
        self.labelEnterName = Label(self.root, text='Entry your name', width=50, height=2)
        self.entry = Entry(self.root, width=30)

        self.emptyLabel = Label(self.root, text='', width=50, height=1)
        self.button = Button(self.root, text='Entry', command=self.click)

        self.label.grid(row=0, column=1)
        self.labelEnterName.grid(row=1, column=1)
        self.entry.grid(row=2, column=1)
        self.emptyLabel.grid(row=3, column=1)
        self.button.grid(row=4, column=1)

        self.root.mainloop()

    def click(self):
        self.name = self.entry.get()
        self.root.destroy()