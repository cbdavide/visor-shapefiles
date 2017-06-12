# -*- coding: utf-8 -*-

from PyQt4.QtGui import QColor
from qgis.gui import QgsMapToolEmitPoint, QgsVertexMarker

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
