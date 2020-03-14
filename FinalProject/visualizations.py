# file with all the visualization code
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries
from PyQt5.Qt import Qt
import pyqtgraph as pg
import pandas
import os
import csv
import statistics
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
        print('connect')
        self.selected_point = None

        # creates the histogram
        histogram_subset = dataset.loc[dataset['name'] == names[0]]

        histogram_y, histogram_x = np.histogram(histogram_subset['price'].tolist())

        self.histogram = pg.PlotCurveItem(histogram_x, histogram_y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
        widget2.addItem(self.histogram)
        widget2.setLabel('left', '# of Occurrences')
        widget2.setLabel('bottom', 'Price (USD)')
        widget2.setTitle(names[0].capitalize() + ' Price Histogram')
        self.widget2 = widget2

    def update_histogram(self, name):
        histogram_subset = dataset.loc[dataset['name'] == name]

        histogram_y, histogram_x = np.histogram(histogram_subset['price'].tolist())
        self.histogram.setData(histogram_x, histogram_y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
        self.widget2.setTitle(name.capitalize() + ' Price Histogram')

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

class bar_chart(QtWidgets.QWidget):

    def __init__(self, items, freqs, value=True, parent=None):

        QtWidgets.QWidget.__init__(self, parent)
        price_dict = {}
        weight_dict = {}
        type_dict = {}
        with open('project_dataset.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(reader)
            for row in reader:
                if row[0] not in price_dict.keys():
                    price_dict[row[0]] = []
                    weight_dict[row[0]] = []
                    type_dict[row[0]] = row[1]
                price_dict[row[0]].append(float(row[2]))
                weight_dict[row[0]].append(float(row[3]))
        average_prices = {}
        average_weights = {}
        for key in price_dict.keys():
            average_prices[key] = statistics.mean(price_dict[key])
            average_weights[key] = statistics.mean(weight_dict[key])

        entries = []
        type_entries = [0, 0, 0]

        if value:
            value_dict = average_prices
        else:
            value_dict = average_weights

        for i in range(len(items)):
            item = items[i]
            freq = freqs[i]
            entries.append(freq * value_dict[item])
            if type_dict[item] == 'electronics':
                type_entries[0] += freq * value_dict[item]
            elif type_dict[item] == 'furniture':
                type_entries[1] += freq * value_dict[item]
            else:
                type_entries[2] += freq * value_dict[item]

        self.set0 = QBarSet('Electronics')
        self.set1 = QBarSet('Furniture')
        self.set2 = QBarSet('Sports Equipment')

        self.set0.append([type_entries[0]])
        self.set1.append([type_entries[1]])
        self.set2.append([type_entries[2]])

        self.series = QBarSeries()
        self.series.append(self.set0)
        self.series.append(self.set1)
        self.series.append(self.set2)

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle('Value by category')
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        months = ('Price By Category')

        axisX = QBarCategoryAxis()
        axisX.append(months)

        axisY = QValueAxis()
        axisY.setRange(0, 15)

        self.chart.addAxis(axisX, Qt.AlignBottom)
        self.chart.addAxis(axisY, Qt.AlignLeft)

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        self.chartView = QChartView(self.chart)

        self.set0.clicked.connect(self.click)

        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.chartView, 0, 0)
        self.setLayout(self.grid)

    def click(self):
        print('clicked 0')

    def mouseClickEvent(self, event):
        print("clicked")

    def onClick(self, _, points_list):
        point = points_list[0]
        print (point)



# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    # for debugging purposes
    app = QtGui.QApplication([])
    mw = QtGui.QMainWindow()
    mw.resize(900,600)
    mw.resize(900, 600)
    mw.show()
    test = bar_chart(['couch', 'bed', 'laptop', 'baseball bat'], [1, 1, 1, 2])
    mw.setCentralWidget(test)

    app.exec_()  # Start QApplication event loop ***
