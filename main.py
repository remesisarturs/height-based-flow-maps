import csv
import networkx as nx
from matplotlib import pyplot as plt
from matplotlib import pyplot

import numpy as np
import matplotlib as mpl

from tkinter import *


def main():
    with open(r"C:\Users\20175326\Desktop\Thesis\Data\USPos.csv", newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    data_processed = []

    for item in data:
        data_processed.append((item[0].split(";")[0], float(item[0].split(";")[1]), float(item[0].split(";")[2])))

    G = nx.DiGraph()

    for item in data_processed:

        if data_processed.index(item) == 0:
            minx = item[1]
            miny = item[2]
            maxx = item[1]
            maxy = item[2]

        if item[1] < minx:
            minx = item[1]
        if item[1] > maxx:
            maxx = item[1]
        if item[2] < miny:
            miny = item[2]
        if item[2] > maxy:
            maxy = item[2]

        G.add_node(item[0], pos=(float(item[1]), float(item[2])), node_color='blue')

    plt.axvline(x=maxx)
    plt.axvline(x=minx)
    plt.axhline(y=maxy)
    plt.axhline(y=miny)

    # states = geopandas.read_file(r"C:\Users\20175326\Desktop\Thesis\Data\usa-states-census-2014.shp")
    # states = states.to_crs("EPSG:3395")
    # states.boundary.plot()

    with open(r"C:\Users\20175326\Desktop\Thesis\Data\Input_data1.csv", newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    us_state_to_abbrev = {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY",
        "District of Columbia": "DC",
        "American Samoa": "AS",
        "Guam": "GU",
        "Northern Mariana Islands": "MP",
        "Puerto Rico": "PR",
        "United States Minor Outlying Islands": "UM",
        "U.S. Virgin Islands": "VI",
    }

    data_flow = []

    for item in data:
        state_abbreviation = us_state_to_abbrev.get(item[0])
        data_flow.append([state_abbreviation, float(item[1])])

    pos = nx.get_node_attributes(G, 'pos')

    for item in data_flow:
        G.add_edge('AL', item[0], weight=item[1] / 2000)

    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    nx.draw(G, pos, width=weights, node_size=400, with_labels=True, arrowstyle='Simple')

    plt.grid()

    plt.show()
    print()


class Cell():
    EMPTY_COLOR_BG = "white"
    EMPTY_COLOR_BORDER = "black"
    MAX_HEIGHT = 255
    MIN_HEIGHT = -255
    STEP = 25

    def __init__(self, master, x, y, size):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.height = 0

    def increase_height(self):

        if self.height + Cell.STEP < Cell.MAX_HEIGHT:
            self.height = self.height + Cell.STEP

    def decrease_height(self):

        if self.height - Cell.STEP > Cell.MIN_HEIGHT:
            self.height = self.height - Cell.STEP

    def clamp(self, x):
        return max(-255, min(x, 255))

    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None:
            # fill = Cell.FILLED_COLOR_BG
            # outline = Cell.FILLED_COLOR_BORDER

            # if not self.fill:
            #    fill = Cell.EMPTY_COLOR_BG
            #    outline = Cell.EMPTY_COLOR_BORDER

            if self.height >= 0:
                fill = "#{0:02x}{1:02x}{2:02x}".format(255, 255 - self.clamp(self.height), 255 - self.clamp(self.height))
            elif self.height < 0:
                fill = "#{0:02x}{1:02x}{2:02x}".format(255 + self.clamp(self.height), 255 + self.clamp(self.height), 255)

            outline = Cell.EMPTY_COLOR_BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=fill, outline=outline)


class CellGrid(Canvas):
    def __init__(self, master, rowNumber, columnNumber, cellSize, *args, **kwargs):
        Canvas.__init__(self, master, width=cellSize * columnNumber, height=cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize

        self.grid = []

        # Structure of grid:
        # grid[line][column] = cell

        for row in range(rowNumber):

            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize))

            self.grid.append(line)

        # memorize the cells that have been modified to avoid many switching of state during mouse motion.
        self.switched = []

        # bind click action
        self.bind("<Button-1>", self.handle_mouse_click_left)
        # bind click action
        self.bind("<Button-3>", self.handle_mouse_click_right)
        # bind moving while clicking
        self.bind("<B1-Motion>", self.handle_mouse_motion_left)
        # bind moving while clicking
        self.bind("<B3-Motion>", self.handle_mouse_motion_right)
        # bind release button action - clear the memory of midified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())

        self.draw()

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def handle_mouse_click_left(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        cell.increase_height()
        cell.draw()
        # add the cell to the list of cell switched during the click
        self.switched.append(cell)

    def handle_mouse_click_right(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        cell.decrease_height()
        cell.draw()
        # add the cell to the list of cell switched during the click
        self.switched.append(cell)

    def handle_mouse_motion_left(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]

        if cell not in self.switched:
            cell.increase_height()
            cell.draw()
            self.switched.append(cell)

    def handle_mouse_motion_right(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]

        if cell not in self.switched:
            cell.decrease_height()
            cell.draw()
            self.switched.append(cell)


if __name__ == '__main__':
    main()

    # app = Tk()
    # grid = CellGrid(app, 100, 100, 10)
    # grid.pack()
    # app.mainloop()
