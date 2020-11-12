from tkinter import *

class DoubleBox:
    def __init__(self):
        self.names = [None, None]
        
        self.root = Tk()

        self.label = Label(self.root, text='Enter players name', width=50, height=2)
        self.fakeLabel = Label(self.root,  width=1)
        self.labelEnterNameOne = Label(self.root, text='Player one [X]', height=2)
        self.labelEnterNameTwo = Label(self.root, text='Player two [O]', height=2)
        self.entryPlayerOne = Entry(self.root, width=30)
        self.entryPlayerTwo = Entry(self.root, width=30)

        self.emptyLabel = Label(self.root, text='', width=50, height=1)
        self.button = Button(self.root, text='Ok', command=self.click)

        self.label.grid(row=0, column=1)
        self.fakeLabel.grid(row=0, column=3)
        self.labelEnterNameOne.grid(row=1, column=0)
        self.entryPlayerOne.grid(row=1, column=1)
        self.labelEnterNameTwo.grid(row=2, column=0)
        self.entryPlayerTwo.grid(row=2, column=1)
        self.emptyLabel.grid(row=3, column=1)
        self.button.grid(row=4, column=1)

        self.root.mainloop()

    def click(self):
        self.names[0] = self.entryPlayerOne.get()
        self.names[1] = self.entryPlayerTwo.get()
        self.root.destroy()

class SimpleBox:
    def __init__(self):
        self.name = None
        
        self.root = Tk()

        self.label = Label(self.root, text='Enter player name', width=50, height=2)
        self.labelEnterName = Label(self.root, text='Player [X]', height=2)
        self.entry = Entry(self.root, width=30)

        self.emptyLabel = Label(self.root, text='', width=50, height=1)
        self.button = Button(self.root, text='Ok', command=self.click)

        self.label.grid(row=0, column=1)
        self.labelEnterName.grid(row=1, column=0)
        self.entry.grid(row=1, column=1)
        self.emptyLabel.grid(row=2, column=1)
        self.button.grid(row=3, column=1)

        self.root.mainloop()

    def click(self):
        self.name = self.entry.get()
        self.root.destroy()