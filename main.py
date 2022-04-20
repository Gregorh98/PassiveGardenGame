from tkinter import *
from math import floor, ceil


class Plot():
    def __init__(self, x, y):
        self.states = {"grass"  : 0,
                       "tilledLand" : 1}
        self.x = x
        self.y = y
        self.state = None

    def draw(self, canvas):
        self.graphicalPlot = garden.create_rectangle(x, y, x+gridSize, y+gridSize, fill=cGrass, outline=cGrassOutline)
        #garden.tag_bind(self.graphicalPlot, "<1>", self.mouse_click)
        garden.tag_bind(self.graphicalPlot, "<ButtonPress-1>", self.mouse_click)

    def mouse_click(self, event):
        print((self.x, self.y))
        currentItem = itemsViewer.get(itemsViewer.curselection())
        if currentItem == "Hoe":
            self.hoeGround(event)

    def hoeGround(self, event):
        if self.state != self.states["tilledLand"]:
            garden.itemconfig(self.graphicalPlot, fill=cTilledLand, outline=cTilledLandOutline)
            self.state = self.states["tilledLand"]
            print("Tilled")

root = Tk()
root.resizable(False, False)

canvasHeight    = 320
canvasWidth     = 320
gridSize        = 32
tools       = ["Hoe", "Watering Can", "Trowel", "Dibber", "Fork", "Netting"]
crops       = ["Potato", "Peas", "Strawberry", "Corn", "Broccoli"]
decoration  = ["Path", "Fence"]
gardenData  = []

cTilledLand         = "#52402a"
cTilledLandOutline  = "#39301d"
cDryLand            = "#6b584a"
cWetLand            = "#482f1f"
cGrass              = "#2c3c1e"
cGrassOutline       = "#202a15"
cPath               = "#a9b1b7"


garden = Canvas(root)
garden.configure(background=cGrass, height=canvasHeight, width=canvasWidth)
garden.grid(column=0, row=0, rowspan=2)

#prepareGarden
for y in range(0, canvasHeight, 32):
    gardenData.append([])
    for x in range(0, canvasWidth, 32):
        gardenData[0 if y==0 else int(y/gridSize)].append(Plot(x, y))
        gardenData[0 if y == 0 else int(y / gridSize)][0 if x == 0 else int(x / gridSize)].draw(garden)

print(">>",len(gardenData))

def showTools():
    itemsViewer.delete(0, END)
    for tool in tools:
        itemsViewer.insert(END, tool)
    itemsViewer.select_set(0)

def showDecoration():
    itemsViewer.delete(0, END)
    for item in decoration:
        itemsViewer.insert(END, item)
    itemsViewer.select_set(0)

def showCrops():
    itemsViewer.delete(0, END)
    crops.sort()
    for crop in crops:
        itemsViewer.insert(END, crop)
    itemsViewer.select_set(0)

#Sidebar
sideBar = Frame(root)
Label(sideBar, text="Garden Game").pack(padx=2, fill=BOTH)

#Items
itemsFrame = LabelFrame(sideBar, text="Items")

itemsViewer = Listbox(itemsFrame)
itemsViewer.pack(padx=2, pady=5, fill=BOTH)

viewToolsButton = Button(itemsFrame, text="Tools", command=showTools)
viewToolsButton.pack(side=RIGHT, padx=2, pady=5, fill=BOTH)

viewSeedsButton = Button(itemsFrame, text="Seeds", command=showCrops)
viewSeedsButton.pack(padx=2, pady=5, fill=BOTH)

viewDecorationButton = Button(itemsFrame, text="Decoration", command=showDecoration)
viewDecorationButton.pack(padx=2, pady=5, fill=BOTH)

itemsFrame.pack(anchor=N, pady=5, padx=2, fill=BOTH)

#Settings
settingsFrame = LabelFrame(sideBar, text="Settings")

viewToolsButton = Button(settingsFrame, text="Save", state=DISABLED)
viewToolsButton.pack(padx=2, pady=5, fill=BOTH)

viewSeedsButton = Button(settingsFrame, text="Load", state=DISABLED)
viewSeedsButton.pack(padx=2, pady=5, fill=BOTH)

viewSeedsButton = Button(settingsFrame, text="Settings", state=DISABLED)
viewSeedsButton.pack(padx=2, pady=5, fill=BOTH)


settingsFrame.pack(anchor=S, fill=BOTH)

sideBar.grid(column=1, row=0, sticky=N)

showTools()
root.mainloop()