import sys, os, glob, math, time
from collections import namedtuple
from PyQt5 import QtCore, QtWidgets, QtSvg
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QFileDialog, QPushButton, QApplication, QTableView, QStyledItemDelegate, QStackedLayout, QDialog, QToolBar
from PyQt5.QtGui import QImage, QPixmap, QIcon, QBrush, QColor, QMouseEvent
from PyQt5.QtCore import QSize, Qt, QAbstractTableModel, QEvent, QItemSelectionModel

# Create a custom namedtuple class to hold our data.
preview = namedtuple("preview", "id title image")

NUMBER_OF_COLUMNS = 4
CELL_PADDING = 20 # all sides

###
### Main Window ----------------------------------------------------------------------------------
###
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.folderpath = "None"

        #
        # icons
        #
        self.folderIcon = QtSvg.QSvgWidget(r'icons/folder.svg')
        self.checkmarkIcon = QtSvg.QSvgWidget(r'icons/checkmark.svg')
        self.checkmarkIcon2 = QtSvg.QSvgWidget(r'icons/checkmark.svg')
        self.checkmarkIcon3 = QtSvg.QSvgWidget(r'icons/checkmark.svg')
        self.galleryIcon = QtSvg.QSvgWidget(r'icons/gallery.svg')

        #
        # main window
        #
        self.setMinimumSize(QSize(980, 640))    
        self.setWindowTitle("PictureSort")
        self.setWindowIcon(QIcon(r'img/gallery.png'))
        self.setStyleSheet("QMainWindow {\
                               background-color: gray;\
                            }\
                            QPushButton {\
                               background-color: #adb7e6;\
                               border-style: solid;\
                               padding: 5px;\
                               border-radius: 5px;\
                            }\
                            QPushButton:hover{\
                               background-color: #ade6d1;\
                               font: bold;\
                            }\
                            QPushButton:disabled{\
                               color: gray;\
                               background-color: #c4c4c4;\
                            }")
        self.folderIcon.setGeometry(250,300,50,50)
        self.layout().addWidget(self.folderIcon)

        self.checkmarkIcon.setGeometry(290,325,20,20)
        self.layout().addWidget(self.checkmarkIcon)
        self.checkmarkIcon.hide()

        self.galleryIcon.setGeometry(450,300,60,40)
        self.layout().addWidget(self.galleryIcon)

        self.checkmarkIcon2.setGeometry(500,325,20,20)
        self.layout().addWidget(self.checkmarkIcon2)
        self.checkmarkIcon2.hide()

        self.checkmarkIcon3.setGeometry(650,300,50,50)
        self.layout().addWidget(self.checkmarkIcon3)
        self.checkmarkIcon3.hide()
        
        self.folderbutton = QPushButton('Select Folder',self)
        self.folderbutton.clicked.connect(self.folderMethod)
        self.folderbutton.resize(150,40)
        self.folderbutton.move(200, 350)

        self.picturebutton = QPushButton('Start Sorting', self)
        self.picturebutton.clicked.connect(self.pictureMethod)
        self.picturebutton.resize(150, 40)
        self.picturebutton.move(400, 350)
        self.picturebutton.setEnabled(False)

        self.finishbutton = QPushButton('Commit Order', self)
        self.finishbutton.clicked.connect(self.commitMethod)
        self.finishbutton.resize(150, 40)
        self.finishbutton.move(600, 350)
        self.finishbutton.setEnabled(False)

        self.helpbutton = QPushButton('', self)
        self.helpbutton.clicked.connect(self.showHelp)
        self.helpbutton.resize(40, 40)
        self.helpbutton.move(940,0)
        self.helpbutton.setIcon(QIcon(r'img/questionmark.png'))

        #
        # table view: image selector
        #
        self.view = MyTableView()
        self.view.setMinimumSize(QSize(980, 640)) 
        self.view.horizontalHeader().hide()
        self.view.verticalHeader().hide()
        self.view.setGridStyle(Qt.NoPen)

        delegate = PreviewDelegate()
        self.view.setItemDelegate(delegate)
        self.model = PreviewModel()
        self.view.setModel(self.model)

        self.view.setStyleSheet("MyTableView{\
                                    background-color: gray;\
                                    margin: 60px;\
                                 }\
                                 MyTableView::item:selected{\
                                    background-color: #adb7e6;\
                                 }")
        self.view.setSelectionMode(2) #multi selection mode

        #
        # stacked layouts
        #
        self.stack = QStackedLayout()
        self.stack.insertWidget(0, self)
        self.stack.insertWidget(1, self.view)
        
    def folderMethod(self):
        self.folderpath  = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a folder for sorting pictures')
        self.picturebutton.setEnabled(True)
        self.checkmarkIcon.show()

    def pictureMethod(self, win):
        # fill with pictures
        #
        os.chdir(self.folderpath)
        for n, fn in enumerate(glob.glob("*.jpg")):
            image = QImage(fn)
            self.view.addFileList(fn)
            item = preview(n, fn, image)
            self.model.previews.append(item)
        self.model.layoutChanged.emit()
        self.view.resizeRowsToContents()
        self.view.resizeColumnsToContents()

        tbar = QToolBar('titletitle', self.view)
        tbar.resize(100,32)
        
        exitbutton = QPushButton('Exit Sort View', tbar)
        exitbutton.clicked.connect(self.exitMethod)
        exitbutton.resize(100, 32)
        exitbutton.move(0, 0)
        exitbutton.setStyleSheet("QPushButton {\
                                     background-color: #adb7e6;\
                                     border-style: solid;\
                                     padding: 2px;\
                                     border-radius: 5px;\
                                  }\
                                  QPushButton:hover{\
                                     background-color: #ade6d1;\
                                     font: bold;\
                                  }")
        
        # show sort widget
        self.stack.setCurrentIndex(1)
        self.checkmarkIcon2.show()
        self.checkmarkIcon3.show()
                
    def commitMethod(self):
        self.writeMetaData(self.view.exportCurrentOrder())
        self.picturebutton.setEnabled(False)
        self.finishbutton.setEnabled(False)
        self.checkmarkIcon.hide()
        self.checkmarkIcon2.hide()
        self.checkmarkIcon3.hide()

        # clean up
        self.view.clearFileList()
        self.model.clearPreview()

    def exitMethod(self):
        # show main window again
        self.finishbutton.setEnabled(True)
        self.stack.setCurrentIndex(0)

    def writeMetaData(self, newOrder):
        if len(newOrder) > 0:
            startTime = os.path.getmtime(newOrder[0])
            i = 0
            while(i < len(newOrder)):
                os.utime(newOrder[i], (time.time(), startTime + i*60))
                print(str(startTime+i))
                i = i + 1
                i = 0
        
    def showHelp(self):
        helpDiag = QDialog(self)
        helpDiag.setWindowTitle('Picture Sort - Help')
        helpDiag.setGeometry(500,500,400,200)
        text = QLabel(helpDiag)
        text.setText('\
PictureSort is a small application and changes the modification date of pictures to sort it in your wished order.\n\
1. Select the folder where your .jpgs are.\n\
2. Choose your order: \n\
\tLeft click adds the picture to you selection following order of clicks.\n\
\tRight click removes the latest picture from your ordered selection.\n\
3. When ready, exit the gallery view.\n\
4. Commit your order to write the new meta data to your .jpgs.\n\
Author: Daniel Adlkofer\
                    ')
        helpDiag.show()
        
