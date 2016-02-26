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
from qgis.gui import QgsDoubleSpinBox, QgsMessageBar

from _serval_dialog_base import Ui_Serval
import numpy as np
from osgeo import gdal
from osgeo import gdal_array
from osgeo.gdalconst import *

gdal.UseExceptions()

def is_number(s):
    try:
        if np.isnan(float(s)):
            raise ValueError
        float(s)
        return True
    except ValueError:
        return False


class bandSpinBox(QgsDoubleSpinBox):
    def __init__(self, parent):
        QgsDoubleSpinBox.__init__(self, parent)
        self.parent = parent

    def keyPressEvent(self, event):
        b = self.property("bandNr")
        if event.key() == Qt.Key_Return:
            self.setValue(float(self.text()))
            self.parent.changeCellValue(b)
        else:
            QgsDoubleSpinBox.keyPressEvent(self, event)


class ServalWidget(QWidget, Ui_Serval):
    def __init__(self, iface, parent):
        self.iface = iface
        self.parent = parent
        self.canvas = iface.mapCanvas()
        QWidget.__init__(self)
        self.setupUi(self)
        self.setupSpinBoxes()
        self.probing_mode = True
        self.probeBtn.setDown(True)
        self.bands = {}
        self.px = 0
        self.py = 0
        self.mapRegistry = QgsMapLayerRegistry.instance()
        self.iface.currentLayerChanged.connect(self.setActiveRaster)
        self.mapRegistry.layersAdded.connect(self.setActiveRaster)
        self.pencilBtn.clicked.connect(self.activate_pencil)
        self.probeBtn.clicked.connect(self.activate_probing)
        self.mColorButton.colorChanged.connect(self.set_rgb_from_picker)
        self.webpageBtn.clicked.connect(self.showWebsite)


    def activate_pencil(self):
        self.probing_mode = False
        self.canvas.setMapTool(self.parent.drawTool)
        self.pencilBtn.setDown(True)
        self.probeBtn.setDown(False)


    def activate_probing(self):
        self.probing_mode = True
        self.canvas.setMapTool(self.parent.probeTool)
        self.pencilBtn.setDown(False)
        self.probeBtn.setDown(True)


    def setupSpinBoxes(self):
        self.b1SBox = bandSpinBox(self)
        self.b2SBox = bandSpinBox(self)
        self.b3SBox = bandSpinBox(self)
        sboxes = [self.b1SBox, self.b2SBox, self.b3SBox]
        for sbox in sboxes:
            sbox.setMinimumSize(QSize(50, 25))
            sbox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
            sbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
            sbox.setKeyboardTracking(False)
            sbox.setShowClearButton(False)
            sbox.setExpressionsEnabled(False)
            sbox.setStyleSheet("")
            self.bandSpinBoxesLayout.addWidget(sbox)


    def pointClicked(self, point, button):
        if self.raster == None:
            self.iface.messageBar().pushMessage("Serval",
                                                "Choose a raster to set a value",
                                                level=QgsMessageBar.WARNING,
                                                duration = 3)
            return
        mapCanvasSrs = self.iface.mapCanvas().mapRenderer().destinationCrs()
        if point is None:
            pos = QgsPoint(0,0)
        elif not mapCanvasSrs == self.raster.crs() and self.iface.mapCanvas().hasCrsTransformEnabled():
            srsTransform = QgsCoordinateTransform(mapCanvasSrs, self.raster.crs())
            try:
                pos = srsTransform.transform(point)
            except QgsCsException, err:
                self.iface.messageBar().pushMessage("Serval",
                            "Point coordinates transformation failed! Check the raster projection.",
                            level=QgsMessageBar.WARNING,
                            duration = 5)
                return
        else:
            pos = QgsPoint(point.x(), point.y())

        if pos.x() >= self.rbounds[0] and pos.x() <= self.rbounds[2]:
            self.px = int((pos.x() - self.gt[0]) / self.gt[1])
        else:
            self.iface.messageBar().pushMessage("Serval",
                            "Out of x bounds",
                            level=QgsMessageBar.INFO,
                            duration = 2)
            return

        if  pos.y() >= self.rbounds[1] and pos.y() <= self.rbounds[3]:
            self.py = int((pos.y() - self.gt[3]) / self.gt[5])
        else:
            self.iface.messageBar().pushMessage("Serval",
                            "Out of y bounds",
                            level=QgsMessageBar.INFO,
                            duration = 2)
            return

        for nr in range(1, min(4, self.bandCount + 1)):
            self.bands[nr]['array'] = self.bands[nr]['data'].ReadAsArray(self.px, self.py, 1, 1)
            if self.probing_mode:
                if self.bands[nr]['array'] is None or pos.x() < self.gt[0] or pos.y() > self.gt[3] :
                    self.bands[nr]['sbox'].setValue(self.bands[nr]['nodata'])
                else:
                    value = self.bands[nr]['array'][0][0]
                    if is_number(value):
                        self.bands[nr]['sbox'].setValue(value)
                        self.bands[nr]['sbox'].setFocus()
                        self.bands[nr]['sbox'].selectAll()

            else:
                self.changeCellValue(nr)
        if self.bandCount > 2:
            self.mColorButton.setColor(QColor(
                self.bands[1]['sbox'].value(),
                self.bands[2]['sbox'].value(),
                self.bands[3]['sbox'].value()
            ))


    def set_rgb_from_picker(self, c):
        print("New color: {}".format(str(c)))
        self.bands[1]['sbox'].setValue(c.red())
        self.bands[2]['sbox'].setValue(c.green())
        self.bands[3]['sbox'].setValue(c.blue())


    def changeCellValue(self, nr):
        if not self.bands[nr]['array'] is None:
            if self.bands[nr]['gtype'] > 0 and self.bands[nr]['gtype'] < 6:
                value_t = int(self.bands[nr]['sbox'].value())
            elif self.bands[nr]['gtype'] >= 0 and self.bands[nr]['gtype'] < 8:
                value_t = float(self.bands[nr]['sbox'].value())
            else:
                self.iface.messageBar().pushMessage("Serval", "Complex or unknown numeric GDAL data type",
                                                    level=QgsMessageBar.WARNING,
                                                    duration = 5)
                return
            self.bands[nr]['array'][0][0] = value_t
            print value_t
            self.bands[nr]['data'].WriteArray(self.bands[nr]['array'], self.px, self.py)
            self.gdal_raster = None # saved to disk
            self.raster.setCacheImage(None)
            self.raster.triggerRepaint()
            self.activate(True)


    def setActiveRaster(self):
        layer = self.iface.activeLayer()
        if layer!=None and layer.isValid() and \
                layer.type() == 1 and \
                layer.dataProvider() and \
                (layer.dataProvider().capabilities() & 2) and \
                not layer.crs() is None:
            self.raster = layer
            self.curRasterLabel.setText('R: {}'.format(layer.name()))
            # properly close previous raster data if they exist
            try:
                for key, value in self.bands.iteritems():
                    self.bands[key]['data'] = None
                self.bands = {}
                self.gdal_raster = None
            except AttributeError:
                pass
            self.activate(True)
        else:
            self.raster = None
            self.curRasterLabel.setText('R: None')
            self.mColorButton.setDisabled(True)
            self.activate(False)


    def activate(self, bool=True):
        sboxes = [self.b1SBox, self.b2SBox, self.b3SBox]
        for i, sbox in enumerate(sboxes):
            sbox.setProperty('bandNr', i+1)
            sbox.setDisabled(True)
        if bool:
            self.bandCount = self.raster.bandCount()
            if self.bandCount > 2:
                self.mColorButton.setEnabled(True)
            else:
                self.mColorButton.setDisabled(True)
            try:
                self.gdal_raster = gdal.Open(self.raster.source(), GA_Update)
            except:
                self.iface.messageBar().pushMessage("Serval", "Can't write to this raster format",
                                                    level=QgsMessageBar.WARNING,
                                                    duration = 10)
                return
            if self.gdal_raster.GetProjection() == '':
                self.iface.messageBar().pushMessage("Serval", "The raster file has no projection defined. Taking the projection defined in the layer's properities.",
                                                    level=QgsMessageBar.WARNING,
                                                    duration = 6)
                proj_wkt = self.raster.crs().toWkt()
                self.gdal_raster.SetProjection(str(proj_wkt))

            self.gt = self.gdal_raster.GetGeoTransform()
            self.r_width = self.gdal_raster.RasterXSize
            self.r_height = self.gdal_raster.RasterYSize

            # raster bounds [xmin, ymin, xmax, ymax] in raster CRS
            self.rbounds = [
                self.gt[0],
                self.gt[3] + self.r_width * self.gt[4] + self.r_height * self.gt[5],
                self.gt[0] + self.r_width * self.gt[1] + self.r_height * self.gt[2],
                self.gt[3]
            ]
            self.bands = {}
            for nr in range(1, min(4, self.bandCount + 1)):
                self.bands[nr] = {}
                self.bands[nr]['sbox'] = sboxes[nr-1]
                self.bands[nr]['data'] = self.gdal_raster.GetRasterBand(nr)
                # get band's nodata value - if none, set it to -9999 (it will be 0 for byte type)
                if self.bands[nr]['data'].GetNoDataValue() is None:
                    self.bands[nr]['data'].SetNoDataValue(-9999)
                else:
                    pass
                self.bands[nr]['nodata'] = self.bands[nr]['data'].GetNoDataValue()
                self.bands[nr]['sbox'].setEnabled(True)
                self.bands[nr]['array'] = self.bands[nr]['data'].ReadAsArray(0, 0, 1, 1)
                adtype = self.bands[nr]['array'].dtype.type
                self.bands[nr]['gtype'] = gdal_array.NumericTypeCodeToGDALTypeCode(adtype)
                if self.bands[nr]['gtype'] > 0 and self.bands[nr]['gtype'] < 6:
                    self.bands[nr]['sbox'].setMinimum(np.iinfo(adtype).min)
                    self.bands[nr]['sbox'].setMaximum(np.iinfo(adtype).max)
                    self.bands[nr]['sbox'].setDecimals(0)
                elif self.bands[nr]['gtype'] >=6 and self.bands[nr]['gtype'] < 8:
                    self.bands[nr]['sbox'].setMinimum(np.finfo(adtype).min)
                    self.bands[nr]['sbox'].setMaximum(np.finfo(adtype).max)
                    self.bands[nr]['sbox'].setDecimals(4)
                # dt = "Data type: {0}".format(gdal.GetDataTypeName(self.bands[nr]['gtype']))
                # self.dataTypeLabel.setText(dt)


    def showWebsite(self):
        QDesktopServices.openUrl(QUrl('https://github.com/erpas/serval/wiki'))