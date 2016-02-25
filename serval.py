# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Serval
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
from qgis.gui import QgsMapToolEmitPoint
from serval_widget import ServalWidget

class Serval:
    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.probeTool = QgsMapToolEmitPoint(self.canvas)
        self.probeTool.setCursor(QCursor(QPixmap(':plugins/icons/mIconColorPicker.svg'), hotX=2, hotY=22))
        self.drawTool = QgsMapToolEmitPoint(self.canvas)
        self.drawTool.setCursor(QCursor(QPixmap(':plugins/icons/mActionToggleEditing.svg'), hotX=2, hotY=22))

    def initGui(self):
        self.action=QAction(QIcon(":/plugins/icons/serval_icon.svg"), "Serval - set raster value tool", self.iface.mainWindow())
        self.iface.addToolBarIcon(self.action)
        QObject.connect(self.action, SIGNAL("triggered()"), self.activateTool)

        self.widget = ServalWidget(self.iface, self)
        self.widget.raster = None
        self.probeTool.canvasClicked.connect(self.widget.pointClicked)
        self.drawTool.canvasClicked.connect(self.widget.pointClicked)

        self.dockwidget=QDockWidget("Serval - Set Raster Value" , self.iface.mainWindow() )
        self.dockwidget.setObjectName("Serval")
        self.dockwidget.setWidget(self.widget)
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockwidget)

        QgsMessageLog.logMessage("Gui loaded", 'Serval', QgsMessageLog.INFO)

    def unload(self):
        # properly close raster data if they exist
        try:
            for key, value in self.bands.iteritems():
                self.bands[key]['data'] = None
            self.bands = None
            self.gdal_raster = None
        except AttributeError:
            pass
        self.widget.px = None
        self.widget.py = None
        self.dockwidget.close()
        self.iface.removeDockWidget(self.dockwidget)
        self.iface.removeToolBarIcon(self.action)

    def activateTool(self):
        self.canvas.setMapTool(self.probeTool)
        self.widget.setActiveRaster()

