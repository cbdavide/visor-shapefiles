# -*- coding: utf-8 -*-

from PyQt4.QtGui import QColor
from PyQt4.QtCore import Qt
from qgis.gui import QgsMapToolEmitPoint, QgsVertexMarker, QgsRubberBand
from qgis.core import QGis

class PointMapTool(QgsMapToolEmitPoint):

    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)

        self.point = None
        self.m = None

    def canvasPressEvent(self, e):
        # if self.m is not None:
        #     self.canvas.scene().removeItem(self.m)

        self.point = self.toMapCoordinates(e.pos())
        # print self.point.x(), self.point.y()

        self.m = QgsVertexMarker(self.canvas)
        self.m.setCenter(self.point)

        self.m.setColor(QColor(34, 167, 240))
        self.m.setIconSize(5)

        self.m.setIconType(QgsVertexMarker.ICON_X)
        self.m.setPenWidth(3)

class PolyMapTool(QgsMapToolEmitPoint):

    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)

        self.rubberband = QgsRubberBand(self.canvas, QGis.Polygon)
        self.rubberband.setColor(Qt.red)
        self.rubberband.setWidth(1)

        self.point = None
        self.points = []

    def canvasPressEvent(self, e):
        self.point = self.toMapCoordinates(e.pos())

        m = QgsVertexMarker(self.canvas)
        m.setCenter(self.point)
        m.setColor(QColor(0, 255, 0))
        m.setIconSize(5)
        m.setIconType(QgsVertexMarker.ICON_BOX)
        m.setPenWidth(3)

        self.points.append(self.point)
        self.isEmittingPoint = True
        self.showPoly()

    def showPoly(self):
        self.rubberband.reset(QGis.Polygon)

        for point in self.points[: -1]:
            self.rubberband.addPoint(point, False)

        self.rubberband.addPoint(self.points[-1], True)
        self.rubberband.show()
