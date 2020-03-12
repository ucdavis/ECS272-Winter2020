# file with all the visualization code
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pandas
import os
import numpy as np

relative_path = os.path.join('.', 'project_dataset.csv')
dataset = pandas.read_csv(relative_path)

class scatter_plot_histogram:
    # accepts a list of the masked images and a list of each name's frequency
    # if the image has 5 sofas, then name[x] = sofa and freqs[x] = 5
    # creates a price/weight scatter plot using the inputted data
    def __init__(self, widget1, widget2, names, freqs):
        avg_price_list = []
        avg_weight_list = []
        size_list = []

        # creates the scatter plot's entries
        num_unique_items = len(names)
        for index in range(num_unique_items):
            subset = dataset.loc[dataset['name'] == names[index]]
            avg_price = round(subset['price'].mean(), 2)
            avg_weight = round(subset['weight'].mean(), 2)

            avg_price_list.append(avg_price)
            avg_weight_list.append(avg_weight)
            size_list.append(freqs[index] * 10)

        # creates the scatter plot
        self.plot_points = pg.ScatterPlotItem(avg_weight_list, avg_price_list, size=size_list, pen=pg.mkPen(width=1, color=(0, 0, 0)),
                                                 data=names, brush=pg.mkBrush(0, 0, 255, 120))
        widget1.addItem(self.plot_points)
        widget1.setLabel('left', 'Average Price (USD)')
        widget1.setLabel('bottom', 'Average Weight (Kg)')
        widget1.setTitle('Price Vs Wgt Scatter Plot')
        self.widget1 = widget1

        # creates the scatter plot's tooltip
        self.tooltip = pg.TextItem(text='', color=(176, 23, 31), anchor=(0, 1), border='w', fill='w')
        self.tooltip.hide()
        widget1.addItem(self.tooltip)

        # adds embedded interactions
        self.plot_points.scene().sigMouseMoved.connect(self.onMove)
        self.plot_points.sigClicked.connect(self.onClick)
        self.selected_point = None

        # creates the histogram
        histogram_subset = dataset.loc[dataset['name'] == names[0]]

        histogram_y, histogram_x = np.histogram(histogram_subset['price'].tolist())

        self.histogram = pg.PlotCurveItem(histogram_x, histogram_y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
        widget2.addItem(self.histogram)
        widget2.setLabel('left', '# of Occurrences')
        widget2.setLabel('bottom', 'Price (USD)')
        widget2.setTitle(names[0].capitalize() + ' Price Histogram')

    def update_histogram(self, name):
        histogram_subset = dataset.loc[dataset['name'] == name]

        histogram_y, histogram_x = np.histogram(histogram_subset['price'].tolist())
        self.histogram.setData(histogram_x, histogram_y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))

    def onMove(self, pos):
        act_pos = self.plot_points.mapFromScene(pos)
        points_list = self.plot_points.pointsAt(act_pos)

        # if at least one point is hovered over
        if len(points_list) > 0:
            point = points_list[0]

            # highlights the point that was hovered over and un-highlights the previous point
            if self.selected_point is not None and self.selected_point is not point:
                self.selected_point.setBrush(0, 0, 255, 80)
            self.selected_point = point
            self.selected_point.setBrush(100, 100, 255, 80)

            # updates and shows the tooltip
            tooltip_text = 'name: ' + point.data() + '\navg price: $' + str(point.pos()[1]) + \
                           '\navg wgt: ' + str(point.pos()[0]) + ' Kg'
            self.tooltip.setText(tooltip_text)

            # gets the mouse position and the plot's max x an y values
            x_max = self.widget1.getAxis('bottom').range[1]
            y_max = self.widget1.getAxis('left').range[1]
            x_pos = point.pos()[0]
            y_pos = point.pos()[1]

            # if the mouse is close to the right or left of the plot's edge
            # set the anchor to the tooltip's top right
            if (3 * x_max / 4) < x_pos or (3 * y_max / 4) < y_pos:
                self.tooltip.setAnchor((1, 0))
            # else, set the anchor to the tooltip's bottom left
            else:
                self.tooltip.setAnchor((0, 1))

            # sets the tooltip's position and makes it viewable
            self.tooltip.setPos(point.pos()[0], point.pos()[1])
            self.tooltip.show()

        # if no point is hovered over
        else:
            # hides the tooltip
            self.tooltip.hide()

            # un-highlights the point that was hovered over
            if self.selected_point is not None:
                self.selected_point.setBrush(0, 0, 255, 80)
                self.selected_point = None

    def onClick(self, _, points_list):
        if len(points_list) > 0:
            point = points_list[0]
            self.update_histogram(point.data())

# for debugging purposes
app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.resize(900,600)
view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
mw.setCentralWidget(view)
mw.show()

## create 2 areas to add plots
w1 = view.addPlot()
w2 = view.addPlot()
test = scatter_plot_histogram(w1, w2, ['couch', 'bed'], [1, 2])


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':

    app.exec_()  # Start QApplication event loop ***