###
### Delegate -----------------------------------------------------------------------------------------------
###
class PreviewDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        # data is our preview object
        data = index.model().data(index, Qt.DisplayRole)
        if data is None:
            return
        
        width = option.rect.width() - CELL_PADDING * 2
        height = option.rect.height() - CELL_PADDING * 2

        # option.rect holds the area we are painting on the widget (our table cell)
        # scale our pixmap to fit
        scaled = data.image.scaled(
            width,
            height,
            aspectRatioMode=Qt.KeepAspectRatio,
        )
        # Position in the middle of the area.
        x = CELL_PADDING + (width - scaled.width()) / 2
        y = CELL_PADDING + (height - scaled.height()) / 2

        #self.initStyleOption(option, index)
        painter.drawImage(option.rect.x() + int(x), option.rect.y() + int(y), scaled)

        
    def sizeHint(self, option, index):
        # All items the same size.
        return QSize(300, 200)
    
    #def initStyleOption(self, option, index):
    #    super().initStyleOption(option, index)
    #    if (index.row() == 1 and index.column() == 0 ):
    #        option.backgroundBrush = QBrush(QColor(173, 183, 230))
    #        print('initStyle')
    
    #coordinates in table rows(x)/columns(y)
    #def select(self, index):
       # painter.fillRect(option.rect, QBrush(Qt.red)) > rect in color
       # print(index.model().data(index, Qt.DisplayRole)) > preview
       # print (index.model().data(index, Qt.DisplayRole).title) > filename
       # print (index.model().data(index, Qt.DisplayRole).id) > id

    
