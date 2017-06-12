#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from src import login
from src.model.users import Model
from qgis.core import QgsApplication
from PyQt4.QtGui import QApplication

qgis_prefix = "/usr"

def main():
    app = QApplication(sys.argv)
    QgsApplication.setPrefixPath(qgis_prefix, True)
    QgsApplication.initQgis()

    model = Model()
    ex = login.Window(model)

    r = app.exec_()

    QgsApplication.exitQgis()
    sys.exit(r)

main()
