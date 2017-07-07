# -*- coding: utf-8 -*-

import sys

from PyQt4.QtCore import SIGNAL, QFileInfo, QPoint, QByteArray
from PyQt4.QtGui import QMainWindow, QColor, QIcon, QVBoxLayout, QAction, QFileDialog
from PyQt4.QtGui import QApplication, QWidget, QImage

from WindowUI import Ui_MainWindow

import mapnik

class MapnikWidget(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.map = mapnik.Map(256, 256)
        self.qim = QImage()
        #Drag positions
        self.startDragPos = QPoint()
        self.endDragPos = QPoint()
        #Zoom poistion
        self.zoomPos = QPoint()

        self.drag = False
        self.scale = False
        self.total_scale = 1.0

    #temp functions to try a few things
    def createMap(self):
        s = mapnik.Style()
        r = mapnik.Rule()

        polygon_symbolizer = mapnik.PolygonSymbolizer()
        polygon_symbolizer.fill = mapnik.Color('#f2eff9')
        r.symbols.append(polygon_symbolizer)

        line_symbolizer = mapnik.LineSymbolizer()
        line_symbolizer.stroke = mapnik.Color('rgb(50%, 50%, 50%)')
        line_symbolizer.stroke_width = 0.1
        r.symbols.append(line_symbolizer)

        s.rules.append(r)

        self.map.append_style('Estilo1', s)

        #Loading source
        data_source = mapnik.Shapefile(file = 'Colombia/Colombia.shp')
        print data_source.envelope()

        layer = mapnik.Layer('Colombia')
        layer.datasource = data_source
        layer.styles.append('Estilo1')

        self.map.layers.append(layer)
        self.map.zoom_all()

        im = mapnik.Image(self.map.width, self.map.height)
        mapnik.render(self.map, im)

        self.qim.loadFromData(QByteArray(im.tostring('png')))
        self.update()



class VisorShapefiles(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.setWindowTitle(u'Visor de Shapefiles')

        self.layout = QVBoxLayout(self.frame)

        maper = MapnikWidget()
        maper.createMap()

        canvas = QCanvas()

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
