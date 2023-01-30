
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import json
import pathlib

VERSION = 0.1

class HeatMap(ttk.Frame):

    # create new blank map of given size, or load from JSON string.
    def __init__(self, parent, mapStr=None, nrows=5, ncols=8):
        super().__init__(parent, padding="12 6 12 12")
        mapGrid = []
        if mapStr:
            mapData = json.loads(mapStr)
            nrows = len(mapData)
            ncols = len(mapData[0])
        for i in range(nrows):
            mapGrid.append([])
            for j in range(ncols):
                btn = ttk.Label(self, width=5, text=f'{i},\n{j}', padding=2,
                                borderwidth=1, relief="solid")
                if mapStr and mapData[i][j]:
                    btn.configure(background=mapData[i][j])
                btn.grid(row=i, column=j, padx=2, pady=2)
                # Have to make a new scope for each variable or it just uses ref
                btn.bind('<Button-1>',
                         lambda ev, i=i, j=j: self.clickSetColor(ev, i, j))
                mapGrid[i].append(btn)
        self.mapGrid = mapGrid
        self.cur_i = None
        self.cur_j = None

    # Serialize to JSON to save
    def toString(self):
        mapData = []
        for row in self.mapGrid:
            mapRow = []
            for cell in row:
                rgbstr = cell.cget("background")
                mapRow.append(str(rgbstr))
            mapData.append(mapRow)                
        return json.dumps(mapData)

    def popCloseSet(self, n1level, n2level, n3level):
        def scaleDB(level):
            return int((level+120)*(255/120))
        r, g, b = scaleDB(n1level), scaleDB(n2level), scaleDB(n3level)
        rgbval = f"#{r:02x}{g:02x}{b:02x}"
        # print("Setting color to", rgbval)
        self.mapGrid[self.cur_i][self.cur_j].configure(
            background=rgbval)
        self.pop.destroy()
        mainWin.grab_set()

    def popCloseCancel(self):
        self.pop.destroy()
        mainWin.grab_set()      # note, references global

    def validateLevel(self, newtext):
        if not newtext or newtext == '-':
            return True # allows deleting 
        try:
            float(newtext) # works with ints too
            return True
        except ValueError:
            return False
    
    def clickSetColor(self, event, i, j):
        pop = Toplevel(mainWin)
        self.cur_i = i
        self.cur_j = j
        self.pop = pop
        pop.title("Set Signal Strengths")
        pop.geometry("300x240")
        popframe = ttk.Frame(pop, relief=RAISED, borderwidth=1)
        popframe.pack(fill=BOTH, expand=True)
        entValidate = (popframe.register(self.validateLevel), '%P')
        lblNetwork1 = ttk.Label(popframe, text="Network 1 Strength (db)",
                                foreground="#cc0000")
        lblNetwork1.grid(row=0, column=0)
        n1level = IntVar()
        n1level.set(-120)
        sldNetwork1 = ttk.Scale(popframe, from_=-120, to=0, length=240,
                                orient='horizontal', variable=n1level)
        sldNetwork1.grid(row=1, column=0)
        entNetwork1 = ttk.Entry(popframe, width=5, validate='key',
                                validatecommand=entValidate,
                                textvariable=n1level)
        entNetwork1.grid(row=1, column=1)
        lblNetwork2 = ttk.Label(popframe, text="Network 2 Strength (db)",
                                foreground="#00aa00")
        lblNetwork2.grid(row=2, column=0)
        n2level = IntVar()
        n2level.set(-120)
        sldNetwork2 = ttk.Scale(popframe, from_=-120, to=0, length=240,
                                orient='horizontal', variable=n2level)
        sldNetwork2.grid(row=3, column=0)
        entNetwork2 = ttk.Entry(popframe, width=5, validate='key',
                                validatecommand=entValidate,
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
        entNetwork3 = ttk.Entry(popframe, width=5, validate='key',
                                validatecommand=entValidate,
                                textvariable=n3level)
        entNetwork3.grid(row=5, column=1)
        # get the previously set colors, if any
        def rgbToLevels(rgbstr):
            strs = [rgbstr[1:3], rgbstr[3:5], rgbstr[5:7]]
            return [int(int(s, 16)*(120/255)) - 120 for s in strs]
        if prevColor := self.mapGrid[i][j].cget("background"):
            # print(prevColor)
            l1, l2, l3 = rgbToLevels(str(prevColor))
            #print("setting levels to ", l1, l2, l3)
            n1level.set(l1)
            n2level.set(l2)
            n3level.set(l3)            
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
        pop.wait_visibility()
        pop.grab_set()
    

# top level and menus

def newFile():
    dlgNew = Toplevel(mainWin)
    dlgNew.geometry("300x240")
    frmNew = ttk.Frame(dlgNew, relief=RAISED, borderwidth=1,
                       padding="12 6 12 12")
    frmNew.pack(fill=BOTH, expand=True)
    n1name = StringVar()
    n1name.set("Network1")
    n2name = StringVar()
    n2name.set("Network2")
    n3name = StringVar()
    n3name.set("Network3")
    lblNetwork1 = ttk.Label(frmNew, text="Network 1 Name: ",
                            foreground="#cc0000")
    lblNetwork1.grid(row=0, column=0)
    entNetwork1 = ttk.Entry(frmNew, width=25, textvariable=n1name)
    # validatecommand=entValidate,
    # textvariable=n1level)
    entNetwork1.grid(row=0, column=1, pady=5)
    lblNetwork2 = ttk.Label(frmNew, text="Network 2 Name: ",
                            foreground="#00bb00")
    lblNetwork2.grid(row=1, column=0, pady=5)
    entNetwork2 = ttk.Entry(frmNew, width=25, textvariable=n2name)
    entNetwork2.grid(row=1, column=1)
    lblNetwork3 = ttk.Label(frmNew, text="Network 3 Name: ",
                            foreground="#0000ff")
    lblNetwork3.grid(row=2, column=0, pady=5)
    entNetwork3 = ttk.Entry(frmNew, width=25, textvariable=n3name)
    entNetwork3.grid(row=2, column=1)
    vWidth = IntVar()
    vWidth.set(8)
    vHeight = IntVar()
    vHeight.set(6)
    lblWidth = ttk.Label(frmNew, text="Width: ")
    lblWidth.grid(row=3, column=0, pady=10)
    entWidth = ttk.Entry(frmNew, width=4, textvariable=vWidth)
    entWidth.grid(row=3, column=1)
    lblHeight = ttk.Label(frmNew, text="Height: ")
    lblHeight.grid(row=4, column=0, pady=10)
    entHeight = ttk.Entry(frmNew, width=4, textvariable=vHeight)
    entHeight.grid(row=4, column=1)

    def cancel():
        dlgNew.destroy()

    btnCancel = ttk.Button(dlgNew, text="Cancel", command=cancel)
    btnCancel.pack(side=RIGHT, padx=5, pady=5)
    
    def create():
        global hmFrame
        if hmFrame:
            hmFrame.destroy()
        hmFrame = HeatMap(mainWin, nrows=vHeight.get(), ncols=vWidth.get())
        hmFrame.pack()
        dlgNew.destroy()
        
    btnCreate = ttk.Button(dlgNew, text="Create", command=create)
    btnCreate.pack(side=RIGHT, padx=5, pady=5)
    
    dlgNew.attributes("-topmost", True)
    dlgNew.wait_visibility()
    dlgNew.grab_set()


def saveFileAs():
    global hmFrame, filePath
    my_filetypes = [('heatmap files', '.hmap')]
    mapFile = filedialog.asksaveasfile(filetypes=my_filetypes)
    if mapFile:
        mapStr = hmFrame.toString()
        mapFile.write(mapStr)
        filePath = mapFile.name
        filename = pathlib.PurePath(filePath).name
        mainWin.title("Heatmap Clicker - " + filename)
        mapFile.close()
    

def saveFile():
    global hmFrame, filePath
    if filePath is None:
        saveFileAs()
    else:
        mapFile = open(filePath, 'w')
        mapStr = hmFrame.toString()
        mapFile.write(mapStr)
        mapFile.close()

        
def openFile():
    global hmFrame, filePath
    my_filetypes = [('heatmap files', '.hmap')]
    if hmFrame:
        hmFrame.destroy()
    mapFile = filedialog.askopenfile(mode='r')
    if mapFile:
        filedata = mapFile.read()
        #print(filedata)
        # TODO: catch exception if read fails
        hmFrame = HeatMap(mainWin, mapStr=filedata)
        hmFrame.pack()
        filePath = mapFile.name
        filename = pathlib.PurePath(filePath).name
        mainWin.title("Heatmap Clicker - " + filename)
        mapFile.close()

def quit():
    mainWin.destroy()

# TODO: status bar with network names, save network names

mainWin = Tk()
mainWin.title(f"Heatmap Clicker {VERSION}")
hmFrame = None
filePath = None
menubar = Menu(mainWin, tearoff=False)
menuFile = Menu(menubar, tearoff=False)
menubar.add_cascade(menu=menuFile, label='File')
menuFile.add_command(label='New', command=newFile)
menuFile.add_command(label='Open...', command=openFile)
menuFile.add_command(label='Save', command=saveFile)
menuFile.add_command(label='Save As...', command=saveFileAs)
# menuFile.add_command(label='Close')#, command=closeFile)
menuFile.add_command(label='Quit', command=quit)

mainWin['menu'] = menubar

mainWin.mainloop()
