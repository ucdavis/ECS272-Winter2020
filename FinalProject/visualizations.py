# file with all the visualization code
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pandas
import os
import numpy as np

relative_path = os.path.join('.', 'project_dataset.csv')
dataset = pandas.read_csv(relative_path)

class scatter_plot:
    # accepts a list of the masked images and a list of each name's frequency
    # if the image has 5 sofas, then name[x] = sofa and freqs[x] = 5
    # creates a price/weight scatter plot using the inputted data
    def __init__(self, widget1, widget2, names, freqs):
        avg_price_list = []
        avg_weight_list = []
        size_list = []

        num_unique_items = len(names)
        for index in range(num_unique_items):
            subset = dataset.loc[dataset['name'] == names[index]]
            avg_price = round(subset['price'].mean(), 2)
            avg_weight = round(subset['weight'].mean(), 2)

            avg_price_list.append(avg_price)
            avg_weight_list.append(avg_weight)
            size_list.append(freqs[index] * 10)

        self.plot_points = pg.ScatterPlotItem(avg_weight_list, avg_price_list, size=size_list, pen=pg.mkPen(None),
                                                 data=names, brush=pg.mkBrush(255, 255, 255, 120))
        self.tooltip = pg.TextItem(text='', color=(176, 23, 31), anchor=(1, 1))
        self.tooltip.hide()
        widget1.addItem(self.plot_points)
        widget1.addItem(self.tooltip)
        self.plot_points.scene().sigMouseMoved.connect(self.onMove)
        self.plot_points.sigClicked.connect(self.onClick)

        # creates the histogram
        histogram_subset = dataset.loc[dataset['name'] == names[0]]

        histogram_y, histogram_x = np.histogram(histogram_subset['price'].tolist())

        self.histogram = pg.PlotCurveItem(histogram_x, histogram_y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
        widget2.addItem(self.histogram)
        self.widget2 = widget2

    def update_histogram(self, name):
        histogram_subset = dataset.loc[dataset['name'] == name]

        histogram_y, histogram_x = np.histogram(histogram_subset['price'].tolist())
        self.histogram.setData(histogram_x, histogram_y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))

    def onMove(self, pos):
        act_pos = self.plot_points.mapFromScene(pos)
        points_list = self.plot_points.pointsAt(act_pos)

        if len(points_list) > 0:
            point = points_list[0]
            tooltip_text = 'name: ' + point.data() + '\navg price: ' + str(point.pos()[1]) + \
                           '\navg wgt: ' + str(point.pos()[0])
            self.tooltip.setText(tooltip_text)
            self.tooltip.setPos(point.pos()[0], point.pos()[1])
            self.tooltip.show()

        else:
            self.tooltip.hide()

    def onClick(self, _, points_list):
        if len(points_list) > 0:
            point = points_list[0]
            self.update_histogram(point.data())

app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.resize(800,800)
view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
mw.setCentralWidget(view)
mw.show()

## create four areas to add plots
w1 = view.addPlot()
w2 = view.addPlot()
test = scatter_plot(w1, w2, ['couch', 'bed'], [1, 2])


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':

    app.exec_()  # Start QApplication event loop ***
