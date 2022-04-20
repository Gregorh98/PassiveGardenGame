from tkinter import *
from math import floor, ceil


class Plot():
    def __init__(self, x, y, gridPlot):
        self.states = {"Empty"  : 0,
                       "Tilled" : 1}
        self.x = x
        self.y = y
        self.gridPlot = gridPlot
        self.state = None

    def hoe(self):
        self.state = self.states["Tilled"]


root = Tk()
root.resizable(False, False)

canvasHeight    = 320
canvasWidth     = 320
gridSize        = 32
tools       = ["Hoe", "Watering Can", "Trowel", "Dibber", "Fork", "Netting"]
crops       = ["Potato", "Peas", "Strawberry", "Corn", "Broccoli"]
decoration  = ["Path", "Fence"]
gardenData  = []


def gardenClicked(event):
    clickedPoint = {"x1": floor(event.x/gridSize), "y1": floor(event.y/gridSize), "x2": ceil(event.x/gridSize), "y2": ceil(event.y/gridSize)}
    print(clickedPoint)
    print(event.x, event.y)
    garden.create_rectangle(clickedPoint["x1"]*gridSize, clickedPoint["y1"]*gridSize, clickedPoint["x2"]*gridSize, clickedPoint["y2"]*gridSize, fill="brown", outline="black")


garden = Canvas(root)
garden.bind("<Button-1>", gardenClicked)
garden.configure(background="green", height=canvasHeight, width=canvasWidth)
garden.grid(column=0, row=0, rowspan=2)

#prepareGarden
for y in range(0, gridSize, canvasHeight):
    gardenData.append([])
    for x in range(0, gridSize, canvasWidth):
        gardenData[y].append(Plot(x, y, garden.create_rectangle(clickedPoint["x1"]*gridSize, clickedPoint["y1"]*gridSize, clickedPoint["x2"]*gridSize, clickedPoint["y2"]*gridSize, fill="brown", outline="black")))

print(gardenData)

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