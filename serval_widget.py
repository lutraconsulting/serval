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
        self.webpageBtn.released.connect(self.showWebsite)
        self.valueEdit.returnPressed.connect(self.changeCellValue)

    def pointClicked(self, point, button):
        if self.raster == None:
            self.iface.messageBar().pushMessage("Serval", "Choose a raster to set a value", level=QgsMessageBar.WARNING)
            return
        gdal_raster = gdal.Open(self.raster.source(), GA_ReadOnly)
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
        else:
            pos = QgsPoint(point.x(), point.y())

        gt = gdal_raster.GetGeoTransform()
        band = gdal_raster.GetRasterBand(1)
        self.px = int((pos.x() - gt[0]) / gt[1]) #x pixel
        self.py = int((pos.y() - gt[3]) / gt[5]) #y pixel
        self.array = band.ReadAsArray(self.px, self.py, 1, 1)
        if self.array == None:
            self.valueEdit.setText("NULL")
        else:
            value = self.array[0][0]
            if value:
                self.valueEdit.setText("{}".format(value))
                self.valueEdit.setFocus()
                self.valueEdit.selectAll()
        gt = None
        band = None
        array = None
        gdal_raster = None
        value = None

    def changeCellValue(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        gdal_raster = gdal.Open(self.raster.source(), GA_Update)
        band = gdal_raster.GetRasterBand(1)
        value = self.valueEdit.text()
        print value
        if is_number(value):
            self.array[0][0] = float(self.valueEdit.text())
            band.WriteArray(self.array, self.px, self.py)
            self.array = None
            band = None
            gdal_raster = None
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
        curInd = self.rastersCbo.currentIndex()
        lid = self.rastersCbo.itemData(curInd)
        cboLayer = self.mapRegistry.mapLayer(lid)
        if cboLayer:
            self.raster = cboLayer

    def showWebsite(self):
        QDesktopServices.openUrl(QUrl('https://github.com/erpas/serval/wiki'))