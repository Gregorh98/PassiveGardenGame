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

canvasHeight    = 1024
canvasWidth     = 1024
gridSize        = 32
tools = ["Hoe", "Watering Can", "Trowel", "Dibber", "Fork", "Netting"]
crops = ["Potato", "Peas", "Strawberry", "Corn", "Broccoli"]
gardenData = []

def gardenClicked(event):
    print((event.x, event.y))
    print( ((floor(event.x/32), floor(event.y/32))),((ceil(event.x/32), ceil(event.y/32))) )

garden = Canvas(root)
garden.bind("<Button-1>", gardenClicked)
garden.configure(background="green", height=canvasHeight, width=canvasWidth)
garden.grid(column=0, row=0, rowspan=2)

#prepareGarden
"""for y in range(0, gridSize, canvasHeight):
    gardenData.append([])
    for x in range(0, gridSize, canvasWidth):
        gardenData[y].append(Plot(x/gridSize, y/gridSize, garden.create_rectangle(x, y, x+gridSize, y+gridSize, outline="darkgreen")))"""

def showTools():
    itemsViewer.delete(0, END)
    for tool in tools:
        itemsViewer.insert(END, tool)
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