import sys

from PyQt4.QtCore import SIGNAL, QFileInfo, QPoint, QByteArray, Qt
from PyQt4.QtGui import QMainWindow, QColor, QIcon, QVBoxLayout, QAction, QFileDialog
from PyQt4.QtGui import QApplication, QWidget, QImage, QPainter

from WindowUI import Ui_MainWindow

import mapnik

class MapnikWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.map = mapnik.Map(750, 500)
        self.map.background = mapnik.Color('steelblue')
        self.qim = QImage()
        #Drag positions
        self.startDragPos = QPoint()
        self.endDragPos = QPoint()
        #Zoom poistion
        self.zoomPos = QPoint()

        self.drag = False
        self.scale = False
        self.total_scale = 1.0

        self.updateMap()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.drag:
            painter.drawImage(self.endDragPos - self.startDragPos, self.qim)
        else:
            painter.drawImage(0, 0, self.qim)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startDragPos = event.pos()
            self.drag = True

    def mouseMoveEvent(self, event):
        if self.drag:
            self.endDragPos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.endDragPos = event.pos()
            self.updateMap()

    def updateMap(self):
        if self.drag:
            cx = int(0.5 * self.map.width)
            cy = int(0.5 * self.map.height)
            dpos = self.endDragPos - self.startDragPos
            self.map.pan(cx - dpos.x(), cy - dpos.y())
            self.drag = False

        im = mapnik.Image(self.map.width, self.map.height)
        mapnik.render(self.map, im)
        self.qim.loadFromData(QByteArray(im.tostring('png')))
        self.update()

        # self.envelopeItem.setText(str(self.map.envelope()))
        # self.widthItem.setText(str(self.map.width))
        # self.heightItem.setText(str(self.map.height))

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

        self.updateMap()

        # im = mapnik.Image(self.map.width, self.map.height)
        # mapnik.render(self.map, im)
        #
        # self.qim.loadFromData(QByteArray(im.tostring('png')))
        # self.update()