###
### Preview ---------------------------------------------------------------------
###

class PreviewModel(QAbstractTableModel):
    def __init__(self, todos=None):
        super().__init__()
        # .data holds our data for display, as a list of Preview objects.
        self.previews = []

    def data(self, index, role):
        try:
            data = self.previews[index.row() * 4 + index.column() ]
        except IndexError:
            # Incomplete last row.
            return
            
        if role == Qt.DisplayRole:
            return data   # Pass the data to our delegate to draw.
           
        if role == Qt.ToolTipRole:
            return data.title

        #if role == Qt.BackgroundRole: # and index.row() == index.row() == 0 and index.column() == 3:
        #    return QBrush(QColor(QColor(173, 183, 230)) )
            
    def columnCount(self, index):
        return NUMBER_OF_COLUMNS

    def rowCount(self, index):
        n_items = len(self.previews)
        return math.ceil(n_items / NUMBER_OF_COLUMNS)

    def clearPreview(self):
        self.previews = []
###
### inheriting from QTableView --------------------------------------------------------------------
###
class MyTableView(QTableView):
    def __init__(self):
        self.currentOrder = []
        self.fileList = []
        QTableView.__init__(self)
    
    def mousePressEvent(self, event):
        if event.type() == QEvent.MouseButtonPress:
            initialIndex = self.rowAt(event.y())*NUMBER_OF_COLUMNS + self.columnAt(event.x())
            if initialIndex < len(self.fileList):
                if event.button() == Qt.LeftButton:
                    #self.selectRow(event.y())
                    # entry in fileList = y*NUMBER_OF_COLUMNS + x
                    initialIndex = self.rowAt(event.y())*NUMBER_OF_COLUMNS + self.columnAt(event.x())
                    print(initialIndex)
                    self.addToOrder(self.fileList[initialIndex])
                    super().mousePressEvent(event)
                    print(self.currentOrder)
                elif event.button() == Qt.RightButton:
                    self.removeLastFromOrder()
                    # change right to left: this will give the right selection behaviour for the super call
                    leftButtonEvent = QMouseEvent(QEvent.MouseButtonPress, event.pos(), Qt.LeftButton, event.buttons(), event.modifiers())
                    super().mousePressEvent(leftButtonEvent)
                    print(self.currentOrder)
              
    def addToOrder(self, pic):
        self.currentOrder.append(pic)

    def removeLastFromOrder(self):
        if len(self.currentOrder) > 0:
            self.currentOrder.pop()

    def addFileList(self, fn):
        self.fileList.append(fn)
        
    def exportCurrentOrder(self):
        return self.currentOrder

    def clearFileList(self):
        self.fileList = []
        self.currentOrder = []
        self.clearSelection()
                
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )
