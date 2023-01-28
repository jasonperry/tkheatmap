
from tkinter import *
from tkinter import ttk

VERSION = 0.01

GRIDWIDTH = 15
GRIDHEIGHT = 10

class HeatMap(ttk.Frame):

    def __init__(self, parent, nrows, ncols):
        super().__init__(parent, padding="12 6 12 12")
        buttonGrid = []
        for i in range(nrows):
            buttonGrid.append([])
            for j in range(ncols):
                btn = ttk.Label(self, width=5, text=f'{i},\n{j}', padding=2,
                                borderwidth=1, relief="solid")
                btn.grid(row=i, column=j, padx=2, pady=2)
                # Have to make a new scope for each variable or it just uses ref
                btn.bind('<Button-1>',
                         lambda ev, i=i, j=j: self.clickSetColor(ev, i, j))
                buttonGrid[i].append(btn)
        self.buttonGrid = buttonGrid
        self.cur_i = None
        self.cur_j = None

    def popCloseSet(self, n1level, n2level, n3level):
        def scaleDB(level):
            return int((level+120)*(255/120))
        r, g, b = scaleDB(n1level), scaleDB(n2level), scaleDB(n3level)
        rgbval = f"#{r:02x}{g:02x}{b:02x}"
        print("Setting color to", rgbval)
        self.buttonGrid[self.cur_i][self.cur_j].configure(
            background=rgbval)
        self.pop.destroy()
        mainWin.grab_set()

    def popCloseCancel(self):
        self.pop.destroy()
        mainWin.grab_set()      # note, references global

    def validateLevel(self, reason, newtext):
        # print("Validating", newtext, "because of", reason)
        if reason == 'key':
            return newtext.isdigit() or newtext == '-'
        return True

    
    def clickSetColor(self, event, i, j):
        pop = Toplevel(mainWin)
        self.cur_i = i
        self.cur_j = j
        self.pop = pop
        pop.title("Set Signal Strengths")
        pop.geometry("300x240")
        popframe = ttk.Frame(pop, relief=RAISED, borderwidth=1)
        popframe.pack(fill=BOTH, expand=True)
        entValidate = popframe.register(self.validateLevel)
        lblNetwork1 = ttk.Label(popframe, text="Network 1 Strength (db)",
                                foreground="#cc0000")
        lblNetwork1.grid(row=0, column=0)
        n1level = IntVar()
        n1level.set(-120)
        sldNetwork1 = ttk.Scale(popframe, from_=-120, to=0, length=240,
                                orient='horizontal', variable=n1level)
        sldNetwork1.grid(row=1, column=0)
        entNetwork1 = ttk.Entry(popframe, width=5, validate='all',
                                validatecommand=(entValidate, '%V', '%S'),
                                textvariable=n1level)
        entNetwork1.grid(row=1, column=1)
        lblNetwork2 = ttk.Label(popframe, text="Network 2 Strength (db)",
                                foreground="#00cc00")
        lblNetwork2.grid(row=2, column=0)
        n2level = IntVar()
        n2level.set(-120)
        sldNetwork2 = ttk.Scale(popframe, from_=-120, to=0, length=240,
                                orient='horizontal', variable=n2level)
        sldNetwork2.grid(row=3, column=0)
        entNetwork2 = ttk.Entry(popframe, width=5, validate='all',
                                validatecommand=(entValidate, '%V', '%S'),
                                textvariable=n2level)
        entNetwork2.grid(row=3, column=1)
        lblNetwork3 = ttk.Label(popframe, text="Network 3 Strength (db)",
                                foreground="#0000dd")
        lblNetwork3.grid(row=4, column=0)
        n3level = IntVar()
        n3level.set(-120)
        sldNetwork3 = ttk.Scale(popframe, from_=-120, to=0, length=240,
                                orient='horizontal', variable=n3level)
        sldNetwork3.grid(row=5, column=0)
        entNetwork3 = ttk.Entry(popframe, width=5, validate='all',
                                validatecommand=(entValidate, '%V', '%S'),
                                textvariable=n3level)
        entNetwork3.grid(row=5, column=1)
        for child in popframe.winfo_children(): 
            child.grid_configure(padx=5, pady=4)
        
        btnCancel = ttk.Button(pop, text="Cancel",
                               command=self.popCloseCancel)
        btnCancel.pack(side=RIGHT, padx=5, pady=5)
        btnSet = ttk.Button(pop, text="Set", 
                            command=lambda: self.popCloseSet(n1level.get(),
                                                             n2level.get(),
                                                             n3level.get()))
        btnSet.pack(side=RIGHT, padx=5, pady=5)
        pop.attributes("-topmost", True)
        pop.wait_window()
    

# top level (put menus here)
mainWin = Tk()
mainWin.title(f"Heatmap Clicker {VERSION}")
hmFrame = HeatMap(mainWin, 10, 15)

    
hmFrame.pack()
mainWin.mainloop()
