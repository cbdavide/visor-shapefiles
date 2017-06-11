# -*- coding: utf-8 -*-

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

from visor_shapefiles_ui import Ui_MainWindow

qgis_prefix = "/usr"

class VisorShapefiles(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.setWindowTitle(u'Visor de Shapefiles')

        self.canvas = QgsMapCanvas()
        self.canvas.setCanvasColor(QColor(255, 255, 255))
        self.canvas.enableAntiAliasing(True)
        self.canvas.useImageToRender(False)
        self.canvas.show()

        self.layout = QVBoxLayout(self.frame)
        self.layout.addWidget(self.canvas)

        self.actionAddLayer = QAction(u'Agregar capa',self.frame)
        self.connect(self.actionAddLayer, SIGNAL('activated()'), self.addLayer)
        self.actionZoomIn = QAction(u'+', self.frame)
        self.connect(self.actionZoomIn, SIGNAL('activated()'), self.zoomIn)
        self.actionZoomOut = QAction(u'-', self.frame)
        self.connect(self.actionZoomOut, SIGNAL('activated()'), self.zoomOut)
        self.actionMove = QAction(u'Mover', self.frame)
        self.connect(self.actionMove, SIGNAL('activated()'), self.pan)
        self.actionZoomFull = QAction(u'Enfocar', self.frame)
        self.connect(self.actionZoomFull, SIGNAL('activated()'), self.zoomFull)

        self.toolbar = self.addToolBar('Map')
        self.toolbar.addAction(self.actionAddLayer)
        self.toolbar.addAction(self.actionZoomIn)
        self.toolbar.addAction(self.actionZoomOut)
        self.toolbar.addAction(self.actionMove)
        self.toolbar.addAction(self.actionZoomFull)

        self.toolPan = QgsMapToolPan(self.canvas)
        self.toolZoomIn = QgsMapToolZoom(self.canvas, False)
        self.toolZoomOut = QgsMapToolZoom(self.canvas, True)

        self.layers = []

    def zoomIn(self):
        self.canvas.setMapTool(self.toolZoomIn)

    def zoomOut(self):
        self.canvas.setMapTool(self.toolZoomOut)

    def pan(self):
        self.canvas.setMapTool(self.toolPan)

    def zoomFull(self):
        self.canvas.zoomToFullExtent()

    def addLayer(self):
        layerPath = QFileDialog.getOpenFileName(self, u'Abrir shapefile', '.', 'Shapefiles (*.shp)')
        layerInfo = QFileInfo(layerPath)
        layerProvider = 'ogr'

        # name = '/home/cbdavide/Documentos/Projects/shape-viewer/Colombia/Colombia.shp'

        # layer = QgsVectorLayer(name, 'ejje', layerProvider)
        layer = QgsVectorLayer(layerPath, layerInfo.fileName(), layerProvider)
        if not layer.isValid():
            return

        # Cambiar el color del layer
        symbol_layer = layer.rendererV2().symbols()[0].symbolLayer(0)
        symbol_layer.setColor(QColor(176,251,163))

        QgsMapLayerRegistry.instance().addMapLayer(layer)
        if self.canvas.layerCount() == 0:
            self.canvas.setExtent(layer.extent())

        self.layers.insert(0, QgsMapCanvasLayer(layer))
        self.canvas.setLayerSet(self.layers)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QgsApplication.setPrefixPath(qgis_prefix, True)
    QgsApplication.initQgis()
    window = VisorShapefiles()
    window.move(100, 100)
    window.show()

    r = app.exec_()
    QgsApplication.exitQgis()
    sys.exit(r)
