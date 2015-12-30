# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ServalDialog
                                 A QGIS plugin
 Set Raster Values
                             -------------------
        begin                : 2015-12-30
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Radosław Pasiok
        email                : rpasiok@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from os.path import dirname
from . table import CustomTable
from osgeo import gdal
from osgeo.gdalconst import *

from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'serval_dialog_base.ui'))

my_array = [['']]

class ServalDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ServalDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.tableWidget = CustomTable(self)
        self.data = my_array
        self.numRows = 10
        self.numCols = 20
        self.tableWidget.setRowCount(self.numRows)
        self.tableWidget.setColumnCount(self.numCols)
        self.tableWidget.addData(self.data)
        # self.tableWidget.setHorizontalHeaderLabels([QString("River"),QString("km"),QString("Working WSEL"), QString("Ref WSEL"), QString("Ref-Working"), QString("Correction")])
        # self.tableWidget.setHorizontalHeaderLabels(["River","km","Working WSEL", "Ref WSEL", "Ref-Working", "Correction"])
        self.tableWidget.setCurrentCell(0, 0)#needed so selectedRanges does not fail initially
        self.verticalLayout.addWidget(self.tableWidget)

        QObject.connect(self.tableWidget,SIGNAL("currentCellChanged(int,int,int,int)"),self.curTableCellChanged)
        self.loadBtn.released.connect(self.loadRaster)

    def curTableCellChanged(self,cRow,cCol,pRow,pCol):
        if self.tableWidget.item(cRow,1):
            curX = float(self.tableWidget.item(cRow,1).text())
            # self.curKm.setValue(curX)
        else:
            pass

    def loadRaster(self):
        s = QSettings("QGIS","Serval")
        lastRasterDir = s.value("lastRasterDir", "")
        rasterFile = QFileDialog.getOpenFileName(self, 'Load raster', directory=lastRasterDir, filter='All Files (*.*)')
        if not rasterFile:
            return
        s.setValue("lastRasterDir", dirname(rasterFile))
        self.raster = gdal.Open(rasterFile, GA_Update)
        self.band = self.raster.GetRasterBand(1)
        self.array = self.band.ReadAsArray()
        self.array_2_table(self.array)

    def array_2_table(self, array):
        cols_nr = array.shape[1]
        rows_nr = array.shape[0]
        self.tableWidget.setColumnCount(cols_nr)
        self.tableWidget.setRowCount(rows_nr)
        for row in range(rows_nr):
          for column in range(cols_nr):
              self.tableWidget.setItem(row,column,QTableWidgetItem("{0}".format(array[row][column])))

