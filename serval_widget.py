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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar

from _serval_dialog_base import Ui_Serval
import numpy as np
from osgeo import gdal
from osgeo.gdalconst import *

def is_number(s):
    try:
        if np.isnan(float(s)):
            raise ValueError
        float(s)
        return True
    except ValueError:
        return False

class ServalWidget(QWidget, Ui_Serval):
    def __init__(self, iface):
        self.iface = iface
        QWidget.__init__(self)
        self.setupUi(self)
        self.mapRegistry = QgsMapLayerRegistry.instance()
        self.refreshRastersBtn.clicked.connect(self.populateRastersCbo)
        self.rastersCbo.currentIndexChanged.connect(self.layerCboChanged)
        self.changeCellValueBtn.released.connect(self.changeCellValue)
        self.valueEdit.returnPressed.connect(self.changeCellValue)

    def pointClicked(self, point, button):
        if self.raster == None:
            self.iface.messageBar().pushMessage("Warning", "Choose a raster to set a value", level=QgsMessageBar.INFO)
            return
        mapCanvasSrs = self.iface.mapCanvas().mapRenderer().destinationCrs()
        if point is None:
            pos = QgsPoint(0,0)
        elif not mapCanvasSrs == self.raster.crs() and self.iface.mapCanvas().hasCrsTransformEnabled():
            srsTransform = QgsCoordinateTransform(mapCanvasSrs, self.raster.crs())
            try:
                pos = srsTransform.transform(point)
            except QgsCsException, err:
                # ignore transformation errors
                pass
        self.gdal_raster = gdal.Open(self.raster.source(), GA_Update)
        gt = self.gdal_raster.GetGeoTransform()
        band = self.gdal_raster.GetRasterBand(1)

        self.px = int((pos.x() - gt[0]) / gt[1]) #x pixel
        self.py = int((pos.y() - gt[3]) / gt[5]) #y pixel
        array = band.ReadAsArray(self.px, self.py, 1, 1)
        value = array[0][0]
        self.valarr = np.empty_like (array)
        self.valarr[:] = array
        if value:
            self.valueEdit.setText("{}".format(value))
            self.valueEdit.setFocus()
            self.valueEdit.selectAll()

    def changeCellValue(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        value = self.valueEdit.text()
        print value
        if is_number(value):
            self.valarr[0][0] = float(self.valueEdit.text())
            self.gdal_raster.GetRasterBand(1).WriteArray(self.valarr, self.px, self.py)
            self.gdal_raster = None
            del self.gdal_raster
            del self.valarr
            del self.px, self.py
            self.raster.setCacheImage(None)
            self.raster.triggerRepaint()
            self.layerCboChanged()
            QApplication.restoreOverrideCursor()

    def populateRastersCbo(self):
        self.rastersCbo.clear()
        for layerId, layer in sorted(self.mapRegistry.mapLayers().iteritems()):
            if layer!=None and layer.isValid() and \
                    layer.type() == QgsMapLayer.RasterLayer and \
                    layer.dataProvider() and \
                    (layer.dataProvider().capabilities() & QgsRasterDataProvider.Create):
                  self.rastersCbo.addItem(layer.name(), layerId)

    def layerCboChanged(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        curInd = self.rastersCbo.currentIndex()
        lid = self.rastersCbo.itemData(curInd)
        cboLayer = self.mapRegistry.mapLayer(lid)
        if cboLayer:
            self.raster = cboLayer
        QApplication.restoreOverrideCursor()
