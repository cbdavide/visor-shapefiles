from PyQt4.QtGui import QIcon

class IconFactory:
    @staticmethod
    def cretatePanIcon():
        return QIcon('images/mActionPan.svg')
    @staticmethod
    def createOpenIcon():
        return QIcon('images/mActionAddOgrLayer.svg')
    @staticmethod
    def createZoomInIcon():
        return QIcon('images/mActionZoomIn.svg')
    @staticmethod
    def createZoomOutIcon():
        return QIcon('images/mActionZoomOut.svg')
    @staticmethod
    def createZoomFullIcon():
        return QIcon('images/mActionZoomFullExtent.svg')
    @staticmethod
    def createPointIcon():
        return QIcon('images/mActionCapturePoint.svg')
