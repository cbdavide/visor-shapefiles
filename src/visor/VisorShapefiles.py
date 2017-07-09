# -*- coding: utf-8 -*-

import sys

from PyQt4.QtCore import SIGNAL, QFileInfo, QPoint, QByteArray
from PyQt4.QtGui import QMainWindow, QColor, QVBoxLayout, QAction, QFileDialog
from PyQt4.QtGui import QApplication, QWidget, QImage, QPainter, QToolBar

from util import IconFactory

from WindowUI import Ui_MainWindow

from mapnikwidget import MapnikWidget

class MapToolBar(QToolBar):
    def __init__(self, title, parent):
        QToolBar.__init__(self, title, parent)

        self.actions = []
        self.parent = parent

        self.buildActions()
        self.configActions()
        self.addActions()

    def buildActions(self):
        self.actions.append(QAction(IconFactory.createOpenIcon(), u'Agregar capa',self))
        self.actions.append(QAction(IconFactory.cretatePanIcon(), u'Mover', self))
        self.actions.append(QAction(IconFactory.createZoomInIcon(), u'Acercar', self))
        self.actions.append(QAction(IconFactory.createZoomOutIcon(), u'Alejar', self))
        self.actions.append(QAction(IconFactory.createZoomFullIcon(), u'Vista Completa', self))
        self.actions.append(QAction(IconFactory.createPointIcon(), u'Capturar Punto', self))

    def configActions(self):
        self.connect(self.actions[0], SIGNAL('triggered()'), self.parent.addLayer)

        self.actions[1].setCheckable(True)
        self.connect(self.actions[1], SIGNAL('triggered()'), self.parent.pan)

        self.actions[2].setCheckable(True);
        self.connect(self.actions[2], SIGNAL('triggered()'), self.parent.zoomIn)

        self.actions[3].setCheckable(True);
        self.connect(self.actions[3], SIGNAL('triggered()'), self.parent.zoomOut)

        self.connect(self.actions[4], SIGNAL('triggered()'), self.parent.zoomFull)

        self.actions[5].setCheckable(True)
        self.connect(self.actions[5], SIGNAL('triggered()'), self.parent.point)


    def addActions(self):
        '''Add the actions into the toolbar'''
        for action in self.actions:
            self.addAction(action)

class VisorShapefiles(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.setWindowTitle(u'Visor de Shapefiles')

        self.layout = QVBoxLayout(self.frame)

        self.map = MapnikWidget()
        self.map.createMap()

        self.layout.addWidget(self.map)

        self.toolbar = MapToolBar('Barra de Herramientas', self)
        self.addToolBar(self.toolbar)


        self.show()

    def point(self):
        pass

    def zoomIn(self):
        pass

    def zoomOut(self):
        pass

    def pan(self):
        if self.toolbar.actions[1].isChecked():
            self.map.dragEnabled = True
            self.safeCheckAction(self.toolbar.actions[1])
        else:
            self.map.dragEnabled = False

    def zoomFull(self):
        pass

    def addLayer(self):
        pass

    def safeCheckAction(self, new):
        for action in self.toolbar.actions:
            if action != new and action.isChecked():
                action.toggle()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VisorShapefiles()
    sys.exit(app.exec_())
