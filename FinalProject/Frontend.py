import sys
import webbrowser
import os
import time
import random
import string
from PyQt5 import QtCore, QtWidgets, QtGui
from AdditionalWidgets import FileEntry, RangeSlider
from shutil import copyfile
from maskImage import maskImage

'''Primary source of interaction between all kinds of users
and computer.'''
class MainWindow(QtWidgets.QMainWindow):

	def __init__(self, parent=None):
		QtWidgets.QMainWindow.__init__(self, parent)

		self.parent = parent
		self.cwd = os.getcwd()
		# this is the widget we will populate with the main menu widgets
		self.cw = QtWidgets.QWidget(self)
		self.setCentralWidget(self.cw)

		self.showMaximized()

		self.grid = QtWidgets.QGridLayout()

		self.pictures = []
		self.processed_pictures = {'category': [], 'price': [], 'weight': []}

		self.createTabs()
		self.createSetupWindow()
		self.createViewWindow()
		self.createAnalysisWindow()

		self.connect_widgets()

		self.cw.setLayout(self.grid)

		screenShape = QtWidgets.QDesktopWidget().screenGeometry(self)
		self.width = 3.0 * screenShape.width() / 9.0
		self.height = 3.0 * screenShape.height() / 4.0
		self.resize(self.width, self.height)

	def createTabs(self):
		self.tab_widget = QtWidgets.QTabWidget()
		# Create tabs
		self.setup_tab = QtWidgets.QWidget()
		self.view_tab = QtWidgets.QWidget()
		self.analysis_tab = QtWidgets.QWidget()
		# Create individual tab layouts
		self.setup_tab.layout = QtWidgets.QVBoxLayout(self)
		self.view_tab.layout = QtWidgets.QVBoxLayout(self)
		self.analysis_tab.layout = QtWidgets.QVBoxLayout(self)
		# Add tabs to tab widget
		self.tab_widget.addTab(self.setup_tab, 'Setup')
		self.tab_widget.addTab(self.view_tab, 'View')
		self.tab_widget.addTab(self.analysis_tab, 'Analysis')
		# Add tab widget to MW
		self.grid.addWidget(self.tab_widget, 0, 0)

	def createSetupWindow(self):
		# Setup window grid and frame
		self.setup_grid = QtWidgets.QGridLayout()
		self.setup_frame = QtWidgets.QFrame(self.cw)
		self.setup_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.setup_frame.setFrameShape(QtWidgets.QFrame.Panel)
		# Setup widgets
		self.setup_title = QtWidgets.QLabel("Setup")
		self.setup_title.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
		self.path_entry = FileEntry()
		self.upload_button = QtWidgets.QPushButton("Upload")
		self.raw_image = QtWidgets.QLabel()
		raw_pixmap = QtGui.QPixmap(os.path.join('images', 'placeholder.jpg'))
		self.raw_image.setPixmap(raw_pixmap.scaled(480, 360))
		self.setup_prev_button = QtWidgets.QPushButton(">>")
		self.setup_next_button = QtWidgets.QPushButton("<<")
		self.advanced_label = QtWidgets.QLabel("Advanced")
		self.advanced_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
		self.prediction_confidence_label = QtWidgets.QLabel("Prediction Confidence")
		self.masking_confidence_label = QtWidgets.QLabel("Masking Confidence")
		self.prediction_confidence_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
		self.masking_confidence_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
		# Slider values
		self.prediction_confidence_slider.setMinimum(0)
		self.prediction_confidence_slider.setMaximum(100)
		self.prediction_confidence_slider.setValue(50)
		self.masking_confidence_slider.setMinimum(0)
		self.masking_confidence_slider.setMaximum(100)
		self.masking_confidence_slider.setValue(30)
		# Add setup widgets to setup grid
		self.setup_grid.addWidget(self.setup_title, 0, 0)
		self.setup_grid.addWidget(self.path_entry, 1, 0)
		self.setup_grid.addWidget(self.upload_button, 2, 0)
		self.setup_grid.addWidget(self.raw_image, 1, 1, 2, 2)
		self.setup_grid.addWidget(self.setup_next_button, 3, 1)
		self.setup_grid.addWidget(self.setup_prev_button, 3, 2)
		self.setup_grid.addWidget(self.advanced_label, 3, 0)
		self.setup_grid.addWidget(self.prediction_confidence_label, 4, 0)
		self.setup_grid.addWidget(self.prediction_confidence_slider, 5, 0, 1, 2)
		self.setup_grid.addWidget(self.masking_confidence_label, 6, 0)
		self.setup_grid.addWidget(self.masking_confidence_slider, 7, 0, 1, 2)
		# Set setup layout
		self.setup_tab.setLayout(self.setup_grid)
		# Hide hidden widgets
		self.setup_next_button.hide()
		self.setup_prev_button.hide()

	def createViewWindow(self):
		# Setup window grid and frame
		self.view_grid = QtWidgets.QGridLayout()
		self.view_frame = QtWidgets.QFrame(self.cw)
		self.view_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.view_frame.setFrameShape(QtWidgets.QFrame.Panel)
		# Setup widgets
		self.view_title = QtWidgets.QLabel("View")
		self.view_title.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
		self.view_image = QtWidgets.QLabel()
		view_pixmap = QtGui.QPixmap(os.path.join('images', 'placeholder.jpg'))
		self.view_image.setPixmap(view_pixmap.scaled(480, 360))
		self.value_lowend_label = QtWidgets.QLabel("$")
		self.price_range_slider = RangeSlider()
		self.value_highend_label = QtWidgets.QLabel("$$$")
		self.view_changer = QtWidgets.QButtonGroup()
		self.category_button = QtWidgets.QRadioButton("Category")
		self.value_button = QtWidgets.QRadioButton("Value")
		self.weight_button = QtWidgets.QRadioButton("Weight")
		self.view_changer.addButton(self.category_button)
		self.view_changer.addButton(self.value_button)
		self.view_changer.addButton(self.weight_button)
		self.category_tree = QtWidgets.QTreeWidget()
		# Populate
		self.populate_tree_widget(self.category_tree)
		# Add setup widgets to setup grid
		self.view_grid.addWidget(self.view_title, 0, 0)
		self.view_grid.addWidget(self.view_image, 1, 0, 4, 3)
		self.view_grid.addWidget(self.value_lowend_label, 5, 0)
		self.view_grid.addWidget(self.price_range_slider, 5, 1)
		self.view_grid.addWidget(self.value_highend_label, 5, 2)
		self.view_grid.addWidget(self.category_button, 1, 3)
		self.view_grid.addWidget(self.value_button, 2, 3)
		self.view_grid.addWidget(self.weight_button, 3, 3)
		self.view_grid.addWidget(self.category_tree, 4, 3)
		# Set setup layout
		self.view_tab.setLayout(self.view_grid)

	def createAnalysisWindow(self):
		# Setup window grid and frame
		self.analysis_grid = QtWidgets.QGridLayout()
		self.analysis_frame = QtWidgets.QFrame(self.cw)
		self.analysis_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.analysis_frame.setFrameShape(QtWidgets.QFrame.Panel)
		# Setup widgets
		self.analysis_title = QtWidgets.QLabel("Analysis")
		self.analysis_title.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
		self.vis_combobox = QtWidgets.QComboBox()
		self.populate_vis_combobox()
		self.analysis_category_tree = QtWidgets.QTreeWidget()
		self.analysis_image = QtWidgets.QLabel()
		analysis_pixmap = QtGui.QPixmap(os.path.join('images', 'placeholder.jpg'))
		self.analysis_image.setPixmap(analysis_pixmap.scaled(480, 360))
		self.reset_visualization_button = QtWidgets.QPushButton('Reset')
		# Populate
		self.populate_tree_widget(self.analysis_category_tree)
		# Add analysis widgets to grid
		self.analysis_grid.addWidget(self.analysis_title, 0, 0)
		self.analysis_grid.addWidget(self.analysis_image, 1, 0, 4, 3)
		self.analysis_grid.addWidget(self.vis_combobox, 1, 3)
		self.analysis_grid.addWidget(self.analysis_category_tree, 2, 3)
		self.analysis_grid.addWidget(self.reset_visualization_button, 3, 0)
		self.analysis_tab.setLayout(self.analysis_grid)

	def populate_vis_combobox(self):
		self.vis_combobox.addItem('Value Barchart')
		self.vis_combobox.addItem('Weight Barchart')
		self.vis_combobox.addItem('Value-Weight Scatterplot')
		self.vis_combobox.addItem('Alluvial Diagram')

	def populate_tree_widget(self, widget):
		widget.setHeaderHidden(True)
		parents = ['Furniture', 'Sports Equipment', 'Electronics']
		children = {'Furniture': ['Couch', 'Chair', 'Mirror', 'Dining Table'],
		'Sports Equipment': ['Baseball Glove', 'Baseball Bat', 'Bicycle', 'Tennis Racket'],
		'Electronics': ['Blender', 'Toaster', 'TV', 'Refrigerator']}
		for parent in parents:
			newEntry = QtWidgets.QTreeWidgetItem(widget)
			newEntry.setText(0, parent)
			newEntry.setFlags(newEntry.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
			newEntry.setCheckState(0, QtCore.Qt.Checked)
			widget.addTopLevelItem(newEntry)
			for child_category in children[parent]:
				child = QtWidgets.QTreeWidgetItem(newEntry)
				child.setFlags(child.flags() | QtCore.Qt.ItemIsUserCheckable)
				child.setText(0, child_category)
				child.setCheckState(0, QtCore.Qt.Checked)

	# Connect widgets

	def connect_widgets(self):
		self.connect_setup_widgets()

	def connect_setup_widgets(self):
		self.upload_button.clicked.connect(self.upload_picture)

	# Update methods

	def upload_picture(self):
		path = str(self.path_entry.text())
		if os.path.isfile(path):
			raw_pixmap = QtGui.QPixmap(path)
			self.pictures.append(raw_pixmap)
			self.raw_image.setPixmap(raw_pixmap.scaled(480, 360))
		# Mask Image
		maskImage(path)
		cat_pixmap = QtGui.QPixmap('cat.jpg')
		price_pixmap = QtGui.QPixmap('price.jpg')
		weight_pixmap = QtGui.QPixmap('weight.jpg')
		self.processed_pictures['category'].append(cat_pixmap)
		self.processed_pictures['price'].append(price_pixmap)
		self.processed_pictures['weight'].append(weight_pixmap)
		self.set_view_pixmap(cat_pixmap)

	def set_view_pixmap(self, pixmap):
		self.view_image.setPixmap(pixmap.scaled(480, 360))

'''Launches MainWindow object'''
def launch(filename=None):
	app = QtWidgets.QApplication(sys.argv)
	mw = MainWindow()
	sys.exit(app.exec_())


'''Pilot'''
launch()
