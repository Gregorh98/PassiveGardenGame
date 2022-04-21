from tkinter import *
import datetime
import random


class Plant():
    def __init__(self, name):
        self.states = {"placed": 0,
                       "buried": 1,
                       "grown": 2}
        self.name = name
        self.growTime = crops[name]["growTime"]
        self.harvestYield = crops[name]["harvestYield"]
        self.seedColour = crops[name]["seedColour"]
        self.plantedOn = todaysDate
        self.harvestDate = self.plantedOn + datetime.timedelta(days=self.growTime)
        self.state = self.states["placed"]
        self.maxDryDaysBeforeDeath = 4

    def kill(self):
        print("plant is dead")

    def grow(self):
        print("plant is ready")

    def draw(self, x, y):
        offset = random.choice(range(int((0 - gridSize) / 4), int((gridSize / 4))))
        self.seed = garden.create_oval(
            x + (gridSize / 3) + offset,
            y + (gridSize / 3) + offset,
            x + gridSize - (gridSize / 3) + offset,
            y + gridSize - (gridSize / 3) + offset,
            fill=self.seedColour)

        garden.tag_bind(self.seed, "<ButtonPress-1>", self.mouse_click)

    def mouse_click(self, event):
        currentItem = itemsViewer.get(itemsViewer.curselection())
        if currentItem == "Trowel":
            self.burySeed()

    def burySeed(self):
        garden.delete(self.seed)
        self.state = self.states["buried"]


class Plot:
    def __init__(self, x, y):
        # State
        self.states = {"grass": 0,
                       "tilledLand": 1,
                       "planted": 3,
                       "dry": 4}
        self.state = self.states["grass"]

        # Location
        self.x = x
        self.y = y

        # Planted Item
        self.plant = None

        # Soil dryness
        self.dry = True
        self.dateWatered = None

    def getDaysSinceLastWatered(self):
        if self.dateWatered is not None:
            return todaysDate - self.dateWatered
        else:
            return -1

    def draw(self):
        self.graphicalPlot = garden.create_rectangle(x, y, x + gridSize, y + gridSize, fill=cGrass,
                                                     outline=cGrassOutline)
        garden.tag_bind(self.graphicalPlot, "<ButtonPress-1>", self.mouse_click)

    def mouse_click(self, event):
        currentItem = itemsViewer.get(itemsViewer.curselection())
        if currentItem == "Hoe":
            self.hoeGround()
        elif currentItem == "Watering Can":
            self.waterGround()
        elif currentItem == "Trowel":
            return
        else:
            # Seed
            self.plantGround(currentItem)

    def hoeGround(self):
        if self.state != self.states["tilledLand"]:
            garden.itemconfig(self.graphicalPlot, fill=cTilledLand, outline=cTilledLandOutline)
            self.state = self.states["tilledLand"]
            print("Tilled")

    def plantGround(self, plant):
        if self.state == self.states["tilledLand"]:
            # garden.itemconfig(self.graphicalPlot, fill=cDryLand, outline=cTilledLandOutline)
            self.plant = Plant(plant)
            self.plant.draw(self.x, self.y)
            self.state = self.states["planted"]
            print("Planted")

    def waterGround(self):
        if self.state == self.states["planted"]:
            if self.plant.state == self.plant.states["buried"]:
                if self.dry == True:
                    garden.itemconfig(self.graphicalPlot, fill=cWetLand, outline=cGrassOutline)
                    self.lastWatered = todaysDate
                    self.dry = False
                    print("Watered")

    def update(self):
        #Dry plot out each day
        if self.getDaysSinceLastWatered() > 0:
            self.state = self.dry = True

        if self.plant is not None:
            #Kill plant if plot unwatered
            if self.getDaysSinceLastWatered() > self.plant.maxDryDaysBeforeDeath:
                self.plant.kill()

            #Check to grow plant
            if self.state == self.states["planted"]:
                if todaysDate == self.plant.harvestDate:
                    self.plant.grow()


# Initialise Root
root = Tk()
root.resizable(False, False)

# System variables
canvasHeight = 640
canvasWidth = 640
gridSize = 32
tools = ["Hoe", "Trowel", "Watering Can", "Netting", "Fork"]
# crops       = ["Potato", "Peas", "Strawberry", "Corn", "Broccoli"]
crops = {"Broccoli": {"growTime": 30, "harvestYield": 1, "seedColour": "black", "readyColour": "Purple"},
         "Potato": {"growTime": 15, "harvestYield": 8, "seedColour": "yellow", "readyColour": "yellow"}}
decoration = ["Path", "Fence"]
gardenData = []
todaysDate = datetime.datetime.today().date()
soilDryTime = 1

# Colours
cTilledLand = "#52402a"
cTilledLandOutline = "#39301d"
cDryLand = "#6b584a"
cWetLand = "#482f1f"
cGrass = "#2c3c1e"
cGrassOutline = "#202a15"
cPath = "#a9b1b7"

# Canvas
garden = Canvas(root)
garden.configure(background=cGrass, height=canvasHeight, width=canvasWidth)
garden.grid(column=0, row=0, rowspan=2)

# Prepare Garden
for y in range(0, canvasHeight, 32):
    gardenData.append([])
    for x in range(0, canvasWidth, 32):
        gardenData[0 if y == 0 else int(y / gridSize)].append(Plot(x, y))
        gardenData[0 if y == 0 else int(y / gridSize)][0 if x == 0 else int(x / gridSize)].draw()


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
    for crop in crops.keys():
        itemsViewer.insert(END, crop)
    itemsViewer.select_set(0)


# Sidebar
sideBar = Frame(root)
Label(sideBar, text="Garden Game").pack(padx=2, fill=BOTH)
Label(sideBar, text=f"Date: {todaysDate}").pack(padx=2, fill=BOTH)

# Items
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

# Settings
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

# Main Gameloop
while True:
    #Update each plot
    for y in gardenData:
        for x in y:
            x.update()

    root.update()
