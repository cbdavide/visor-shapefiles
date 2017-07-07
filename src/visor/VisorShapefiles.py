# -*- coding: utf-8 -*-

import sys

from PyQt4.QtCore import SIGNAL, QFileInfo, QPoint, QByteArray
from PyQt4.QtGui import QMainWindow, QColor, QIcon, QVBoxLayout, QAction, QFileDialog
from PyQt4.QtGui import QApplication, QWidget, QImage, QPainter

from WindowUI import Ui_MainWindow

from mapnikwidget import MapnikWidget

class VisorShapefiles(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.setWindowTitle(u'Visor de Shapefiles')

        self.layout = QVBoxLayout(self.frame)

        maper = MapnikWidget(self.frame)
        maper.createMap()

        # canvas = QCanvas()

        self.layout.addWidget(maper)



        # TODO: Move all the declarations of the actions
        self.actionAddLayer = QAction(QIcon('images/mActionAddOgrLayer.svg'), u'Agregar capa',self.frame)
        self.connect(self.actionAddLayer, SIGNAL('activated()'), self.addLayer)

        self.actionZoomIn = QAction(QIcon('images/mActionZoomIn.svg'), u'Acercar', self.frame)
        self.connect(self.actionZoomIn, SIGNAL('activated()'), self.zoomIn)

        self.actionZoomOut = QAction(QIcon('images/mActionZoomOut.svg'), u'Alejar', self.frame)
        self.connect(self.actionZoomOut, SIGNAL('activated()'), self.zoomOut)

        self.actionMove = QAction(QIcon('images/mActionPan.svg'), u'Mover', self.frame)
        self.connect(self.actionMove, SIGNAL('activated()'), self.pan)

        self.actionZoomFull = QAction(QIcon('images/mActionZoomFullExtent.svg'), u'Vista Completa', self.frame)
        self.connect(self.actionZoomFull, SIGNAL('activated()'), self.zoomFull)

        self.actionPoint = QAction(QIcon('images/mActionCapturePoint.svg'), u'Capturar Punto', self.frame)
        self.actionPoint.setCheckable(True)
        self.connect(self.actionPoint, SIGNAL('triggered()'), self.point)

        # self.actionPoly = QAction(QIcon('images/mActionCapturePolygon.svg'), u'Capturar Polígono', self.frame)
        # self.actionPoly.setCheckable(True)
        # self.connect(self.actionPoly, SIGNAL('triggered()'), self.poly)

        self.toolbar = self.addToolBar('Map')
        self.toolbar.addAction(self.actionAddLayer)
        self.toolbar.addAction(self.actionZoomIn)
        self.toolbar.addAction(self.actionZoomOut)
        self.toolbar.addAction(self.actionMove)
        self.toolbar.addAction(self.actionZoomFull)
        self.toolbar.addAction(self.actionPoint)
        # self.toolbar.addAction(self.actionPoly)

        self.layers = []

        self.show()

    def poly(self):
        pass

    def point(self):
        pass

    def zoomIn(self):
        pass

    def zoomOut(self):
        pass

    def pan(self):
        pass

    def zoomFull(self):
        pass

    def addLayer(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VisorShapefiles()
    sys.exit(app.exec_())
