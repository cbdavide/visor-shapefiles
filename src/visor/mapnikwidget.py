import sys

from PyQt4.QtCore import SIGNAL, QFileInfo, QPoint, QByteArray, Qt, QRectF, QTimer
from PyQt4.QtGui import QMainWindow, QColor, QIcon, QVBoxLayout, QAction, QFileDialog
from PyQt4.QtGui import QApplication, QWidget, QImage, QPainter, QMatrix

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

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateMap)

        self.drag = False
        self.scale = False
        self.total_scale = 1.0

        self.updateMap()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.drag:
            painter.drawImage(self.endDragPos - self.startDragPos, self.qim)
        if self.scale:
            painter.save()
            scale = 1 / self.total_scale
            painter.translate(self.zoomPos.x(), self.zoomPos.y())
            painter.scale(scale, scale)
            painter.translate(-self.zoomPos.x(), -self.zoomPos.y())
            exposed = painter.matrix().inverted()[0].mapRect(self.rect())
            painter.drawImage(exposed, self.qim, exposed)
            painter.restore()
        else:
            painter.drawImage(0, 0, self.qim)

        painter.setPen(QColor(0, 0, 0, 100))
        painter.setBrush(QColor(0, 0, 0, 100))
        painter.drawRect(0, 0, 256, 26)
        painter.setPen(QColor(0, 255 , 0))
        painter.drawText(10, 19, 'Scale Denominator: ' + str(self.map.scale_denominator()))

    def wheelEvent(self, event):
        self.zoomPos = event.pos()
        self.total_scale *= 1.0 - event.delta() / (360.0 * 8.0) * 4
        self.scale = True

        self.update()
        self.timer.start(400)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startDragPos = event.pos()
            self.drag = True
        else:
            # transform = self.map.view_transform()
            coord = self.map.view_transform().backward(mapnik.Coord(event.pos().x(), event.pos().y()))
            print coord

            print '>', event.pos().x(), event.pos().y()
            # print self.map.envelope().center()
            # print mapnik.Coord(event.pos().x(), event.pos().y())

    def mouseMoveEvent(self, event):
        if self.drag:
            self.endDragPos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.endDragPos = event.pos()
            self.updateMap()

    def updateMap(self):
        self.timer.stop()

        if self.drag:
            cx = int(0.5 * self.map.width)
            cy = int(0.5 * self.map.height)
            dpos = self.endDragPos - self.startDragPos
            self.map.pan(cx - dpos.x(), cy - dpos.y())
            self.drag = False
        elif self.scale:
            ma = QMatrix()
            ma.translate(self.zoomPos.x(), self.zoomPos.y())
            ma.scale(self.total_scale, self.total_scale)
            ma.translate(-self.zoomPos.x(), -self.zoomPos.y())

            rect = ma.mapRect(QRectF(0, 0, self.map.width, self.map.height))
            env = mapnik.Envelope(rect.left(), rect.bottom(), rect.right(), rect.top())
            self.map.zoom_to_box(self.map.view_transform().backward(env))

            self.total_scale = 1.0
            self.scale = False

        im = mapnik.Image(self.map.width, self.map.height)
        mapnik.render(self.map, im)
        self.qim.loadFromData(QByteArray(im.tostring('png')))
        self.update()

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
        data_source = mapnik.Shapefile(file = '110m-admin-0-countries/ne_110m_admin_0_countries.shp')
        print data_source.envelope()

        layer = mapnik.Layer('Colombia')
        layer.datasource = data_source
        print "\tLayer: ", layer.srs
        layer.styles.append('Estilo1')

        self.map.layers.append(layer)
        self.map.zoom_all()

        self.updateMap()
