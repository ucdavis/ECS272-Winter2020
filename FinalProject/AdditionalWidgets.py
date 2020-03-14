'''Contains custom QWidgets
Copyright Renkert Oil LLC 2019. All rights reserved'''

from PyQt5 import QtWidgets, QtCore, QtGui

'''QWidget that brings up file explorer and returns string of file location'''
class FileEntry(QtWidgets.QWidget):
    '''Creates a entry box and an associated browse button'''
    def __init__(self, parent=None, t='file'):
        
        QtWidgets.QWidget.__init__(self, parent)
        
        self.type = t #Type is 'file' or 'folder' (what you want to open)
        
        self.grid = QtWidgets.QGridLayout()
        
        self.entry_box = QtWidgets.QLineEdit(self)
        self.grid.addWidget(self.entry_box, 0, 0)
        
        self.browse_button = QtWidgets.QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse_files)
        self.grid.addWidget(self.browse_button, 0, 1)
        
        self.textChanged = self.entry_box.textChanged
        
        self.setLayout(self.grid)
        self.show()
    
    def browse_files(self):
        if self.type == 'file':
            '''NOTE: Name is coming in as a tuple for some reason. 
            Maybe part of the Qt5 change? in any case, this should
            be investiaged to ensure that it will always be a tuple'''
            name = QtWidgets.QFileDialog.getOpenFileName(self, 'Browse Files') 
        else:
            name = QtWidgets.QFileDialog.getExistingDirectory(self,
                'Browse Folders')
            
        if name != '': #The dialog box wasn't canceled
            self.entry_box.setText(name[0])
    
    def setText(self, text):
        self.entry_box.setText(text)

    def text(self):
        '''returns the entry_box text'''
        return self.entry_box.text()

# Credit: Jeong Hweon Woo of StackOverflow
class RangeSlider(QtWidgets.QWidget):

    def __init__(self, maxval=100):
        super().__init__()

        self.minTime = 0
        self.maxTime = 0
        self.minRangeTime = 0
        self.maxRangeTime = 0

        self.sliderMin = maxval
        self.sliderMax = maxval

        self.setupUi(self)

    def setupUi(self, RangeSlider):
        RangeSlider.setObjectName("RangeSlider")
        RangeSlider.resize(1000, 65)
        RangeSlider.setMaximumSize(QtCore.QSize(16777215, 65))
        self.RangeBarVLayout = QtWidgets.QVBoxLayout(RangeSlider)
        self.RangeBarVLayout.setContentsMargins(5, 0, 5, 0)
        self.RangeBarVLayout.setSpacing(0)
        self.RangeBarVLayout.setObjectName("RangeBarVLayout")

        self.slidersFrame = QtWidgets.QFrame(RangeSlider)
        self.slidersFrame.setMaximumSize(QtCore.QSize(16777215, 25))
        self.slidersFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.slidersFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.slidersFrame.setObjectName("slidersFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.slidersFrame)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(5, 2, 5, 2)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        ## Start Slider Widget
        self.startSlider = QtWidgets.QSlider(self.slidersFrame)
        self.startSlider.setMaximum(self.sliderMin)
        self.startSlider.setMinimumSize(QtCore.QSize(100, 5))
        self.startSlider.setMaximumSize(QtCore.QSize(16777215, 10))

        font = QtGui.QFont()
        font.setKerning(True)

        self.startSlider.setFont(font)
        self.startSlider.setAcceptDrops(False)
        self.startSlider.setAutoFillBackground(False)
        self.startSlider.setOrientation(QtCore.Qt.Horizontal)
        self.startSlider.setInvertedAppearance(True)
        self.startSlider.setObjectName("startSlider")
        self.startSlider.setValue(self.sliderMax)
        self.startSlider.valueChanged.connect(self.handleStartSliderValueChange)
        self.horizontalLayout.addWidget(self.startSlider)

        ## End Slider Widget
        self.endSlider = QtWidgets.QSlider(self.slidersFrame)
        self.endSlider.setMaximum(self.sliderMax)
        self.endSlider.setMinimumSize(QtCore.QSize(100, 5))
        self.endSlider.setMaximumSize(QtCore.QSize(16777215, 10))
        self.endSlider.setTracking(True)
        self.endSlider.setOrientation(QtCore.Qt.Horizontal)
        self.endSlider.setObjectName("endSlider")
        self.endSlider.setValue(self.sliderMax)
        self.endSlider.valueChanged.connect(self.handleEndSliderValueChange)

        #self.endSlider.sliderReleased.connect(self.handleEndSliderValueChange)

        self.horizontalLayout.addWidget(self.endSlider)

        self.RangeBarVLayout.addWidget(self.slidersFrame)

        #self.retranslateUi(RangeSlider)
        QtCore.QMetaObject.connectSlotsByName(RangeSlider)

        self.show()

    @QtCore.pyqtSlot(int)
    def handleStartSliderValueChange(self, value):
        self.startSlider.setValue(value)

    @QtCore.pyqtSlot(int)
    def handleEndSliderValueChange(self, value):
        self.endSlider.setValue(value)






