import csv
import networkx as nx
from matplotlib import pyplot as plt

from tkinter import *


def obtain_bounds(input_points):
    for item in input_points:

        if input_points.index(item) == 0:
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

    return minx, maxx, miny, maxy


def compute_cell_for_coordinate(bounds, nr_of_rows, nr_of_columns, input_points_coordinates):
    # min and max coordinates of input points:
    min_x = bounds[0]
    max_x = bounds[1]

    min_y = bounds[2]
    max_y = bounds[3]

    # the extent/spread/length of space in x and y dimension
    extent_x = max_x - min_x
    extent_y = max_y - min_y

    # Step = the size of a cell
    step_x = extent_x / nr_of_columns
    step_y = extent_y / nr_of_rows

    coordinate_and_cell = []

    for point in input_points_coordinates:

        # the coordinates of the point:
        x = float(point[1])
        y = float(point[2])

        # i and j are the indices of the row and column in the grid
        i = 1
        j = 1

        # increase the
        while min_x + i * step_x < x:
            i = i + 1

        column_index = i - 1

        while min_y + j * step_y < y:
            j = j + 1

        row_index = nr_of_rows - j - 1

        if row_index < 0:
            # TODO: temporary fix, investigate if this causes issues later
            row_index = abs(row_index)

        coordinate_and_cell.append((point, column_index, row_index))

    return coordinate_and_cell


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
    IS_SOURCE_OR_DESTINATION_CELL = False

    def __init__(self, master, x, y, size):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x  # abs = x coordinate
        self.ord = y  # ord = y coordinate
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
            # self.master.create_text((xmin + self.size/2, ymin + self.size/2), text="")


class CellGrid(Canvas):
    def __init__(self, master, rowNumber, columnNumber, cellSize, coordinate_and_cell, *args, **kwargs):
        Canvas.__init__(self, master, width=cellSize * columnNumber, height=cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize

        self.grid = []

        # Structure of grid:
        # grid[line][column] = cell

        for row in range(rowNumber):

            column = []
            for col in range(columnNumber):
                column.append(Cell(self, col, row, cellSize))

            self.grid.append(column)

        for point_info in coordinate_and_cell:
            row = point_info[2]
            column = point_info[1]

            self.grid[row][column].height = 100

            # xmin = self.abs * self.size
            # xmax = xmin + self.size
            # ymin = self.ord * self.size
            # ymax = ymin + self.size
            #
            # self.master.create_text((xmin + self.size / 2, ymin + self.size / 2), text="aa")

            # print()

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

        self.bind("<MouseWheel>", self.do_zoom)

        self.draw()

        self.draw_text_in_cells(coordinate_and_cell=coordinate_and_cell)

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def draw_text_in_cells(self, coordinate_and_cell):

        # for row in self.grid:
        #     for cell in row:
        #
        #         xmin = cell.abs * cell.size
        #         xmax = xmin + cell.size
        #         ymin = cell.ord * cell.size
        #         ymax = ymin + cell.size
        #
        #         cell.master.create_text((xmin + cell.size / 2, ymin + cell.size / 2), text="aa")

        for point_info in coordinate_and_cell:
            row_id = point_info[2]
            column_id = point_info[1]

            row = self.grid[row_id]
            cell = row[column_id]

            xmin = cell.abs * cell.size
            xmax = xmin + cell.size
            ymin = cell.ord * cell.size
            ymax = ymin + cell.size

            text = point_info[0][0]

            cell.master.create_text((xmin + cell.size / 2, ymin + cell.size / 2), text=text)

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

    def do_zoom(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        factor = 1.001 ** event.delta
        self.scale(ALL, x, y, factor, factor)

def import_points():
    with open(r"C:\Users\20175326\Desktop\Thesis\Data\USPos.csv", newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    data_processed = []

    for item in data:
        data_processed.append((item[0].split(";")[0], float(item[0].split(";")[1]), float(item[0].split(";")[2])))

    return data_processed


if __name__ == '__main__':
    # bounds = [minx, maxx, miny, maxy]

    NR_OF_ROWS = 120
    NR_OF_CELLS = 120
    CELL_SIZE = 7

    input_points = import_points()

    bounds = obtain_bounds(input_points)

    coordinate_and_cell = compute_cell_for_coordinate(bounds=bounds, nr_of_rows=NR_OF_ROWS, nr_of_columns=NR_OF_CELLS, input_points_coordinates=input_points)

    app = Tk()
    grid = CellGrid(master=app, rowNumber=NR_OF_ROWS, columnNumber=NR_OF_CELLS, cellSize=CELL_SIZE, coordinate_and_cell=coordinate_and_cell)
    grid.pack()
    app.mainloop()
