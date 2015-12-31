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

# from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *

from serval_dialog_base import Ui_Serval

class ServalWidget(QWidget, Ui_Serval):
    def __init__(self, iface):
        QWidget.__init__(self)
        self.setupUi(self)
        self.iface=iface
        self.mapRegistry = QgsMapLayerRegistry.instance()


    def toolPressed(self, position):
        print(position)
        mapCanvasSrs = self.iface.mapCanvas().mapRenderer().destinationCrs()
        pos = position

        # if given no position, get dummy values
        if position is None:
            pos = QgsPoint(0,0)
        # transform points if needed
        elif not mapCanvasSrs == self.raster.crs() and self.iface.mapCanvas().hasCrsTransformEnabled():
            srsTransform = QgsCoordinateTransform(mapCanvasSrs, self.raster.crs())
            try:
                pos = srsTransform.transform(position)
            except QgsCsException, err:
                # ignore transformation errors
                pass

        ident = None
        if position is not None:
            print position


            # # first test if point is within map layer extent
            # # maintain same behaviour as in 1.8 and print out of extent
            # if not self.raster.dataProvider().extent().contains( pos ):
            #     ident = dict()
            #     for iband in range(1,self.raster.bandCount()+1):
            #         ident[iband] = str(self.tr('out of extent'))
            # # we can only use context if layer is not projected
            # elif canvas.hasCrsTransformEnabled() and self.raster.dataProvider().crs() != canvas.mapRenderer().destinationCrs():
            #     ident = layer.dataProvider().identify(pos, QgsRaster.IdentifyFormatValue ).results()
            # else:
            #     extent = canvas.extent()
            #     width = round(extent.width() / canvas.mapUnitsPerPixel());
            #     height = round(extent.height() / canvas.mapUnitsPerPixel());
            #
            #     extent = canvas.mapRenderer().mapToLayerCoordinates( self.raster, extent );
            #
            #     ident = self.raster.dataProvider().identify(pos, QgsRaster.IdentifyFormatValue, canvas.extent(), width, height ).results()




    def populateRastersCbo(self):
        self.rastersCbo.clear()
        for layerId, layer in sorted(self.mapRegistry.mapLayers().iteritems()):
            if layer!=None and layer.isValid() and \
                    layer.type()==QgsMapLayer.RasterLayer and \
                    layer.dataProvider() and \
                    (layer.dataProvider().capabilities() & QgsRasterDataProvider.IdentifyValue):
                  self.rastersCbo.addItem(layer.name(), layerId)

    def layerCboChanged(self):
        curInd = self.rastersCbo.currentIndex()
        lid = self.rastersCbo.itemData(curInd)
        cboLayer = self.rgis.mapRegistry.mapLayer(lid)
        if cboLayer:
            self.raster = cboLayer
